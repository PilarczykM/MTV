import dash
from dash import html

dash.register_page(__name__)

content = html.Div(
    className="centered-404",
    children=[
        html.H1("404 - Page Not Found"),
        html.P("Sorry, the page you are looking for does not exist."),
        html.A("Return to the homepage", href="/"),
    ],
)

layout = content
