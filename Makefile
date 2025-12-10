
ruff:
	poetry run ruff check ./aconnection ./tests


pyrefly:
	poetry run pyrefly check ./aconnection ./tests


tests:
	poetry run pytest ./tests -vv ./tests ./aconnection \
	--cov ./iter_model --cov-branch --cov-fail-under=100


code-quality-tests: ruff pyrefly tests
