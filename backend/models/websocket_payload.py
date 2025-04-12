from pydantic import BaseModel, Field


class WebSocketPayload(BaseModel):
    """Represent a single payload of simulated test data for WebSocket communication."""

    test_id: str
    test_name: str
    test_type: str
    test_param_1: float
    test_param_2: float
    test_param_3: float
    time_start: int = Field(..., description="Time start.")
    traces: dict[str, float] = Field(..., description="Trace 1 - Trace 10 values.")
    metrics: dict[str, float] = Field(..., description="Metric 1 - Metric 6 values.")
