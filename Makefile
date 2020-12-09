init-data:
	python src/flex/db/initial_data.py

migrate:
	alembic upgrade head


generate-migrations:
	alembic revision --autogenerate


clean-migrations:
	-rm -f ./src/alembic/versions/*


format:
	./scripts/format.sh

lint:
	 ./scripts/lint.sh

