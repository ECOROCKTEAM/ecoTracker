CMD:=poetry run

.PHONY: setup
setup:
	poetry install && ${CMD} pre-commit install

.PHONY: clean
clean:
	${CMD} pyclean .

.PHONY: lint
lint:
	${CMD} ruff .

.PHONY: lint-fix
lint-fix:
	${CMD} ruff --fix .

.PHONY: fmt
fmt:
	${CMD} isort .
	${CMD} black .

.PHONY: export-deps
export-deps:
	poetry export --without-hashes -f requirements.txt --output requirements.txt

.PHONY: translate-update
translate-update:
	${CMD} python manage.py translate enum

.PHONY: translate-verify
translate-verify:
	${CMD} python manage.py translate verify

.PHONY: pre-commit
pre-commit:
	${CMD} pre-commit run --all-files

.PHONY: tests
tests:
	export DOCKER_BUILDKIT=0
	export COMPOSE_DOCKER_CLI_BUILD=0
	docker compose -f docker-compose.test.yaml up --force-recreate -V --build --exit-code-from test-runner
