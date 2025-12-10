
ruff:
	poetry run ruff check ./connectable ./tests


pyrefly:
	poetry run pyrefly check ./connectable ./tests


tests:
	poetry run pytest ./tests -vv ./tests ./connectable \
	--cov ./iter_model --cov-branch --cov-fail-under=100


code-quality-tests: ruff pyrefly tests
