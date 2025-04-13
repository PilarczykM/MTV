import dash
from dash.development.base_component import Component
from mtv_dashboard.callback import metric_plot

from mtv_dashboard.layout.metric import metrics_layout

dash.register_page(__name__)


def metrics_page() -> Component:
    """Render metrics page."""
    return metrics_layout()


layout = metrics_page()
