# Toast Backend
  Build Status: ![.github/workflows/main.yml](https://github.com/cci-toast/backend/workflows/.github/workflows/main.yml/badge.svg)
  [![Coverage Status](https://coveralls.io/repos/github/cci-toast/backend/badge.svg?branch=master)](https://coveralls.io/github/cci-toast/backend?branch=master)
## Development Set up
- `git clone` this repo 
- [Install docker](https://docs.docker.com/docker-for-mac/install/)
- Check the version by `docker --version`
- Make sure Docker desktop is running 
- `cd` into `/backend`. This is the project root.
- Create an `.env.dev` file to store the environment variables which can be copied over (Check Slack) 

# Build and Test Workflow
## Build and Run the Docker container
- Open a terminal in the project's root directory, to build and run the container
```
make build
```
- You can browse the Swagger docs to view the api once authenticated
- The Django app will be hosted on `http://0.0.0.0:8000/`
## Run Test Suite with Coverage
- Open a second terminal and run:
```
make test
```
## Stop and Purge all the containers
### Stop all containers:   
```
docker container stop $(docker container ls -aq)
```
### Remove all containers: 
```
docker container rm $(docker container ls -aq)
```

## Handling data migrations in local docker container
In case you have changes to migrate:
```
make migration
```
```
make migrate
```
