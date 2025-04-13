from json import JSONDecodeError

import pandas as pd
import requests

DEFAULT_TIMEOUT = 10000


def fetch_data_from_api(api_url: str) -> pd.DataFrame:
    """Fetch data from a REST API and returns it as a pandas DataFrame."""
    try:
        response = requests.get(api_url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)

        # Sent data via JSON needs to be concat
        trace_df = pd.json_normalize(df["traces"])
        metrics_df = pd.json_normalize(df["metrics"])
        df = pd.concat([df.drop(columns=["traces"]), trace_df], axis=1)
        df = pd.concat([df.drop(columns=["metrics"]), metrics_df], axis=1)
        return df
    except requests.HTTPError as e:
        print(f"Error while fetching data from API ({api_url}): {e}")
        return pd.DataFrame()
    except JSONDecodeError as e:
        print(f"Error while parsing data from API ({api_url}): {e}")
        return pd.DataFrame()
