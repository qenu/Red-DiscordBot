from pathlib import Path
from setuptools import setup
import os

REQUIREMENTS_FOLDER = Path(__file__).absolute().parent / "requirements"

with open(REQUIREMENTS_FOLDER / "base.txt") as fp:
    base_requirements = fp.read().splitlines()

extras = {}
for file in REQUIREMENTS_FOLDER.glob("extra-*.txt"):
    with file.open() as fp:
        extras[file.stem[len("extra-") :]] = fp.read().splitlines()

extras["dev"] = list({req for extra_reqs in extras.values() for req in extra_reqs})
extras["all"] = list(
    {
        req
        for extra_name, extra_reqs in extras.items()
        if extra_name in ("postgres",)
        for req in extra_reqs
    }
)

# Metadata and options defined in setup.cfg
setup(
    install_requires=base_requirements,
    extras_require=extras,
)
