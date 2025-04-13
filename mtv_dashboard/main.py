from dash import Dash

from mtv_dashboard.callback import websocket  # noqa: F401

app = Dash(__name__, suppress_callback_exceptions=True, title="MTV", use_pages=True)
server = app.server

if __name__ == "__main__":
    app.run(debug=True)
