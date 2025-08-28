.PHONY: venv install backend cli frontend bot gradio

PYTHON ?= python3
VENV_DIR := .venv
PY := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

venv:
	@test -x $(PY) || $(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment ready in $(VENV_DIR)"
	
.env: .env.example
	@test -f .env || (cp .env.example .env && echo "Created .env")

install: venv .env
	$(PY) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt
	cd app/frontend && npm ci 

backend:
	RUN_MODE=web $(PY) -m app.backend.main

cli:
	RUN_MODE=cli $(PY) -m app.backend.main

frontend:
	cd app/frontend && npm run dev

bot:
	$(PY) -m app.backend.telegram_bot

gradio:
	$(PY) -m app.backend.demo_gradio
