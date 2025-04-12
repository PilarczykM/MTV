import asyncio
import random

from fastapi import WebSocket, WebSocketDisconnect

from backend.models.test_dto import TestDto

connected_clients: set[WebSocket] = set()
last_payloads: list[TestDto] = []


async def register_client(websocket: WebSocket) -> None:
    """Register client into memory store."""
    await websocket.accept()
    connected_clients.add(websocket)

    await websocket.send_json([payload.model_dump() for payload in last_payloads])


def unregister_client(websocket: WebSocket) -> None:
    """Unregister the client from memory store."""
    connected_clients.discard(websocket)


async def broadcast(payloads: list[TestDto]) -> None:
    """Send the given payload to all connected clients and remove any disconnected."""
    disconnected = []

    for client in connected_clients:
        try:
            await client.send_json([p.model_dump() for p in payloads])
        except WebSocketDisconnect:
            disconnected.append(client)
        except Exception as e:
            print(f"Unexpected error while sending to client: {e}")
            disconnected.append(client)

    for client in disconnected:
        unregister_client(client)


async def websocket_endpoint(websocket: WebSocket) -> None:
    """Handle incoming WebSocket connection and stream the shared data."""
    await register_client(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        unregister_client(websocket)


async def simulate_shared_tests_stream() -> None:
    """
    Simulate 5 shared test streams and broadcast their data every second.

    Each test is updated independently but sent together in a single loop.
    """
    global last_payloads  # noqa: PLW0603, can be fixed by creating additional class to update / get last_payload

    num_tests = 5
    time_counters = [0 for _ in range(num_tests)]
    test_ids = [f"T-LIVE-{i + 1:03}" for i in range(num_tests)]

    test_metadata = {
        test_ids[i]: {
            "test_name": f"Live Test {i + 1}",
            "test_type": "Shared",
            "test_param_1": f"Param{round(random.uniform(0.1, 1.0), 2)}",
            "test_param_2": f"Param{round(random.uniform(0.1, 1.0), 2)}",
            "test_param_3": f"Param{round(random.uniform(0.1, 1.0), 2)}",
        }
        for i in range(num_tests)
    }

    while True:
        payloads = []

        for i in range(num_tests):
            test_id = test_ids[i]
            meta = test_metadata[test_id]

            traces = {f"Trace {j}": random.uniform(0.0, 1.0) for j in range(1, 11)}
            metrics = {f"Metric {j}": random.uniform(0.0, 1.0) for j in range(1, 7)}

            payload = TestDto(
                test_id=test_id,
                test_name=meta["test_name"],
                test_type=meta["test_type"],
                test_param_1=meta["test_param_1"],
                test_param_2=meta["test_param_2"],
                test_param_3=meta["test_param_3"],
                time_start=time_counters[i],
                traces=traces,
                metrics=metrics,
            )

            payloads.append(payload)
            time_counters[i] += 1

        last_payloads = payloads
        await broadcast(payloads)
        await asyncio.sleep(1)
