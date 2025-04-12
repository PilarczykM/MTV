import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes.tests import router as tests_router
from backend.repository.test_csv_repository import TestCSVRepository
from backend.ws.socket import simulate_shared_tests_stream, websocket_endpoint


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run lifespan."""
    simulation_task = asyncio.create_task(simulate_shared_tests_stream())
    app.state.test_repository = TestCSVRepository()
    yield
    simulation_task.cancel()
    try:
        await simulation_task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tests_router)


@app.websocket("/ws/execution")
async def execution(websocket: WebSocket) -> None:
    """Run execution websocket endpoint."""
    await websocket_endpoint(websocket)
