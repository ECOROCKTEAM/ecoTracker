# EcoTracker

## How to start

1. Git clone
2. Check on exist db containers in docker and delete them:

    ```bash
    docker rm -f localpsql
    docker rm -f pgadmin
    ```

3. Create db containers in docker:

    ```bash
    make db
    ```

4. ```make setup```
5. Activate venv: ```source .venv/bin/activate```
6. ```make tests```
7. Go to code: ```code .```
