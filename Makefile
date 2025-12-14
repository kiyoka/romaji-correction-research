.PHONY: setup run clean help

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

help:
	@echo "Available targets:"
	@echo "  make setup  - Create virtualenv and install dependencies"
	@echo "  make run    - Run the typo correction experiment"
	@echo "  make clean  - Remove virtualenv and generated files"

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
	$(PYTHON) src/experiment.py

clean:
	@echo "Cleaning up..."
	rm -rf $(VENV)
	rm -rf src/__pycache__
	rm -rf src/prompts/__pycache__
	rm -rf results
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "Clean complete!"
