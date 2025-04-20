from dash import ClientsideFunction, Dash, Input, Output


def register_clientside_callbacks(app: Dash) -> None:
    """Register client side callback."""
    app.clientside_callback(
        ClientsideFunction(namespace="clipboard", function_name="copyStateUrlToClipboard"),
        Output("copy-confirmation", "children", allow_duplicate=True),
        Input("url", "search"),
        prevent_initial_call=True,
    )
