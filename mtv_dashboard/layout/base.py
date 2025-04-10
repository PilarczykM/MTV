from dash import dcc, html


def create_layout() -> html.Div:
    """Create base layout."""
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Img(src="assets/logo.png", style={"height": "60px"}),
                                    html.P("Multi Test Viever"),
                                ],
                                className="header-left",
                            ),
                            html.Div(
                                [
                                    dcc.Link("Trace", href="*", className="nav-link"),
                                    dcc.Link("Metric", href="*", className="nav-link"),
                                    dcc.Link("Tabele", href="*", className="nav-link"),
                                ],
                                className="header-right",
                            ),
                        ],
                        className="app-container",
                    ),
                ],
                className="header",
            ),
            html.Div(
                [
                    dcc.Location(id="url", refresh=False),
                    html.Div(id="page-content"),
                ],
                className="app-container",
            ),
        ],
    )
