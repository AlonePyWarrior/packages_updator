# py-pkg-updater

A simple command-line tool for checking and upgrading outdated Python packages in your current environment.

`py-pkg-updater` helps you quickly inspect outdated `pip` packages, review the current and latest versions, and upgrade selected packages directly from the terminal.

---

## Features

- Detect outdated packages using `pip list --outdated`
- Display outdated packages in a clean terminal table
- Upgrade all packages or selected packages only
- Supports both package names and numeric selection
- Uses Rich for a better terminal interface when available
- Falls back to plain terminal output if Rich is not installed

---

## Installation

Install from PyPI:

```bash
pip install py-pkg-updater
````

---

## Usage

Run the command inside the Python environment you want to update:

```bash
update-packages
```

The tool will show outdated packages and ask what you want to upgrade.

Example options:

```text
A        upgrade all packages
N        skip upgrading
1,3,5    upgrade selected packages by number
rich,pip upgrade selected packages by name
```

---

## Example

```bash
update-packages
```

Example output:

```text
Outdated packages

#   Package      Current    Latest
1   pip          24.0       25.1.1
2   rich         13.7.0     13.9.4

Choose packages to upgrade:
A  upgrade all
N  skip upgrading
1,3,5  comma-separated indices or package names
```

---

## Recommended Use

Use this tool inside an activated virtual environment:

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install py-pkg-updater
update-packages
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install py-pkg-updater
update-packages
```

---

## Why Use a Virtual Environment?

This tool upgrades packages in the Python environment where it is executed.

For safer package management, run it inside a project-specific virtual environment instead of your global Python installation.

---

## Requirements

* Python 3.9 or newer
* pip
* rich

---

## Development

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/py-pkg-updater.git
cd py-pkg-updater
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source venv/bin/activate
```

Install in editable mode:

```bash
pip install -e .
```

Run locally:

```bash
update-packages
```

---

## Build

Install build tools:

```bash
pip install --upgrade build twine
```

Build the package:

```bash
python -m build
```

This creates distribution files inside the `dist/` directory.

---

## Publish

Upload to PyPI:

```bash
python -m twine upload dist/*
```

---

## Project Structure

```text
py-pkg-updater/
├── src/
│   └── update_python_packages/
│       ├── __init__.py
│       └── cli.py
├── pyproject.toml
├── README.md
├── LICENSE
└── dist/
```

---

## Security Note

Be careful when upgrading many packages at once. Package updates can introduce breaking changes, especially in active projects.

Recommended workflow:

1. Activate your virtual environment.
2. Run `update-packages`.
3. Upgrade selected packages.
4. Test your project.
5. Commit dependency changes if everything works.

---

## License

This project is licensed under the MIT License.

---

## Author

Created by Ali Esmaeilzadeh.