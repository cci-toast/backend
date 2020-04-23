# CI/CD with Docker, Github Actions and DigitalOcean
- `docker-comopose-ci.yml` co-ordinates the prod environment with caching to reduce the image size
- `main.yml` dictates the Github action workflow for handling merging to master and deployment to DigitalOcean
- The relevant  environment variables are handled by Github secrets

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