from dash import Dash

from mtv_dashboard.callback import websocket  # noqa: F401
from mtv_dashboard.layout.base import create_layout
from mtv_dashboard.layout.home import home_layout

app = Dash(__name__, suppress_callback_exceptions=True, title="MTV")
server = app.server

app.layout = create_layout(content=home_layout())

if __name__ == "__main__":
    app.run(debug=True)
