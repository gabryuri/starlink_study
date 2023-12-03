
.PHONY: help
help:
	@echo "****************** COMMANDS  ***********************"
	@echo
	@echo "setup: pip install requirements under the environment folder."
	@echo "lint: Linting using black."
	@echo "test: runs a pytest on tests folder."
	@echo "deploy: runs the application and shows the necessary logs in a convenient sequence."
	@echo
	@echo "***************************************************"

.PHONY: setup
setup:
	pip install -r environment/requirements.txt

.PHONY: lint
lint:
	black . --line-length 120

.PHONY: test
test:
	python -m pytest tests


.PHONY: deploy up initlogs openbrowser 
deploy: up initlogs openbrowser
up:
	docker compose down && docker compose build && docker compose up -d
initlogs:
	docker compose logs -f initialize-db
openbrowser:
	@echo "Opening Google Chrome at http://127.0.0.1:5000/"
	@google-chrome "http://127.0.0.1:5000/" &

