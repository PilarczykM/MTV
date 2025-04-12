from pathlib import Path
from typing import Any, Optional

import pandas as pd

from backend.interfaces.test_repository import TestRepository
from backend.models.test_dto import TestDto
from backend.utils.paths import CSV_PATH


class TestCSVRepository(TestRepository):
    """Implementation of TestRepository."""

    def __init__(self, csv_path: Path = CSV_PATH) -> None:
        """Initialize TestCSVRepository class."""
        self._df = pd.read_csv(csv_path)
        self._df.columns = self._df.columns.str.strip()

    def get_all_tests(self) -> list[TestDto]:
        """Get all tests."""
        return self._to_dto_list(self._df)

    def get_tests_by_ids(self, ids: list[str]) -> list[TestDto]:
        """Get all tests by ID."""
        df = self._df[self._df["Test ID"].isin(ids)]
        return self._to_dto_list(df)

    def get_tests_by_name(self, names: list[str]) -> list[TestDto]:
        """Get all tests by name."""
        df = self._df[self._df["Test name"].isin(names)]
        return self._to_dto_list(df)

    def get_tests_by_type(self, types: list[str]) -> list[TestDto]:
        """Get all tests by type."""
        df = self._df[self._df["Test type"].isin(types)]
        return self._to_dto_list(df)

    def _to_dto_list(self, df: pd.DataFrame) -> list[TestDto]:
        """Convert dataframe info Test Data Transfer Object."""
        return [
            TestDto(
                test_id=row["Test ID"],
                test_name=row["Test name"],
                test_type=row["Test type"],
                test_param_1=row["Test param 1"],
                test_param_2=row["Test param 2"],
                test_param_3=row["Test param 3"],
                time_start=int(row["Time [s]"]),
                traces={f"Trace {i}":self._sanitize_value(row[f"Trace {i}"]) for i in range(1, 11)},
                metrics={f"Metric {i}": self._sanitize_value(row[f"Metric {i}"]) for i in range(1, 7)},
            )
            for _, row in df.iterrows()
        ]

    @staticmethod
    def _sanitize_value(value: Any) -> Optional[float]:
        """Convert invalid float values to None (e.g., NaN, inf)."""
        if pd.isna(value) or value in {float("inf"), float("-inf")}:
            return None
        return value
