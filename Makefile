.PHONY: clean build db migrate static shell superuser run stop

clean:
		@docker-compose -f docker-compose-dev.yml run --rm web sh -c "find . -name '*.pyc' -delete && find . -name '*.pyo' -delete && rm -f .coverage && rm -rf htmlcov"

build:
		@docker-compose -f docker-compose-dev.yml build

db:
		@docker-compose -f docker-compose-dev.yml up -d db

migrate: db
		@docker-compose -f docker-compose-dev.yml run --rm web python manage.py migrate

static: db
		@docker-compose -f docker-compose-dev.yml run --rm web python manage.py collectstatic --noinput

shell: db
		@docker-compose -f docker-compose-dev.yml run --rm web python manage.py shell

superuser: db
		@docker-compose -f docker-compose-dev.yml run --rm web python manage.py createsuperuser

run: migrate static
		@docker-compose -f docker-compose-dev.yml up -d

stop:
	    @docker-compose -f docker-compose-dev.yml stop

remove:
		@docker-compose -f docker-compose-dev.yml rm

test: clean
		@docker-compose -f docker-compose-dev.yml run --rm web sh -c "pytest --cov"