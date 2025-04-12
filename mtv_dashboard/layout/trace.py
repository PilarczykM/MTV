from dash import html

from mtv_dashboard.layout.base import create_base_layout
from mtv_dashboard.layout.home import home_layout


def trace_layout() -> html.Div:
    """"""
    content = html.Div(
        [
            html.H2("Trace Plot Page"),
        ],
    )
    return create_base_layout(content)
