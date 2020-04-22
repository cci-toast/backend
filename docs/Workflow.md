# CI/CD with Docker, Travis-CI and Heroku
We had two options to go about setting up the CI/CD pipeline: 
### 1. Container registry
Either we build the Docker container locally, and then push the image to Heroku Container Registry. Heroku would use the image to create a container to host your Django project.

### 2. Build Manifest
Or we push the Dockerfile and Heroku would be responsible for building and deploying it in standard release flow.
With the Build Manifest -- we have access to the Pipelines, Review, and Release features which makes it more favorable. 

### Handling PostgreSQL instances
We use different instances of Postgres during the different stages in the workflow:

- During `development`, **Docker** handles setting up a Postgres server
- During `testing` in Travis, we won't be using **Travis's instance** of Postgres, we'll let Docker handle it
- During `deployment`, we have to use **Heroku's instance** of Postgres to make sure data is retained in production

#### Handling data migrations in development

In case you have changes to migrate:
```
$ docker-compose web run python manage.py makemigrations

$ docker-compose web run python manage.py migrate

$ docker-compose up --build
```

#### Handling data migrations in production
```
$ docker-compose -f docker-compose.prod.yml up -d --build

$ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
```

#### Bringing down Dev containers
In case you want to stop containers and remove containers, networks, volumes, and images created by up
Bring down the development containers (and the associated volumes with the -v flag):
```
$ docker-compose down -v
```

#### Building the production image and spin up the containers
```
$ docker-compose -f docker-compose.prod.yml up -d --build
```

#### Bringing down Prod containers
```
$ docker-compose -f docker-compose.prod.yml down -v
```

#### Notes about the Production Dockerfile
- We used a Docker multi-stage build to reduce the final image size. 
- Essentially, builder is a temporary image that's used for building the Python wheels. 
- The wheels are then copied over to the final production image and the builder image is discarded.
**Security Considerations in Production**
- Non-root user is created to avoid running container processes as root inside a contaienr
- We wouldn't want a bad actor to gain root access to the Docker host if they manage to break out of the container

#### Delete all containers and images
```
docker stop $(docker ps -a -q)  # Stop all containers
docker rm $(docker ps -a -q)    # Delete all containers
docker rmi $(docker images -q)  # Delete all images
```

#### Run a command inside the docker image
```
docker-compose run [container_name] [command]
```
For example:
```
docker-compose run web python3 manage.py migrate
```