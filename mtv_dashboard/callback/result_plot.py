import plotly.graph_objects as go
from dash import callback, Output, Input, State, dcc, html, dash_table

from mtv_dashboard.utils.consts import API_URL
from mtv_dashboard.utils.data_fetcher import fetch_data_from_api
import pandas as pd

@callback(
    Output("selected-tests-plot-container", "children"),
    Input("summary-table", "derived_virtual_selected_rows"),
    State("summary-table", "derived_virtual_data"), # !derived_virtual_data makes sure that data received is correctly shrink on filter mode.
)
def display_selected_tests(selected_rows: list[int], visible_data: list[dict]) -> list:
    """Render trace plots and metrics for selected tests."""
    if not selected_rows or not visible_data:
        return []

    selected_ids = [visible_data[i]["test_id"] for i in selected_rows]

    df = fetch_data_from_api(API_URL)
    df = df.rename(columns=str.lower)
    filtered_df = df[df["test_id"].isin(selected_ids)]

    trace_cols = [col for col in df.columns if col.startswith("trace")]
    metric_cols = [col for col in df.columns if col.startswith("metric")]

    plots = []

    for test_id in selected_ids:
        test_data = filtered_df[filtered_df["test_id"] == test_id]

        if test_data.empty:
            continue

        test_name = test_data["test_name"].iloc[0]
        fig = go.Figure()

        for trace in trace_cols:
            if trace not in test_data:
                continue
            fig.add_trace(
                go.Scatter(
                    x=test_data["time_start"],
                    y=test_data[trace],
                    mode="lines",
                    name=trace,
                    hovertemplate=(
                        f"{trace}<br>Time: %{{x}}<br>Value: %{{y:.2f}}<extra></extra>"
                    ),
                )
            )

        fig.update_layout(
            title=f"Traces for {test_name}",
            xaxis_title="Time [s]",
            yaxis_title="Value",
            template="plotly_white",
            height=400,
        )

        metric_row = test_data.iloc[0][metric_cols]
        metric_table = dash_table.DataTable(
            columns=[{"name": "Metric", "id": "Metric"}, {"name": "Value", "id": "Value"}],
            data=[
                {"Metric": metric, "Value": f"{value:.2f}"}
                for metric, value in metric_row.items()
                if pd.notna(value)
            ],
            style_table={"width": "300px"},
            style_cell={
                "textAlign": "left",
                "padding": "4px",
                "fontFamily": "Arial",
                "fontSize": "13px",
            },
            style_header={
                "backgroundColor": "#f9f9f9",
                "fontWeight": "bold",
            },
        )

        plots.append(
            html.Div([
                dcc.Graph(figure=fig),
                html.H5(f"Metrics for {test_name}"),
                metric_table,
                html.Hr()
            ])
        )

    return plots

