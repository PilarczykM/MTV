import dash
from dash.development.base_component import Component

from mtv_dashboard.callback import result_plot  # noqa: F401
from mtv_dashboard.layout.results_table import results_table_layout

dash.register_page(__name__)


def results_table_page() -> Component:
    """Render results summary table page."""
    return results_table_layout()


layout = results_table_page()
