import dash
from dash.development.base_component import Component

from mtv_dashboard.callback import trace_plot  # noqa: F401
from mtv_dashboard.layout.trace import trace_layout

dash.register_page(__name__)


def trace_page() -> Component:
    """Render trace page."""
    return trace_layout()


layout = trace_page()
