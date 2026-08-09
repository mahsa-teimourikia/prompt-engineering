.PHONY: setup test notebooks serve

setup:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

test:
	pytest -q

notebooks:
	python scripts/validate_notebooks.py

serve:
	python -m http.server --directory hub 8000
