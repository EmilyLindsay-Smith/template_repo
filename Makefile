sync:
	uv sync

install:
	uv run pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push

lint:
	uv run pre-commit run --all-files

format:
	uv run ruff format .

audit:
	uv audit --preview-features audit

typecheck:
	@if find src -type f -name "*.py" 2>/dev/null | grep -q .; then \
		uv run mypy; \
	else \
		echo "No Python source files found; skipping mypy."; \
	fi

test:
	@if find tests -type f -name "test_*.py" 2>/dev/null | grep -q .; then \
		uv run pytest --cov=src --cov-report=term-missing; \
	else \
		echo "No tests found; skipping."; \
	fi

check: lint typecheck test

clean:
	rm -rf \
		.ruff_cache \
		.mypy_cache \
		.pytest_cache \
		htmlcov \
		.coverage \
		build \
		dist \
		*.egg-info\

bootstrap:
	sync install check

pyrefly:
	uv run pyrefly check --summarize-errors

help:
	@echo "Available targets:"
	@echo "  bootstrap  - Create development environment and run checks"
	@echo "  sync       - Synchronise the uv environment"
	@echo "  install    - Install pre-commit hooks"
	@echo "  lint       - Run pre-commit hooks"
	@echo "  format     - Format code with Ruff"
	@echo "  typecheck  - Run mypy (if source exists)"
	@echo "  test       - Run pytest (if tests exist)"
	@echo "  check      - Run lint, typecheck and tests"
	@echo "  clean      - Remove generated files"
