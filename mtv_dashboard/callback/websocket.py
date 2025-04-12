import json

import dash
import plotly.graph_objs as go
from dash import MATCH, Input, Output, State, callback


@callback(
    Output("live-data-store", "data"),
    Input("ws", "message"),
    State("live-data-store", "data"),
    prevent_initial_call=True,
)
def store_ws_data(message, current_data):
    payload = json.loads(message["data"])
    if current_data is None:
        current_data = {}

    for test in payload:
        test_id = test["test_id"]
        time = test["time_start"]

        if test_id not in current_data:
            current_data[test_id] = {}

        for trace_name, value in test["traces"].items():
            if trace_name not in current_data[test_id]:
                current_data[test_id][trace_name] = {"x": [], "y": []}

            current_data[test_id][trace_name]["x"].append(time)
            current_data[test_id][trace_name]["y"].append(value)

        for metric_name, value in test["metrics"].items():
            if metric_name not in current_data[test_id]:
                current_data[test_id][metric_name] = {"x": [], "y": []}

            current_data[test_id][metric_name]["x"].append(time)
            current_data[test_id][metric_name]["y"].append(value)

    return current_data


@callback(
    Output({"type": "live-graph", "index": MATCH}, "figure"),
    Input("live-data-store", "data"),
    Input({"type": "graph-filter", "index": MATCH}, "value"),
    State({"type": "live-graph", "index": MATCH}, "id"),
    prevent_initial_call=True,
)
def update_graph_filtered(data, selected_filter, graph_id):
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

    fig.update_layout(title=test_id)
    return fig
