PYTHON ?= python3.8

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

REQUIREMENT_FILES = $(filter-out requirements/_constraint.in, $(wildcard requirements/*.in))

define pipcompile_extra
$(PYTHON) -m piptools compile --output-file=$(basename $(1)).txt $(1) 'requirements/_constraint.in';
endef


# Python Code Style
reformat:
	$(PYTHON) -m black $(ROOT_DIR)
stylecheck:
	$(PYTHON) -m black --check $(ROOT_DIR)
stylediff:
	$(PYTHON) -m black --check --diff $(ROOT_DIR)

# Translations
gettext:
	$(PYTHON) -m redgettext --command-docstrings --verbose --recursive redbot --exclude-files "redbot/pytest/**/*"
upload_translations:
	crowdin upload sources
download_translations:
	crowdin download

# Dependencies
bumpdeps:
	$(PYTHON) -m piptools compile --output-file='requirements/requirements-dev.txt' $(REQUIREMENT_FILES)
	$(foreach file, $(REQUIREMENT_FILES), $(call pipcompile_extra, $(file)))

# Development environment
newenv:
	$(PYTHON) -m venv --clear .venv
	.venv/bin/pip install -U pip setuptools wheel
	$(MAKE) syncenv
syncenv:
	.venv/bin/pip install -Ur ./tools/dev-requirements.txt
