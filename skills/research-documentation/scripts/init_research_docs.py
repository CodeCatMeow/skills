#!/usr/bin/env python3
"""Initialize a minimal, non-destructive research documentation structure."""

from __future__ import annotations

import argparse
import os
import re
import stat
import sys
from datetime import date
from pathlib import Path
from typing import Sequence


TEMPLATE_FILES = {
    Path("README.md"): "research-readme.md",
    Path("status.md"): "status.md",
    Path("roadmap.md"): "roadmap.md",
}
WEEKLY_LOG_TEMPLATE = "weekly-log.md"

INDEX_FILES = {
    Path("knowledge/README.md"): (
        "# Stable Knowledge\n\n"
        "Organize reusable understanding by topic, with links to supporting evidence, limitations, and related decisions.\n"
    ),
    Path("knowledge/pitfalls/README.md"): (
        "# Reusable Pitfalls\n\n"
        "Record problems likely to recur, whose cause is unclear, whose fix is error-prone, or that need regression prevention. Keep one-off issues in the weekly log.\n"
    ),
    Path("decisions/README.md"): (
        "# Research Decisions\n\n"
        "Use `ADR-YYYYMMDD-short-name.md` for important choices, including context, alternatives, rationale, and trade-offs.\n"
    ),
    Path("protocols/README.md"): (
        "# Research Protocols\n\n"
        "Organize methods that must be executed consistently by topic, including inputs, steps, outputs, failure handling, and environment assumptions.\n"
    ),
    Path("experiments/README.md"): (
        "# Experiment Index\n\n"
        "Organize experiments by year and `EXP-YYYYMMDD-short-slug`. Related runs that answer one question share a plan and report.\n"
    ),
}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        argv: Optional argument sequence for programmatic invocation.

    Returns:
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Create missing research documentation without modifying existing files."
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="Project root to initialize (default: current directory).",
    )
    parser.add_argument(
        "--allow-redirected-research-root",
        action="store_true",
        help=(
            "Allow research itself to be a single symlink or Windows Junction. "
            "Redirected paths below research remain prohibited."
        ),
    )
    return parser.parse_args(argv)


def relative_name(path: Path, project_root: Path) -> str:
    """Return a path relative to the project root for status output."""
    return path.relative_to(project_root).as_posix()


def is_link_or_junction(path: Path) -> bool:
    """Return whether a path redirects filesystem traversal."""
    if path.is_symlink():
        return True
    if hasattr(path, "is_junction") and path.is_junction():
        return True
    if os.name != "nt":
        return False
    try:
        return bool(path.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
    except (FileNotFoundError, AttributeError):
        return False


def validate_no_redirect_components(path: Path) -> None:
    """Reject a path that includes a symlink or Windows Junction."""
    current = Path(path.anchor)
    parts = path.parts[1:] if path.anchor else path.parts
    for part in parts:
        current /= part
        if is_link_or_junction(current):
            raise OSError(f"Refusing redirected path: {current}")


def validate_managed_path(path: Path, research_root: Path) -> None:
    """Reject managed paths that escape a research root or traverse redirects."""
    if is_link_or_junction(research_root):
        raise OSError(f"Refusing redirected research root: {research_root}")
    try:
        relative = path.relative_to(research_root)
    except ValueError as error:
        raise OSError(f"Target is outside the research root: {path}") from error

    current = research_root
    for part in relative.parts:
        current /= part
        if is_link_or_junction(current):
            raise OSError(f"Refusing redirected path: {current}")

    resolved = path.resolve(strict=False)
    if not resolved.is_relative_to(research_root):
        raise OSError(f"Resolved target is outside the research root: {path}")


def validate_directory_target(path: Path, research_root: Path) -> None:
    """Validate a directory before any initialization writes occur."""
    validate_managed_path(path, research_root)
    if path.exists() and not path.is_dir():
        raise NotADirectoryError(f"Expected a directory at {path}")


def validate_file_target(path: Path, research_root: Path) -> None:
    """Validate a file before any initialization writes occur."""
    validate_managed_path(path, research_root)
    if path.exists() and not path.is_file():
        raise IsADirectoryError(f"Expected a file at {path}")


def reported_name(path: Path, research_root: Path, display_root: Path) -> str:
    """Return a stable project-relative name for status output."""
    display_path = display_root / path.relative_to(research_root)
    return relative_name(display_path, display_root.parent)


def ensure_directory(path: Path, research_root: Path, display_root: Path) -> None:
    """Create a validated directory when missing and report its outcome."""
    validate_directory_target(path, research_root)
    if path.exists():
        print(f"SKIPPED {reported_name(path, research_root, display_root)}")
        return

    try:
        validate_directory_target(path, research_root)
        path.mkdir()
    except FileExistsError:
        validate_directory_target(path, research_root)
        print(f"SKIPPED {reported_name(path, research_root, display_root)}")
        return
    print(f"CREATED {reported_name(path, research_root, display_root)}")


def read_template(template_path: Path) -> str:
    """Read a required UTF-8 template with a clear error."""
    try:
        return template_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise OSError(f"Cannot read required template {template_path}: {error}") from error


def create_file(path: Path, content: str, research_root: Path, display_root: Path) -> None:
    """Create a UTF-8 file exclusively after a final target revalidation."""
    validate_file_target(path, research_root)
    if path.exists():
        print(f"SKIPPED {reported_name(path, research_root, display_root)}")
        return

    try:
        validate_file_target(path, research_root)
        with path.open("x", encoding="utf-8", newline="\n") as file:
            file.write(content)
    except FileExistsError:
        validate_file_target(path, research_root)
        print(f"SKIPPED {reported_name(path, research_root, display_root)}")
        return

    print(f"CREATED {reported_name(path, research_root, display_root)}")


def current_iso_week() -> tuple[int, int]:
    """Return the current ISO week-year and week number."""
    iso_year, iso_week, _ = date.today().isocalendar()
    return iso_year, iso_week


def log_path_for_week(research_root: Path, iso_year: int, iso_week: int) -> Path:
    """Return an ISO-week log path below a research root."""
    return research_root / "logs" / str(iso_year) / f"{iso_year}-W{iso_week:02d}.md"


def render_weekly_log(template: str, iso_year: int, iso_week: int) -> str:
    """Replace the weekly-log title placeholder with an ISO week."""
    return template.replace("<!-- YYYY-Www -->", f"{iso_year}-W{iso_week:02d}", 1)


def render_status(template: str, iso_year: int, iso_week: int) -> str:
    """Replace the status template's current-log placeholder."""
    relative_path = f"logs/{iso_year}/{iso_year}-W{iso_week:02d}.md"
    link = f"[{relative_path}]({relative_path})"
    return re.sub(r"<!--\s*CURRENT_WEEKLY_LOG_LINK\b.*?-->", link, template, count=1)


def resolve_research_root(project_root: Path, allow_redirected_root: bool) -> Path:
    """Return the real research root, allowing only its one direct redirect."""
    requested_root = project_root / "research"
    if not is_link_or_junction(requested_root):
        return requested_root
    if not allow_redirected_root:
        raise OSError(
            "Refusing redirected research root. Use "
            "--allow-redirected-research-root to allow one explicit redirect."
        )

    try:
        link_target = Path(os.readlink(requested_root))
    except OSError as error:
        raise OSError(f"Cannot inspect redirected research root: {requested_root}") from error

    direct_target = link_target if link_target.is_absolute() else requested_root.parent / link_target
    direct_target = Path(os.path.abspath(direct_target))
    validate_no_redirect_components(direct_target)
    resolved_root = direct_target.resolve(strict=False)
    print(f"WARNING: initializing redirected research root at {resolved_root}")
    return resolved_root


def initialize(
    project_root: Path, allow_redirected_research_root: bool = False
) -> None:
    """Create only the missing documentation structure for a project.

    Args:
        project_root: Existing directory that will contain ``research``.
        allow_redirected_research_root: Permit one direct research-root redirect.

    Raises:
        OSError: If templates or target paths cannot be read or created safely.
    """
    project_root = project_root.resolve()
    if not project_root.is_dir():
        raise NotADirectoryError(f"Project root is not a directory: {project_root}")

    iso_year, iso_week = current_iso_week()
    display_research_root = project_root / "research"
    research_root = resolve_research_root(
        project_root, allow_redirected_research_root
    )
    log_path = log_path_for_week(research_root, iso_year, iso_week)
    template_root = Path(__file__).resolve().parent.parent / "templates"

    file_contents: dict[Path, str] = {}
    for target, template_name in TEMPLATE_FILES.items():
        path = research_root / target
        if not path.exists():
            content = read_template(template_root / template_name)
            if target == Path("status.md"):
                content = render_status(content, iso_year, iso_week)
            file_contents[path] = content

    if not log_path.exists():
        template = read_template(template_root / WEEKLY_LOG_TEMPLATE)
        file_contents[log_path] = render_weekly_log(template, iso_year, iso_week)

    for target, content in INDEX_FILES.items():
        path = research_root / target
        if not path.exists():
            file_contents[path] = content

    directories = (
        research_root,
        research_root / "knowledge",
        research_root / "knowledge" / "pitfalls",
        research_root / "decisions",
        research_root / "protocols",
        research_root / "experiments",
        research_root / "logs",
        log_path.parent,
    )
    file_targets = (
        *(research_root / target for target in TEMPLATE_FILES),
        *(research_root / target for target in INDEX_FILES),
        log_path,
    )

    for directory in directories:
        validate_directory_target(directory, research_root)
    for path in file_targets:
        validate_file_target(path, research_root)

    for directory in directories:
        ensure_directory(directory, research_root, display_research_root)
    for path in file_targets:
        if path in file_contents:
            create_file(path, file_contents[path], research_root, display_research_root)
        else:
            print(f"SKIPPED {reported_name(path, research_root, display_research_root)}")


def main(argv: Sequence[str] | None = None) -> int:
    """Run the research documentation initializer.

    Args:
        argv: Optional argument sequence for programmatic invocation.

    Returns:
        Process exit status.
    """
    args = parse_args(argv)
    try:
        initialize(args.project_root, args.allow_redirected_research_root)
    except OSError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
