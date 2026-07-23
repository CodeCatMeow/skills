param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot ".."))
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$skillsRoot = Join-Path $Root "skills"
if (-not (Test-Path -LiteralPath $skillsRoot -PathType Container)) {
    throw "Missing skills directory: $skillsRoot"
}

$errors = [System.Collections.Generic.List[string]]::new()
$skillFiles = @(Get-ChildItem -LiteralPath $skillsRoot -Filter "SKILL.md" -File -Recurse)

if ($skillFiles.Count -eq 0) {
    $errors.Add("No SKILL.md files found under $skillsRoot")
}

foreach ($skillFile in $skillFiles) {
    $skillDirectory = $skillFile.Directory
    $relativeDirectory = [System.IO.Path]::GetRelativePath($skillsRoot, $skillDirectory.FullName)

    if ($relativeDirectory -match "[\\/]") {
        $errors.Add("Nested skill is not allowed: skills/$($relativeDirectory.Replace('\', '/'))")
    }

    if ($skillDirectory.Name -notmatch "^[a-z0-9]+(?:-[a-z0-9]+)*$") {
        $errors.Add("Skill directory must use lowercase kebab-case: $($skillDirectory.Name)")
    }

    $content = Get-Content -LiteralPath $skillFile.FullName -Raw -Encoding utf8
    if ($content -notmatch "(?s)\A---\r?\n(?<frontmatter>.*?)\r?\n---(?:\r?\n|\z)") {
        $errors.Add("Missing or malformed YAML frontmatter delimiters: $($skillFile.FullName)")
        continue
    }

    $frontmatter = $Matches.frontmatter
    $namePattern = '(?m)^name:\s*[''"]?(?<value>[^''"\r\n]+)[''"]?\s*$'
    $nameMatch = [regex]::Match($frontmatter, $namePattern)
    $descriptionMatch = [regex]::Match($frontmatter, "(?m)^description:\s*(?<value>.*)$")

    if (-not $nameMatch.Success) {
        $errors.Add("Missing frontmatter name: $($skillFile.FullName)")
    }
    else {
        $name = $nameMatch.Groups["value"].Value.Trim()
        if ($name -notmatch "^[a-z0-9]+(?:-[a-z0-9]+)*$") {
            $errors.Add("Frontmatter name must use lowercase kebab-case: $name")
        }
        if ($name -cne $skillDirectory.Name) {
            $errors.Add("Frontmatter name '$name' must match directory '$($skillDirectory.Name)'")
        }
    }

    if (-not $descriptionMatch.Success) {
        $errors.Add("Missing frontmatter description: $($skillFile.FullName)")
    }
    else {
        $descriptionStart = $descriptionMatch.Groups["value"].Value.Trim()
        $hasIndentedContinuation = [regex]::IsMatch(
            $frontmatter.Substring($descriptionMatch.Index + $descriptionMatch.Length),
            "\A(?:\r?\n[ \t]+\S.*)+"
        )
        if ([string]::IsNullOrWhiteSpace($descriptionStart) -and -not $hasIndentedContinuation) {
            $errors.Add("Empty frontmatter description: $($skillFile.FullName)")
        }
    }

    $nestedSkillFiles = @(
        Get-ChildItem -LiteralPath $skillDirectory.FullName -Filter "SKILL.md" -File -Recurse |
            Where-Object { $_.FullName -ne $skillFile.FullName }
    )
    foreach ($nestedSkillFile in $nestedSkillFiles) {
        $errors.Add("Nested SKILL.md will be hidden from cc-switch: $($nestedSkillFile.FullName)")
    }
}

$unexpectedRootSkill = Join-Path $Root "SKILL.md"
if (Test-Path -LiteralPath $unexpectedRootSkill -PathType Leaf) {
    $errors.Add("Repository-root SKILL.md would hide every nested skill from cc-switch")
}

$unexpectedSkillsRootSkill = Join-Path $skillsRoot "SKILL.md"
if (Test-Path -LiteralPath $unexpectedSkillsRootSkill -PathType Leaf) {
    $errors.Add("skills/SKILL.md would hide every skill below it from cc-switch")
}

if ($errors.Count -gt 0) {
    foreach ($message in $errors) {
        Write-Error $message
    }
    exit 1
}

Write-Host "Validated $($skillFiles.Count) skill(s)."
foreach ($skillFile in $skillFiles) {
    Write-Host "  OK  $([System.IO.Path]::GetRelativePath($Root, $skillFile.FullName).Replace('\', '/'))"
}
