CMD:=.venv/bin/python

.PHONY: setup
setup:
	python3.10 -m venv .venv && ${CMD} -m pip install -r requirements.txt

.PHONY: localdb
localdb:
	docker run --name psql -d -p 5432:5432 --env-file=infra/dev/docker/db.env postgres:15-alpine
	docker run --name pgadmin --link psql -d -p 5050:80 --env-file=infra/dev/docker/pgadmin.env dpage/pgadmin4

.PHONY: localdbclean
localdbclean:
	docker rm -f pgadmin
	docker rm -f psql

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
	docker compose -f docker-compose.testrunner.yaml up --force-recreate -V --build --exit-code-from test-runner && echo "TEST IS 100% OK"