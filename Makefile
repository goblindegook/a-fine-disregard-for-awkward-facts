format:
	poetry run isort disregard tests
	poetry run black disregard tests

lint:
	poetry run black --check disregard tests
	poetry run mypy disregard tests

test:
	poetry run pytest

watch:
	poetry run ptw