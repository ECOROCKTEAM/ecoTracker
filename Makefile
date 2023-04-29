CMD:=poetry run

.PHONY: setup
setup:
	poetry install && ${CMD} pre-commit install

.PHONY: lint
lint:
	${CMD} ruff .

.PHONY: lint-fix
lint-fix:
	${CMD} ruff --fix .

.PHONY: export-deps
export-deps:
	poetry export --without-hashes -f requirements.txt --output requirements.txt

.PHONY: pre-commit
pre-commit:
	${CMD} pre-commit run --all-files