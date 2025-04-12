import plotly.graph_objs as go
from dash import dcc, html
from dash_extensions import WebSocket


def home_layout():
    test_ids = [f"T-LIVE-{i+1:03}" for i in range(5)]
    trace_names = [f"Trace {i}" for i in range(1, 11)]

    return html.Div([
        dcc.Store(id="live-data-store"),
        WebSocket(id="ws", url="ws://127.0.0.1:8000/ws/execution"),
        html.H2("Live execution"),
        html.Div([
            html.Div([
                html.H4(test_id),
                dcc.Graph(
                    id={"type": "live-graph", "index": test_id},
                    figure=go.Figure([
                        go.Scatter(x=[], y=[], mode="lines", name=trace_name)
                        for trace_name in trace_names
                    ]),
                    config={"displayModeBar": False},
                ),
            ], className="chart-box") for test_id in test_ids
        ], id="charts-container"),
    ], id="charts")
