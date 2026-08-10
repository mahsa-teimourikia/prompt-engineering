.PHONY: setup test notebooks serve

PYTHON := .venv/bin/python

setup:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

test:
	$(PYTHON) -m pytest -q

notebooks:
	$(PYTHON) scripts/validate_notebooks.py --execute

serve:
	$(PYTHON) -m http.server --directory hub 8000
