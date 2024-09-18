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
	docker compose -f docker-compose.root.yaml up test_runner_app test_runner_db --force-recreate -V --remove-orphans --build --exit-code-from test_runner_app && echo "TEST IS 100% OK"

.PHONY: devdb
devdb:
	export DOCKER_BUILDKIT=0
	export COMPOSE_DOCKER_CLI_BUILD=0
	docker compose -f docker-compose.root.yaml up -d dev_db dev_pgadmin -V --build --remove-orphans

.PHONY: devapp
devapp:
	export DOCKER_BUILDKIT=0
	export COMPOSE_DOCKER_CLI_BUILD=0
	docker compose -f docker-compose.root.yaml up -d dev_app dev_db dev_pgadmin -V --build
	sleep 5
	docker compose -f docker-compose.root.yaml exec dev_app alembic upgrade head

.PHONY: devstop
devstop:
	export DOCKER_BUILDKIT=0
	export COMPOSE_DOCKER_CLI_BUILD=0
	docker compose -f docker-compose.root.yaml stop dev_app dev_db dev_pgadmin

.PHONY: devclear
devclear:
	export DOCKER_BUILDKIT=0
	export COMPOSE_DOCKER_CLI_BUILD=0
	docker compose -f docker-compose.root.yaml down dev_app dev_db dev_pgadmin -v