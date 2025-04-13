import plotly.graph_objects as go
from dash import Input, Output, callback
from plotly.basedatatypes import BaseFigure

from mtv_dashboard.utils.data_fetcher import fetch_data_from_api
import pandas as pd
API_URL = "http://localhost:8000/tests"


@callback(
    Output("test-name-dropdown", "options"),
    Input("trace-checklist", "id"),
)
def populate_test_name_dropdown(_):
    """Populate the Test Name dropdown with available test names."""
    df = fetch_data_from_api(API_URL)
    unique_test_names = df["test_name"].dropna().unique()
    return [{"label": name, "value": name} for name in sorted(unique_test_names)]


@callback(
    Output("trace-plot", "figure"),
    Input("test-name-dropdown", "value"),
    Input("trace-checklist", "value"),
)
def update_trace_plot(selected_test_names, selected_traces) -> BaseFigure:
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
                        name=f"{test_name} – {trace}",
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
        title="Trace signals over time", xaxis_title="Time [s]", yaxis_title="Value", template="plotly_white",
    )

    return fig
