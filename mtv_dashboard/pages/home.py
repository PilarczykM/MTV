import dash

from mtv_dashboard.layout.home import home_layout

dash.register_page(__name__, path="/")

layout = home_layout()
