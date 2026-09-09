.PHONY: help setup test notebooks notebooks-changed links curriculum-test serve

PYTHON ?= .venv/bin/python

help:
	@echo "Available targets:"
	@echo "  setup              Create a virtual environment and install requirements"
	@echo "  test               Run Python tests"
	@echo "  links              Validate Markdown, Hub, and quiz paths"
	@echo "  curriculum-test    Validate curriculum structure and registry coverage"
	@echo "  notebooks          Execute all curriculum notebooks"
	@echo "  notebooks-changed Execute notebooks added or changed from origin/main"
	@echo "  serve              Serve the static Learning Hub"

setup:
	uv venv
	uv pip install -r requirements.txt

test:
	$(PYTHON) -m pytest -q

notebooks:
	PYTHONPATH=. $(PYTHON) scripts/run_notebooks.py --all

notebooks-changed:
	PYTHONPATH=. $(PYTHON) scripts/run_notebooks.py --base origin/main

links:
	$(PYTHON) scripts/validate_links.py

curriculum-test:
	PYTHONPATH=. $(PYTHON) -m pytest -q tests/test_curriculum.py

serve:
	$(PYTHON) -m http.server --directory hub 8000
