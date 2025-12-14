.PHONY: setup run prompt-compare test-qwerty clean help

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

help:
	@echo "Available targets:"
	@echo "  make setup          - Create virtualenv and install dependencies"
	@echo "  make run            - Run the typo correction experiment"
	@echo "  make prompt-compare - Run prompt comparison experiment (all 6 prompts)"
	@echo "  make test-qwerty    - Test QWERTY_CONCISE prompt only (18 cases)"
	@echo "  make clean          - Remove virtualenv and generated files"

setup:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV)
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Setup complete!"
	@echo "Don't forget to create .env file with your OPENAI_API_KEY"

run:
	@echo "Running typo correction experiment..."
	cd $(dir $(abspath $(lastword $(MAKEFILE_LIST)))) && PYTHONPATH=. $(PYTHON) src/experiment.py

prompt-compare:
	@echo "Running prompt comparison experiment..."
	@echo "This will test 6 different prompts on all test cases."
	cd $(dir $(abspath $(lastword $(MAKEFILE_LIST)))) && PYTHONPATH=. $(PYTHON) src/prompt_comparison.py

test-qwerty:
	@echo "Testing QWERTY_CONCISE prompt only..."
	@echo "This will test 1 prompt on all 18 test cases."
	cd $(dir $(abspath $(lastword $(MAKEFILE_LIST)))) && PYTHONPATH=. $(PYTHON) src/test_qwerty_concise.py

clean:
	@echo "Cleaning up..."
	rm -rf $(VENV)
	rm -rf src/__pycache__
	rm -rf src/prompts/__pycache__
	rm -rf results
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "Clean complete!"
