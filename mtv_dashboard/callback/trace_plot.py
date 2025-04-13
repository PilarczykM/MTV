import urllib

import plotly.graph_objects as go
from dash import Input, Output, State, callback, ClientsideFunction
from plotly.basedatatypes import BaseFigure

from mtv_dashboard.utils.data_fetcher import fetch_data_from_api

API_URL = "http://localhost:8000/tests"


@callback(
    Output("url", "search", allow_duplicate=True),
    Input("test-name-dropdown", "value"),
    Input("trace-checklist", "value"),
    prevent_initial_call="initial_duplicate",
)
def update_url(test_names: list[str], traces: list[str]) -> str:
    """Encode the selected filters into the URL query string."""
    query = {
        "tests": ",".join(test_names) if test_names else "",
        "traces": ",".join(traces) if traces else "",
    }
    return f"?{urllib.parse.urlencode(query)}"

@callback(
    Output("test-name-dropdown", "value"),
    Output("trace-checklist", "value"),
    Input("url", "search"),
    Input("test-name-dropdown", "options"),
)
def sync_inputs_with_url(search: str, test_options: list[dict]) -> tuple[list[str], list[str]]:
    """Decode the query string and update the filter components."""
    if not search or not test_options:
        return [], ["Trace 1"]

    parsed = urllib.parse.parse_qs(search.lstrip("?"))
    tests = parsed.get("tests", [""])[0].split(",") if parsed.get("tests") else []
    traces = parsed.get("traces", [""])[0].split(",") if parsed.get("traces") else []
    return tests, traces


@callback(
    Output("test-name-dropdown", "options"),
    Input("trace-checklist", "id"),
)
def populate_test_name_dropdown(_) -> list[dict[str, str]]:  # noqa: ANN001
    """Populate the Test Name dropdown with available test names."""
    df = fetch_data_from_api(API_URL)
    unique_test_names = df["test_name"].dropna().unique()
    return [{"label": name, "value": name} for name in sorted(unique_test_names)]


@callback(
    Output("trace-plot", "figure"),
    Input("test-name-dropdown", "value"),
    Input("trace-checklist", "value"),
)
def update_trace_plot(selected_test_names: list[str], selected_traces: list[str]) -> BaseFigure:
    """Update the trace plot based on selected test names and trace signals."""
    if not selected_test_names or not selected_traces:
        return go.Figure()

    df = fetch_data_from_api(API_URL)

    # Build mapping: test_name -> test_id
    test_name_to_id = df[["test_name", "test_id"]].drop_duplicates().set_index("test_name")["test_id"].to_dict()

    selected_test_ids = [test_name_to_id.get(name) for name in selected_test_names if name in test_name_to_id]
    filtered_df = df[df["test_id"].isin(selected_test_ids)]

    fig = go.Figure()

    for trace in selected_traces:
        for test_name in selected_test_names:
            test_id = test_name_to_id.get(test_name)
            test_data = filtered_df[filtered_df["test_id"] == test_id]

            if trace in test_data.columns:
                values = test_data[trace]
                time = test_data["time_start"]

                stats = {"avg": values.mean(), "std": values.std(), "min": values.min(), "max": values.max()}

                fig.add_trace(
                    go.Scatter(
                        x=time,
                        y=values,
                        mode="lines",
                        name=f"{test_name} - {trace}",
                        hovertemplate=(
                            "Time: %{x}<br>"
                            "Value: %{y:.2f}<br>"
                            f"Avg: {stats['avg']:.2f}<br>"
                            f"Std: {stats['std']:.2f}<br>"
                            f"Min: {stats['min']:.2f}<br>"
                            f"Max: {stats['max']:.2f}<extra></extra>"
                        ),
                    ),
                )

    fig.update_layout(
        title="Trace signals over time",
        xaxis_title="Time [s]",
        yaxis_title="Value",
        template="plotly_white",
    )

    return fig

def register_clientside_callbacks(app):
    app.clientside_callback(
        ClientsideFunction(namespace="clipboard", function_name="copyUrlToClipboard"),
        Output("copy-confirmation", "children"),
        Input("copy-url-button", "n_clicks"),
        prevent_initial_call=True
    )