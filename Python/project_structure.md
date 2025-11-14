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


# 2. Files and Folders

Our project root folder `pydefense` should contain these files and folders:

## a) Root Files

Under root, we have:

* `pyproject.toml`: This folder is **super essential for editable install** of our project. We need one `.toml` file at the root of the project. This instructs Python and pip, where our package lives. One minimal version of this file will be provided below.
* `README.md`: For documentation purposes.
* `.gitignore`: If we intend to push our project content in GitGub.
* `requirements.txt`: We can put any dependencies here.

A minimal `pyproject.toml` could be:

```
[project]
name = "project"
version = "0.1.0"
description = "A defense automation toolkit"
readme = "README.md"
requires-python = ">=3.10"

# Runtime dependencies
dependencies = [
    "numpy",
    "pandas",
    "requests",
    "beautifulsoup4",
    "pymongo"
]

# Optional metadata
authors = [
    { name = "my_name", email = "my_email" }
]

[build-system]
# Required by PEP 517/518
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
# Instructs setuptools: "Look inside src/ for packages"
where = ["src"]
```

## b) Root Folders

Under root, we also have as siblings of the 4 previous files:

* `venv`: It can also be outside the root of the project, but being here does not pose any problem. We can exclude it in versioning by using the sibling file `.gitignore`.
* `src`: This is where our **source code lives** - this is where our **Python package will be located**. Under `src`, only the folder to be imported (`pydefense`) should be present. This is related to the `where` section inside the `pyproject.toml`, in which we instruct `setuptools` to search under the directory we want (`src`) for packages.


## c) The `src` folder

As we mentioned above, this folder should only contain the code of our tool `pydefense`. This will be an importable Python package (effect only under this `venv`) and we can be able to use dot notation like `pydefense.modules.module1`. This way, the `src/pydefense` will be **the only real package**.

Notes:
1. We should NOT treat the project root as a Python package. The Python package will be located explicitly under the `src` folder.
2. The `venv` folder should never be located inside `src`. We can create it either in the root of the project, or completely in another location

## d) The Python package folder `pydefense`

We need to remember that the first `__init__.py` file MUST BE UNDER the Python package folder. So, our first concern is to create an empty `__init__.py` file. **The `__init__.py` files are necessary, so that Python understands any folder as an importable module**. Besides, from the first section of the documentation (`Filesystem Structure`), you will have noticed that **every folder** under the `pydefense`. This is essential to use dot notation between our modules. So, under `pydefense`, we have:

### Files

* `__init__.py`: Necessary for dot notation and editable install.
* `main.py`: The main script file that will combine the functionalities, described in the functions of its sibling folders.

## Folders

* `auxiliary`: Put any auxiliary functions for visualization and of course an empty `__init__.py`, symbolizing that Python will detect it as a module under `k3recon`.
* `modules`: Include a `__init__.py`
* `tools`: Include a `__init__.py`


# 3. Run `main.py`

After setting up this structure, including the empty `__init__.py` files and the minimal `pyproject.toml` file, you can populate your project by adding content in the `main.py` and the scripts under the `src/pydefense` folders. But first, you need to install your project as a Python package using `pip`, so first go to the root directory and type these commands. **It is important to run this command under the root directory.**

```
cd /home/user/Desktop/pydefense
pip install -e .
```
