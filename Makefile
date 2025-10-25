.PHONY: help test test-scanner test-gui test-coverage test-shell lint clean format install-dev docs

help:
	@echo "Crypto Recovery Toolkit - Development Commands"
	@echo ""
	@echo "Installation:"
	@echo "  make install-dev      Install development dependencies"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test             Run all Python tests"
	@echo "  make test-scanner     Run scanner tests only"
	@echo "  make test-gui         Run GUI tests only"
	@echo "  make test-coverage    Run tests with coverage report"
	@echo "  make test-shell       Validate shell scripts"
	@echo "  make lint             Run all linters"
	@echo "  make format           Format Python code"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove build artifacts and caches"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs             Generate documentation"

install-dev:
	@echo "Installing development dependencies..."
	pip3 install pylint black pytest pytest-cov shellcheck-py
	@echo "✓ Development tools installed"

test:
	@echo "Running all Python tests..."
	python3 -m unittest discover tests/ -v
	@echo "✓ All tests passed"

test-scanner:
	@echo "Running scanner tests..."
	python3 tests/test_scanner.py -v

test-gui:
	@echo "Running GUI tests..."
	python3 tests/test_gui.py -v

test-coverage:
	@echo "Running tests with coverage..."
	@which pytest > /dev/null || (echo "pytest not installed. Run: pip3 install pytest pytest-cov" && exit 1)
	python3 -m pytest tests/ -v --cov=tools --cov-report=term --cov-report=html
	@echo "✓ Coverage report generated in htmlcov/"

test-shell:
	@echo "Validating shell scripts..."
	for script in scripts/*.sh start.sh; do \
		echo "Checking $$script..."; \
		bash -n "$$script" || exit 1; \
	done
	@echo "✓ All shell scripts valid"

lint:
	@echo "Linting Python files..."
	pylint tools/**/*.py tests/**/*.py || true
	@echo "✓ Python linting complete"
	@echo ""
	@echo "Validating shell scripts..."
	shellcheck scripts/*.sh start.sh || true
	@echo "✓ Shell validation complete"

format:
	@echo "Formatting Python code..."
	black tools/ tests/ || true
	@echo "✓ Python formatting complete"

clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ *.egg-info
	@echo "✓ Cleanup complete"

# Benchmarks
benchmark:
	@echo "Running scanner performance benchmark..."
	python3 tests/benchmark_scanner.py --files 100 --iterations 3

benchmark-stress:
	@echo "Running stress test benchmark (this may take a while)..."
	python3 tests/benchmark_scanner.py --files 1000 --iterations 5

benchmark-large-files:
	@echo "Running large file benchmark..."
	python3 tests/benchmark_scanner.py --files 50 --size 1048576 --iterations 3

docs:
	@echo "Documentation is in docs/ directory"
	@echo "Training materials are in training/ directory"
	@echo "Use 'scripts/generate_training_pdf.sh' for PDF generation"

