
ruff:
	poetry run ruff check ./connected ./tests


pyrefly:
	poetry run pyrefly check ./connected ./tests


tests:
	poetry run pytest ./tests -vv ./tests ./connected \
	--cov ./iter_model --cov-branch --cov-fail-under=100


code-quality-tests: ruff pyrefly tests
