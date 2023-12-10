CMD:=.venv/bin/python

.PHONY: setup
setup:
	python3.10 -m venv .venv && ${CMD} -m pip install -r requirements.txt

.PHONY: db
db:
	bash -c "cd infra/docker && ./psql && ./pgadmin"

.PHONY: clean
clean:
	${CMD} -m pyclean .

.PHONY: lint
lint:
	${CMD} -m ruff .

.PHONY: lint-fix
lint-fix:
	${CMD} -m ruff --fix .

.PHONY: fmt
fmt:
	${CMD} -m isort .
	${CMD} -m black .

.PHONY: export-deps
export-deps:
	${CMD} -m pip freeze > requirements.txt

.PHONY: translate-update
translate-update:
	${CMD} manage.py translate enum

.PHONY: translate-verify
translate-verify:
	${CMD} manage.py translate verify

.PHONY: pre-commit
pre-commit:
	${CMD} -m pre-commit run --all-files

.PHONY: tests
tests:
	export DOCKER_BUILDKIT=0
	export COMPOSE_DOCKER_CLI_BUILD=0
	docker compose -f docker-compose.test.yaml up --force-recreate -V --build --exit-code-from test-runner && echo "TEST IS 100% OK"