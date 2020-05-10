# Build and Test Workflow
All the django directories moved out of /app.
After you pull the new master branch:
- Make sure there’s a file called pytest.ini in django_app folder after you pulled successfully from new-master 
(remove pytest.ini from your .gitignore (pytest needs this file)

- Make sure you've stopped and deleted any stray containers, that may interfere with the build process.
## Stop and Purge all docker containers 
From the backend root:
```docker container stop $(docker container ls -aq)```

```docker container rm $(docker container ls -aq)```

# Build Process
## 1. Build and run local docker container
#### `docker-compose -f docker-compose-dev.yml up --build`

## 2. Run Pytest in local docker container
#### `docker-compose -f docker-compose-dev.yml run web pytest`

**When you write new tests and want to run the test suite, make sure you** 
- **stop and purge all old containers** 
- **add your test-entity-api class to tests __init__.py** 
- **rebuild the container (see 1) and then run pytest (see 2)**

#### Handling data migrations in local docker container

In case you have changes to migrate:
```
`docker-compose -f docker-compose-dev.yml run web python3 manage.py makemigrations`

`docker-compose -f docker-compose-dev.yml run web python3 manage.py migrate`
```