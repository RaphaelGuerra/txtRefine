.PHONY: help install test lint format clean build

# Default target
help:
	@echo "Available commands:"
	@echo "  install     Install dependencies"
	@echo "  test        Run tests"
	@echo "  lint        Run linter"
	@echo "  format      Format code"
	@echo "  clean       Clean build artifacts"
	@echo "  build       Build package"
	@echo "  dev         Install in development mode"

# Install dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov black isort flake8 mypy

# Run tests
test:
	pytest tests/ -v

# Run tests with coverage
test-cov:
	pytest tests/ -v --cov=refine --cov-report=html --cov-report=term-missing

# Run linter
lint:
	flake8 refine.py tests/
	mypy refine.py

# Format code
format:
	black refine.py tests/
	isort refine.py tests/

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -type d -name __pycache__ -exec rm -rf {} +

# Build package
build:
	python -m build

# Run the application
run:
	python refine.py

# Quick test with sample file
test-run:
	@echo "Testing with sample file..."
	@if [ -f "input/test_sample.txt" ]; then \
		python refine.py --input input/test_sample.txt --output output/test_refined.txt --model llama3.2:latest; \
	else \
		echo "Sample file not found. Creating test file..."; \
		mkdir -p input; \
		echo "Este é um teste de refinamento de texto." > input/test_sample.txt; \
		python refine.py --input input/test_sample.txt --output output/test_refined.txt --model llama3.2:latest; \
	fi
