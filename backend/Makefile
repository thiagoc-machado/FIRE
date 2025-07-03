run:
	docker-compose up --build

makemigrations:
	docker-compose exec backend python manage.py makemigrations

migrate:
	docker-compose exec backend python manage.py migrate

createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

test:
	docker-compose exec backend pytest
