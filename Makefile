.PHONY: venv install run test lint docker clean

PYTHON := python3
VENV := .venv
ACTIVATE := source $(VENV)/bin/activate

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(ACTIVATE) && pip install --upgrade pip && pip install -r requirements.txt

run:
	$(ACTIVATE) && python src/elogsum/cli.py \
		--input examples/sample_log.csv \
		--time-col timestamp \
		--value-cols temp,voltage,current \
		--out-dir artifacts/dev_run

test:
	$(ACTIVATE) && pytest -q tests/

lint:
	$(ACTIVATE) && ruff check src tests

docker:
	docker build -t engineering-log-summariser .

clean:
	rm -rf $(VENV) artifacts __pycache__ .pytest_cache
