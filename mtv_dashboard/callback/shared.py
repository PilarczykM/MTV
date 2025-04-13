from dash import ClientsideFunction, Dash, Input, Output


def register_clientside_callbacks(app: Dash) -> None:
    """Register client side callback."""
    app.clientside_callback(
        ClientsideFunction(namespace="clipboard", function_name="copyUrlToClipboard"),
        Output("copy-confirmation", "children"),
        Input("copy-url-button", "n_clicks"),
        prevent_initial_call=True,
    )
