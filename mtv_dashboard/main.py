from dash import Dash
from layout.base import create_layout

app = Dash(__name__, suppress_callback_exceptions=True, title="MTV")
server = app.server

app.layout = create_layout()

if __name__ == "__main__":
    app.run(debug=True)
