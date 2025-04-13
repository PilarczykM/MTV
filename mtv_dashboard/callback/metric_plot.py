import urllib

import plotly.graph_objects as go
from dash import Input, Output, callback, html
from plotly.basedatatypes import BaseFigure

from mtv_dashboard.utils.consts import API_URL
from mtv_dashboard.utils.data_fetcher import fetch_data_from_api


@callback(
    Output("url", "search", allow_duplicate=True),
    Input("metrics-test-dropdown", "value"),
    Input("metrics-checklist", "value"),
    prevent_initial_call="initial_duplicate",
)
def update_url(test_names: list[str], metrics: list[str]) -> str:
    """Encode selected tests and metrics into URL query string."""
    query = {
        "tests": ",".join(test_names) if test_names else "",
        "metrics": ",".join(metrics) if metrics else "",
    }
    return f"?{urllib.parse.urlencode(query)}"


@callback(
    Output("metrics-test-dropdown", "value"),
    Output("metrics-checklist", "value"),
    Input("url", "search"),
    Input("metrics-test-dropdown", "options"),
)
def sync_inputs_with_url(search: str, test_options: list[dict]) -> tuple[list[str], list[str]]:
    """Decode the query string and update filter components."""
    if not search or not test_options:
        return [], ["Metric 1"]

    parsed = urllib.parse.parse_qs(search.lstrip("?"))
    tests = parsed.get("tests", [""])[0].split(",") if parsed.get("tests") else []
    metrics = parsed.get("metrics", [""])[0].split(",") if parsed.get("metrics") else []
    return tests, metrics


@callback(
    Output("metrics-test-dropdown", "options"),
    Input("metrics-checklist", "id"),
)
def populate_metric_test_dropdown(_) -> dict:  # noqa: ANN001
    """Populate metrics tests into dropdown."""
    df = fetch_data_from_api(API_URL)
    unique_names = df["test_name"].dropna().unique()
    return [{"label": name, "value": name} for name in sorted(unique_names)]


@callback(
    Output("metrics-plot", "figure"),
    Output("metrics-diff-info", "children"),
    Input("metrics-test-dropdown", "value"),
    Input("metrics-checklist", "value"),
)
def update_metrics_plot(selected_tests: list[str], selected_metrics: list[str]) -> BaseFigure:
    """Update metrics plot for selected tests and metrics."""
    if not selected_tests or not selected_metrics:
        return go.Figure(), ""

    df = fetch_data_from_api(API_URL)
    test_id_map = df[["test_name", "test_id"]].drop_duplicates().set_index("test_name")["test_id"].to_dict()
    selected_ids = [test_id_map.get(t) for t in selected_tests]
    filtered = df[df["test_id"].isin(selected_ids)]

    fig = go.Figure()
    reference = None
    diff_info = []

    for metric in selected_metrics:
        for i, test in enumerate(selected_tests):
            test_id = test_id_map.get(test)
            val = filtered.loc[filtered["test_id"] == test_id, metric].mean()

            fig.add_trace(
                go.Bar(
                    x=[metric],
                    y=[val],
                    name=test,
                    offsetgroup=test,
                ),
            )

            if i == 0:
                reference = val
            else:
                diff = ((val - reference) / reference) * 100 if reference else 0
                color = "green" if diff > 0 else "red" if diff < 0 else "black"
                diff_info.append(
                    html.Div(
                        f"{test} vs {selected_tests[0]} ({metric}): {diff:+.1f}%",
                        style={"color": color, "fontWeight": "bold"},
                    ),
                )

    fig.update_layout(
        barmode="group",
        title="Metrics Comparison",
        yaxis_title="Metric Value",
        template="plotly_white",
    )

    return fig, diff_info
