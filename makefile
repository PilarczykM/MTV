lint:
	uv run -- ruff check .

frontend:
	uv run -m mtv_dashboard.main

server:
	uv run uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

dev:
	( make server & make frontend & wait )