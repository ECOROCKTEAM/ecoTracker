# EcoTracker

## DEVELOP

1. Git clone
2. Checkout to develop branch

    `git checkout origin/develop`

3. Unpack `EcoTrackerEnv.zip` to root of project
4. Run tests

    `make tests`

5. Run application, database, pgadmin

    `make devapp`

6. Go to browser

    `localhost:5050` - pgadmin

    `localhost:8000/docs` - swagger

7. Connect pgadmin to database

    Login to pgadmin usage credentials from `env/dev/pgadmin.env`

    Add server usage credentials from `env/dev/dev.env`, see `DATABASE_*` env

8. Done!

9. For stop use cmd `make devstop`

10. For drop all containers use cmd `make devclear`

### Develop backend

1. Same steps ^

2. But copy `dev.env` rom `env/dev/dev.env` to root of project

3. Clear already running containers with `make devclear`

4. Run `make devdb`

5. Run `alembic upgrade head`

6. Run uvicorn `uvicorn src.http.app:create_app --factory`
