migrate:
	docker compose exec web alembic upgrade head

makemigrations:
	docker compose exec web alembic revision --autogenerate -m "$(m)"
