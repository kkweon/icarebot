test:
	pytest --pylint --mypy --cov=icarebot --doctest-modules

format:
	isort -y
	black icarebot


dep:
	pip install -r requirements.txt
