from dash import Dash, ClientsideFunction

from mtv_dashboard.callback import websocket  # noqa: F401
from mtv_dashboard.callback.trace_plot import register_clientside_callbacks

app = Dash(__name__, suppress_callback_exceptions=True, title="MTV", use_pages=True)
server = app.server

register_clientside_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
