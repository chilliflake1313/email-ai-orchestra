.PHONY: help install test validate check run run-dry clean

help:
	@echo "Email AI Orchestra - Makefile commands"
	@echo ""
	@echo "  make install    - Install dependencies"
	@echo "  make check      - Check environment setup"
	@echo "  make validate   - Validate configuration"
	@echo "  make test       - Run tests"
	@echo "  make run        - Start the application"
	@echo "  make run-dry    - Start in dry-run mode"
	@echo "  make cli        - Run CLI interface"
	@echo "  make clean      - Clean temporary files"

install:
	pip install -r requirements.txt

check:
	python scripts/check_env.py

validate:
	python scripts/validate_config.py

test:
	python tests/run_tests.py

run:
	python app.py

run-dry:
	python app.py --dry-run

cli:
	python cli.py --verbose

cli-dry:
	python cli.py --dry-run --verbose

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -f .coverage
