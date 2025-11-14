The ideal code is:
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
