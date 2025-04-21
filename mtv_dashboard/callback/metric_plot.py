import urllib.parse
from json import JSONDecodeError

import plotly.graph_objects as go
import requests
from dash import Input, Output, State, callback, dash, html
from dash.exceptions import PreventUpdate
from fastapi.responses import JSONResponse
from plotly.basedatatypes import BaseFigure

from mtv_dashboard.utils.consts import API_STATE_URL, API_TESTS_URL
from mtv_dashboard.utils.data_fetcher import fetch_data_from_api


@callback(
    Output("dashboard-state", "data"),
    Input("metrics-test-dropdown", "value"),
    Input("metrics-checklist", "value"),
)
def update_dashboard_state(test_names: list[str], metrics: list[str]) -> dict:
    """Update dashboard state."""
    return {
        "source": "metrics",
        "tests": test_names,
        "metrics": metrics,
    }


@callback(
    Output("url", "search", allow_duplicate=True),
    Output("copy-confirmation", "children"),
    Input("copy-url-button", "n_clicks"),
    State("dashboard-state", "data"),
    prevent_initial_call=True,
)
def copy_shareable_link(n_clicks: int, state: dict) -> tuple[str, str]:  # noqa: ARG001
    """Copy sharable link."""
    try:
        response = requests.post(API_STATE_URL, json=state, timeout=1000)
        response.raise_for_status()
        hash_ = response.json()["state_hash"]
        url = f"?state={hash_}"
    except requests.HTTPError as e:
        return "", f"❌ Error: {e!s}"

    return url, "✅ Link copied!"


@callback(
    Output("dashboard-state", "data", allow_duplicate=True),
    Input("url", "search"),
    prevent_initial_call=True,
)
def load_state_from_url(search: str) -> JSONResponse:
    """Load state from url."""
    if not search or not search.startswith("?state="):
        raise PreventUpdate

    hash_ = urllib.parse.parse_qs(search.lstrip("?")).get("state", [""])[0]
    if not hash_:
        raise PreventUpdate

    try:
        response = requests.get(f"{API_STATE_URL}/{hash_}", timeout=1000)
        response.raise_for_status()
        return response.json()
    except (requests.HTTPError, JSONDecodeError):
        return dash.no_update


@callback(
    Output("metrics-test-dropdown", "value"),
    Output("metrics-checklist", "value"),
    Output("state-loaded", "data"),
    Input("metrics-test-dropdown", "options"),
    State("dashboard-state", "data"),
    State("state-loaded", "data"),
)
def apply_loaded_state(options: list[dict], state: dict, already_loaded: bool) -> list:  # noqa: FBT001
    """Apply loaded state."""
    if not options or not state or already_loaded:
        raise PreventUpdate

    if state.get("source") != "metrics":
        raise PreventUpdate

    allowed = {opt["value"] for opt in options}
    valid_tests = [t for t in state.get("tests", []) if t in allowed]
    return valid_tests, state.get("metrics", []), True


@callback(
    Output("metrics-test-dropdown", "options"),
    Input("metrics-checklist", "id"),
)
def populate_metric_test_dropdown(_) -> list[dict]:  # noqa: ANN001
    """Populate metrics tests into dropdown."""
    df = fetch_data_from_api(API_TESTS_URL)
    unique_names = df["test_name"].dropna().unique()
    return [{"label": name, "value": name} for name in sorted(unique_names)]


@callback(
    Output("metrics-plot", "figure"),
    Output("metrics-diff-info", "children"),
    Input("metrics-test-dropdown", "value"),
    Input("metrics-checklist", "value"),
)
def update_metrics_plot(selected_tests: list[str], selected_metrics: list[str]) -> tuple[BaseFigure, str]:
    """Update metrics plot for selected tests and metrics."""
    if not selected_tests or not selected_metrics:
        return go.Figure(), ""

    df = fetch_data_from_api(API_TESTS_URL)
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
