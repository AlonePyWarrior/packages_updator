# Auto Update Python Packages

A simple interactive Python script to find and upgrade outdated packages in your current virtual environment.

This tool:

- lists outdated packages using `pip list --outdated --format=json`
- lets you choose what to upgrade (`all`, `none`, or selected packages)
- upgrades selected packages one by one using `pip install --upgrade`
- uses a rich terminal UI when [`rich`](https://pypi.org/project/rich/) is installed
- automatically falls back to plain text mode when `rich` is not installed

---

## Features

- ✅ Interactive package selection
- ✅ Upgrade all or specific packages by **index** or **name**
- ✅ Optional rich table/progress UI
- ✅ Works without third-party dependencies (Rich is optional)
- ✅ Runs upgrades with the same Python interpreter (`sys.executable`)

---

## Requirements

- Python **3.9+** (recommended)
- `pip` available in the selected environment
- Optional: `rich` for enhanced UI

---

## Installation

### 1) Clone or copy the script

Save the script as:

```bash
update_python_packages.py
```

### 2) Create and activate a virtual environment (recommended)

If you use `uv`:

```cmd
uv venv
.venv\Scripts\activate
```

### 3) (Optional) Install Rich for better UI

```cmd
uv pip install rich
```

If you don't install Rich, the script still works in plain text mode.

---

## Usage

Run the script from an activated environment:

```cmd
python update_python_packages.py
```

You will see outdated packages, then a prompt:

- `a` or `all` → upgrade all outdated packages
- `n` or Enter → skip upgrades
- `1,3,5` → upgrade specific entries by index
- `requests,urllib3` → upgrade by package names
- mixed input works too (e.g. `1,requests,4`)

---

## Example Flow

1. Script fetches outdated packages.
2. Displays a table/list with current and latest versions.
3. Asks which packages to upgrade.
4. Runs:

```bash
python -m pip install --upgrade <package>
```

for each selected package.

---

## Behavior Notes

- Uses the **current interpreter** (`sys.executable`) to ensure upgrades happen in the active environment.
- If `pip list` fails, the script exits and prints the error.
- Unknown package/index input is skipped with a warning.
- In Rich mode, a progress bar and status icons are displayed.

---

## Minimal Dependencies

Strict required third-party dependencies: **none**

Optional dependency:

```txt
rich
```

---

## Security / Operational Considerations

- Upgrading packages may introduce breaking changes.
- Prefer reviewing critical upgrades before applying to production environments.
- Consider pinning versions in `requirements.txt` / lockfiles after successful upgrades.
- Run this in a virtual environment to avoid changing global Python packages.

---

## Suggested `.gitignore` (for this repo)

If this is a standalone repo, add:

```gitignore
.venv/
__pycache__/
*.pyc
```

---

## Roadmap Ideas (Optional)

- `--yes` non-interactive mode
- export before/after versions
- dry-run mode
- skip/include package patterns
- rollback guidance
