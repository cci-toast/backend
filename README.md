# Toast Backend
  Build Status: ![.github/workflows/main.yml](https://github.com/cci-toast/backend/workflows/.github/workflows/main.yml/badge.svg)
## Development Set up
- `git clone` this repo 
- [Install docker](https://docs.docker.com/docker-for-mac/install/)
- Check the version by `docker --version`
- Make sure Docker desktop is running 
- `cd` into `/backend`. This is the project root.
- Create an `.env.dev` file to store the environment variables which can be copied over (Check Slack) 

# Build and Test Workflow
## Build and Run the Docker container
- Open a terminal in the project's root directory
- You can browse the Swagger docs to view the api once authenticated
`make build`
- The Django app will be hosted on `http://0.0.0.0:8000/`
## Run Test Suite with Coverage
- Open a second terminal and run:
`make test`
## Stop and Purge all the containers
  Stop:   `docker container stop $(docker container ls -aq)`
  Purge:  `docker container rm $(docker container ls -aq)`

**When you write new tests and want to run the test suite, make sure you** 
- **stop and purge all old containers** 
- **add your test-<entity> class to tests __init__.py** 
- **rebuild the container (see 1) and then run pytest (see 2)**

#### Handling data migrations in local docker container
In case you have changes to migrate:
- The equivalent of running _python manage.py makemigrations_
`make migration`
- The equivalent of running _python manage.py migrate_
`make migrate`
