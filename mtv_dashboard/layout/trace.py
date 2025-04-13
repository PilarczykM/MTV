from dash import dcc, html

from mtv_dashboard.layout.base import create_base_layout


def trace_layout() -> html.Div:
    """Return trace layout."""
    content = html.Div(
        [
            dcc.Location(id="url", refresh=False),
            html.Div(
                [
                    html.H2("Trace Plot Page"),
                    html.Div(
                        [
                            html.Button(
                                ["📋", " Copy URL"],
                                id="copy-url-button",
                                title="Click to copy the current URL and share it",
                                style={"fontSize": "12px", "padding": "2px 4px"}
                            ),
                            html.Div(id="copy-confirmation", style={"color": "green", "marginTop": "10px"}),
                        ],
                        style={"margin-bottom": "20px"},
                    ),
                ],
                style={"display": "flex", "gap": "20px"}
            ),
            html.Div(
                [
                    html.Label("Select tests:"),
                    dcc.Dropdown(
                        id="test-name-dropdown",
                        options=[],  # Populated dynamically based on data
                        multi=True,
                        placeholder="Select tests to compare",
                    ),
                ],
                style={"marginBottom": "20px"},
            ),
            html.Div(
                [
                    html.Label("Select Trace signals:"),
                    dcc.Checklist(
                        id="trace-checklist",
                        options=[{"label": f"Trace {i}", "value": f"Trace {i}"} for i in range(1, 11)],
                        value=["Trace 1"],
                        labelStyle={"display": "inline-block", "marginRight": "10px"},
                    ),
                ],
                style={"marginBottom": "20px"},
            ),
            dcc.Graph(id="trace-plot"),
        ],
        style={"padding": "20px"},
    )
    return create_base_layout(content)
