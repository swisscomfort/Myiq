.PHONY: help build test lint clean format install-dev docs

help:
	@echo "Crypto Recovery Toolkit - Development Commands"
	@echo ""
	@echo "Installation:"
	@echo "  make install-dev      Install development dependencies"
	@echo ""
	@echo "Building:"
	@echo "  make build            Build Rust scanner (release)"
	@echo "  make build-debug      Build Rust scanner (debug)"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make lint             Run all linters (pylint, shellcheck, cargo clippy)"
	@echo "  make format           Format Python and Rust code"
	@echo "  make test             Run Python tests"
	@echo "  make test-shell       Validate shell scripts"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove build artifacts and caches"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs             Generate documentation"

install-dev:
	@echo "Installing development dependencies..."
	pip3 install pylint black pytest shellcheck-py
	@echo "✓ Development tools installed"

build:
	@echo "Building Rust scanner (release)..."
	cd A_rustscanner && cargo build --release
	@echo "✓ Build complete: A_rustscanner/target/release/rustscanner"

build-debug:
	@echo "Building Rust scanner (debug)..."
	cd A_rustscanner && cargo build
	@echo "✓ Build complete: A_rustscanner/target/debug/rustscanner"

lint:
	@echo "Linting Python files..."
	pylint tools/**/*.py || true
	@echo "✓ Python linting complete"
	@echo ""
	@echo "Validating shell scripts..."
	shellcheck scripts/*.sh start.sh || true
	@echo "✓ Shell validation complete"
	@echo ""
	@echo "Checking Rust code..."
	cd A_rustscanner && cargo clippy -- -D warnings || true
	@echo "✓ Rust clippy check complete"

format:
	@echo "Formatting Python code..."
	black tools/ || true
	@echo "✓ Python formatting complete"
	@echo ""
	@echo "Formatting Rust code..."
	cd A_rustscanner && cargo fmt
	@echo "✓ Rust formatting complete"

test:
	@echo "Running Python tests..."
	python3 -m pytest tests/ -v || true

test-shell:
	@echo "Validating shell scripts..."
	for script in scripts/*.sh start.sh; do \
		echo "Checking $$script..."; \
		bash -n "$$script" || exit 1; \
	done
	@echo "✓ All shell scripts valid"

clean:
	@echo "Cleaning build artifacts..."
	cd A_rustscanner && cargo clean
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ *.egg-info
	@echo "✓ Cleanup complete"

docs:
	@echo "Documentation is in docs/ directory"
	@echo "Training materials are in training/ directory"
	@echo "Use 'scripts/generate_training_pdf.sh' for PDF generation"
