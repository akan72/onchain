python_version="python3.9"

.PHONY: lint test

install:
	python3 -m venv env; \
	source env/bin/activate; \
	python -m pip install --upgrade pip; \
	pip install -r requirements.txt

lint:
	$(python_version) -m pylint onchain/*py

test:
	$(python_version) test/unittests.py
