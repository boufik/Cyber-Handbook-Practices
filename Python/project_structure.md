# 1. Filesystem Structure

Suppose that we want to create a Python project with a `main.py` script that will call the functions of other scripts, located in different files. Also, suppose we want any script to be able to import any function of any other script. A good idea is to **convert our repo/project into a Python package**, that will be **importable** and subsequently, we will be able to call any script inside our repo using the **dot notation**.

First, navigate to a desired directory, in which you will create your project. Let's say we want to store our project folder named `pydefense` under `/home/user/Desktop`. Create a folder named `pydefense` under this directory - this will be called as the **project root** - and create an indicative filesystem structure like below:

```
pydefense/                        # Project root (NOT a Python package)
│
├── venv/                         # Virtual environment
├── src/
│   └── pydefense/                # This will be the REAL Python package
│       ├── __init__.py
│       ├── main.py
│       ├── auxiliary/
│       │   ├── __init__.py
│       │   ├── functionalities.py
│       │   └── visualizations.py
│       │   └── ....
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── tool1_wireshark.py
│       │   ├── tool2_nmap.py
│       │   ├── tool3_metasploit.py
│       │   └── ....
│       ├── modules/
│       │   ├── __init__.py
│       │   ├── module1_step1.py
│       │   ├── module2_steps23.py
│       │   ├── module3_steps456.py
│       │   └── ....
│       ├── schemas/
│       │   ├── __init__.py
│       │   └── ....
│       ├── plugins/
│       │   ├── __init__.py
│       │   └── ....
│       └── output/
│       │   ├── __init__.py
│       │   └── ....
│       └── db/
│       │   ├── __init__.py
│       │   └── ....
│
├── README.md
├── requirements.txt
├── pyproject.toml                # NECESSARY, to make our project importable - editable install
└── .gitignore

```





A minimal `pyproject.toml` is:
```
[project]
name = "project"
version = "0.1.0"
description = "OSINT and Cyber Threat Intelligence automation toolkit"
readme = "README.md"
requires-python = ">=3.10"

# Runtime dependencies
dependencies = [
    "pymongo",
    "pandas",
    "requests",
    "beautifulsoup4",
    "pydantic"
]

# Optional metadata
authors = [
    { name = "Your Name", email = "youremail@example.com" }
]

[build-system]
# Required by PEP 517/518
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
# Tells setuptools: "Look inside src/ for packages"
where = ["src"]

```
