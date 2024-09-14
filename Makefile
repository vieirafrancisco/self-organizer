run:
	poetry run flask --app app --debug run

test:
	poetry run pytest app/

lint:
	poetry run ruff check --fix

shell:
	poetry run flask --app app shell
