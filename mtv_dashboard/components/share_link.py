from dash import html


def share_link() -> html.Div:
    """Return share link component."""
    return html.Div(
        [
            html.Button(
                ["📋", " Copy URL"],
                id="copy-url-button",
                title="Click to copy the current URL and share it",
                style={"fontSize": "12px", "padding": "2px 4px"},
            ),
        ],
        style={"marginBottom": "20px"},
    )
