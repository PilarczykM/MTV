from dash import dcc, html
from dash.development.base_component import Component


def create_base_layout(content: Component) -> html.Div:
    """Create base layout."""
    return html.Div(
        [
            dcc.Location(id="url", refresh=False),
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
                                    dcc.Link("Trace", href="/trace", className="nav-link"),
                                    dcc.Link("Metric", href="/metric", className="nav-link"),
                                    dcc.Link("Tabele", href="/result", className="nav-link"),
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
                    html.Div(content, id="page-content"),
                ],
                className="app-container",
            ),
        ],
    )
