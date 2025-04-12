import json

import dash
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
    Output({"type": "live-graph", "index": MATCH}, "extendData"),
    Input("live-data-store", "data"),
    State({"type": "live-graph", "index": MATCH}, "id"),
    State({"type": "live-graph", "index": MATCH}, "figure"),
    prevent_initial_call=True,
)
def update_graph_extend(data, graph_id, existing_figure):
    test_id = graph_id["index"]

    if not data or test_id not in data or not existing_figure or "data" not in existing_figure:
        return dash.no_update

    figures_data = data[test_id]

    extend = {"x": [], "y": []}
    for figure in existing_figure["data"]:
        name = figure["name"]
        new_x = [figures_data[name]["x"][-1]]
        new_y = [figures_data[name]["y"][-1]]
        extend["x"].append(new_x)
        extend["y"].append(new_y)

    return extend
