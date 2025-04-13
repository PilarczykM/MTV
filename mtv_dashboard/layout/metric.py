from dash import dcc, html

from mtv_dashboard.components.share_link import share_link
from mtv_dashboard.layout.base import create_base_layout


def metrics_layout() -> html.Div:
    """Return metrics layout."""
    content = html.Div(
        [
            dcc.Location(id="url", refresh=False),
            html.Div(
                [
                    html.H2("Metrics Comparison Page"),
                    share_link()
                ],
                style={"display": "flex", "gap": "20px"},
            ),
            html.Div(
                [
                    html.Label("Select tests:"),
                    dcc.Dropdown(
                        id="metrics-test-dropdown",
                        options=[],  # Populated dynamically
                        multi=True,
                        placeholder="Select tests",
                    ),
                ],
                style={"marginBottom": "20px"},
            ),

            html.Div(
                [
                    html.Label("Select Metrics:"),
                    dcc.Checklist(
                        id="metrics-checklist",
                        options=[{"label": f"Metric {i}", "value": f"Metric {i}"} for i in range(1, 6)],
                        value=["Metric 1"],
                        labelStyle={"display": "inline-block", "marginRight": "10px"},
                    ),
                ],
                style={"marginBottom": "20px"},
            ),

            dcc.Graph(id="metrics-plot"),
            html.Div(id="metrics-diff-info"),  # Extra visual feedback
        ],
        style={"padding": "20px"},
    )
    return create_base_layout(content)
