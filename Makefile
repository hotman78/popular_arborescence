.PHONY: run test fmt lint type-check web
run:
	uv run src/solve.py
test:
	uvx pytest .
fmt:
	uvx ruff format .
lint:
	uvx ruff check . --fix
type-check:
	uvx mypy .
app:
	uvx streamlit run src/app.py