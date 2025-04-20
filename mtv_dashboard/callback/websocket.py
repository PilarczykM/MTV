import json

import dash
import plotly.graph_objs as go
from dash import MATCH, Input, Output, State, callback

from mtv_dashboard.types import Data

# Rolling window size - number of points to keep per series
ROLLING_WINDOW = 15


def append_with_rolling(
    data_dict: dict,
    series_name: str,
    time: int,
    value: int,
    max_len: int = ROLLING_WINDOW,
) -> None:
    """Append data point and enforce rolling window limit."""
    if series_name not in data_dict:
        data_dict[series_name] = {"x": [], "y": []}
    series = data_dict[series_name]
    series["x"].append(time)
    series["y"].append(value)
    if len(series["x"]) > max_len:
        series["x"] = series["x"][-max_len:]
        series["y"] = series["y"][-max_len:]


@callback(
    Output("live-data-store", "data"),
    Input("ws", "message"),
    State("live-data-store", "data"),
    prevent_initial_call=True,
)
def store_ws_data(message: dict, current_data: Data) -> Data:
    """Store websocket data with rolling window."""
    payload = json.loads(message["data"])
    if current_data is None:
        current_data = {}

    for test in payload:
        test_id = test["test_id"]
        time = test["time_start"]

        if test_id not in current_data:
            current_data[test_id] = {}

        for trace_name, value in test["traces"].items():
            append_with_rolling(current_data[test_id], trace_name, time, value)

        for metric_name, value in test["metrics"].items():
            append_with_rolling(current_data[test_id], metric_name, time, value)

    return current_data


@callback(
    Output({"type": "live-graph", "index": MATCH}, "figure"),
    Input("live-data-store", "data"),
    Input({"type": "graph-filter", "index": MATCH}, "value"),
    State({"type": "live-graph", "index": MATCH}, "id"),
    prevent_initial_call=True,
)
def apply_filter_to_figure(data: Data, selected_filter: str, graph_id: str) -> go.Figure:
    """Apply filter to figure."""
    test_id = graph_id["index"]

    if not data or test_id not in data:
        return dash.no_update

    figures_data = data[test_id]
    fig = go.Figure()

    for name, trace in figures_data.items():
        if selected_filter == "trace" and not name.startswith("Trace"):
            continue
        if selected_filter == "metric" and not name.startswith("Metric"):
            continue

        fig.add_trace(go.Scatter(x=trace["x"], y=trace["y"], mode="lines", name=name))

    fig.update_layout(
        title=test_id,
        margin={"l": 40, "r": 20, "t": 40, "b": 40},
        uirevision=test_id,
    )
    return fig
