import dash

from mtv_dashboard.layout.trace import trace_layout

dash.register_page(__name__)

def trace_page():
    print("TRACE LAYOUT RENDERED")
    return trace_layout()

layout = trace_page()
