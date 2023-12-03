
.PHONY: help
help:
	@echo "****************** COMMANDS  ***********************"
	@echo
	@echo "setup: pip install requirements under the environment folder."
	@echo "lint: Linting using black."
	@echo "lint-check: Lint check from black."
	@echo "test: runs a pytest on tests folder."
	@echo
	@echo "***************************************************"

.PHONY: setup
setup:
	pip install -r environment/requirements.txt

.PHONY: lint
lint:
	black . --line-length 120

.PHONY: lint-check
lint-check:
	black . --line-length 120 --check

.PHONY: test
test:
	python -m pytest tests
