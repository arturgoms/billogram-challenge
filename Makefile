lint:
	pylint -E --django-settings-module=settings.test src/

test:
	python src/manage.py test apps --settings=settings.test --verbosity=2 --noinput

run-dev:
	python src/manage.py runserver --settings=settings.development

coverage:
	coverage run --source='.' src/manage.py test apps --settings=settings.test
	coverage report

coverage-html:
	coverage html

shell:
	poetry shell

install-dependencies:
	poetry install

k8s-create-secret:
	kubectl create secret generic polls-secret --from-env-file=.env

helm-deploy:
	helm upgrade --install django-app ./helm/django-app

migrate:
	python src/manage.py migrate

make-migrations:
	python src/manage.py makemigrations

black:
	poetry run black .