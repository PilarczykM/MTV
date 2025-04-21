import pandas as pd
from dash import dash_table, dcc, html

from mtv_dashboard.layout.base import create_base_layout
from mtv_dashboard.utils.consts import API_TESTS_URL
from mtv_dashboard.utils.data_fetcher import fetch_data_from_api


def results_table_layout() -> html.Div:
    """Return the layout for the results summary table."""
    df = fetch_data_from_api(API_TESTS_URL)
    summary = build_test_summary(df)

    trace_cols = [col for col in summary.columns if col.startswith("Trace")]
    metric_cols = [col for col in summary.columns if col.startswith("Metric")]

    content = html.Div(
        [
            html.H2("Test Results Summary Table"),
            # Column selection
            html.Div(
                [
                    html.Label(
                        "📈 Select Trace Columns:",
                        style={
                            "fontWeight": "bold",
                            "fontSize": "15px",
                            "marginBottom": "6px",
                            "display": "block",
                        },
                    ),
                    dcc.Dropdown(
                        id="trace-column-dropdown",
                        options=[{"label": col, "value": col} for col in trace_cols],
                        value=trace_cols,
                        multi=True,
                        placeholder="Select Trace columns",
                        style={"width": "100%"},
                    ),
                    html.Label(
                        "📊 Select Metric Columns:",
                        style={
                            "fontWeight": "bold",
                            "fontSize": "15px",
                            "marginBottom": "6px",
                            "display": "block",
                        },
                    ),
                    dcc.Dropdown(
                        id="metric-column-dropdown",
                        options=[{"label": col, "value": col} for col in metric_cols],
                        value=metric_cols,
                        multi=True,
                        placeholder="Select Metric columns",
                        style={"width": "100%"},
                    ),
                ],
                style={"marginBottom": "20px"},
            ),
            # DataTable
            dash_table.DataTable(
                id="summary-table",
                columns=[{"name": col, "id": col} for col in summary.columns],
                data=summary.to_dict("records"),
                page_size=15,
                filter_action="native",
                sort_action="native",
                row_selectable="multi",
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left", "minWidth": "100px"},
            ),
            html.Div(id="selected-tests-plot-container"),
        ],
        style={"padding": "20px", "width": "100%"},
    )

    return create_base_layout(content)


def build_test_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Build a summary DataFrame with test parameters, trace stats and metrics."""
    trace_cols = [col for col in df.columns if col.startswith("Trace")]
    metric_cols = [col for col in df.columns if col.startswith("Metric")]
    param_cols = ["test_id", "test_name", "test_type", "test_param_1", "test_param_2", "test_param_3"]

    trace_stats = df.groupby("test_id")[trace_cols].agg(["mean", "std", "min", "max"])
    trace_stats.columns = ["_".join(col).strip() for col in trace_stats.columns.values]

    param_values = df.groupby("test_id")[param_cols[1:]].first()
    metric_values = df.groupby("test_id")[metric_cols].first()

    return pd.concat([param_values, trace_stats, metric_values], axis=1).reset_index()
