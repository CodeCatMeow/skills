# Runtime and Output Directories

Source: https://hydra.cc/docs/tutorials/basic/running_your_app/working_directory/

## What Hydra creates

```text
outputs/YYYY-MM-DD/HH-MM-SS/
├── .hydra/
│   ├── config.yaml
│   ├── hydra.yaml
│   └── overrides.yaml
└── my_app.log
```

Multiruns use `hydra.sweep.dir` / `hydra.sweep.subdir`.

```python
import os
from hydra.core.hydra_config import HydraConfig

print("CWD:", os.getcwd())
print("Output dir:", HydraConfig.get().runtime.output_dir)
```

Prefer `runtime.output_dir` for run-specific artifacts regardless of chdir.

## `hydra.job.chdir`

- `True`: `@hydra.main` chdirs into the job output directory before user code.
- **Default since Hydra 1.2: `False`.** Output dirs and `.hydra` dumps still created.
- Do not force `chdir=True` on repos that use repo-relative data/checkpoint paths.

| chdir | CWD during main | Path style |
| --- | --- | --- |
| `False` (default ≥1.2) | original process directory | repo-relative paths keep working |
| `True` | job output directory | write next to logs; fix repo-relative opens |

When chdir is true:

```python
from hydra.utils import get_original_cwd, to_absolute_path
data_path = to_absolute_path("data/train")
```

## Customize dirs

```yaml
hydra:
  run:
    dir: outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}
  sweep:
    dir: multirun/${now:%Y-%m-%d}/${now:%H-%M-%S}
    subdir: ${hydra.job.num}
  job:
    chdir: false
```

Follow project conventions; do not invent a complex scheme during a small task.
Gitignore `outputs/` and `multirun/`. Keep datasets outside ephemeral run dirs.

## Debug path issues

1. Print `os.getcwd()` and `HydraConfig.get().runtime.output_dir`.
2. Check `hydra.job.chdir` via `--cfg hydra`.
3. Use `to_absolute_path` or an explicit project root when needed.
4. Inspect `hydra.run.dir` / sweep dirs if outputs are hard to find.

| Bad | Good |
| --- | --- |
| Assume Hydra always chdirs | verify default and project setting |
| Hand-roll a second timestamped output system | use/customize Hydra output dirs |
| Assume `Path("outputs")` matches the real run dir | use `runtime.output_dir` |
