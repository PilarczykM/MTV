from dash import dcc, html
from dash_extensions import WebSocket

from mtv_dashboard.layout.base import create_base_layout


def home_layout() -> html.Div:
    """Render home layout."""
    test_ids = [f"T-LIVE-{i + 1:03}" for i in range(5)]

    return create_base_layout(
        content=html.Div(
            [
                dcc.Store(id="live-data-store"),
                WebSocket(id="ws", url="ws://127.0.0.1:8000/ws/execution"),
                html.H2("Live execution"),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Fieldset(
                                    [
                                        html.Legend("Select data type:"),
                                        dcc.RadioItems(
                                            id={"type": "graph-filter", "index": test_id},
                                            options=[
                                                {"label": "All", "value": "all"},
                                                {"label": "Traces", "value": "trace"},
                                                {"label": "Metrics", "value": "metric"},
                                            ],
                                            value="all",
                                            inline=True,
                                            className="radio-filter",
                                        ),
                                    ],
                                    className="graph-filter-fieldset",
                                ),
                                dcc.Graph(
                                    id={"type": "live-graph", "index": test_id},
                                    config={"displayModeBar": False},
                                ),
                            ],
                            className="chart-box",
                        )
                        for test_id in test_ids
                    ],
                    id="charts-container",
                ),
            ],
            id="charts",
        ),
    )
