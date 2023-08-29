# recipe-app-api-
Recipe API Project

Commands to run

`docker-compose run --rm api sh -c "python manage.py collectstatic"`

`docker-compose run --rm api sh -c "python manage.py test && flake8"`
