.PHONY: clean build db migrate static shell superuser run stop cover coverage-html codecov

clean:
		@docker-compose -f docker-compose-dev.yml run --rm web sh -c "find . -name '*.pyc' -delete && find . -name '*.pyo' -delete && rm -f .coverage && rm -rf htmlcov"

build:
		@docker-compose -f docker-compose-dev.yml up --build

db:
		@docker-compose -f docker-compose-dev.yml up -d db

migration: db
		@docker-compose -f docker-compose-dev.yml run --rm web python manage.py makemigrations

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

test:
		@docker-compose -f docker-compose-dev.yml run web sh -c "pytest --cov=./ --cov-report=xml"

coverage: clean
		@docker-compose -f docker-compose-dev.yml run --rm web sh -c "pytest -s -v --cov --cov-report=html:reports/html_dir --cov-report=xml:reports/coverage.xml"

