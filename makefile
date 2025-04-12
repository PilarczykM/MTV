lint:
	uv run -- ruff check .

dev:
	uv run mtv_dashboard/main.py

server:
	uv run uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000