from abc import ABC, abstractmethod

from backend.models.test_dto import TestDto


class TestRepository(ABC):
    """Define a contract for accessing test data."""

    @abstractmethod
    def get_all_tests(self) -> list[TestDto]:
        """Return all available test records."""
        pass

    @abstractmethod
    def get_tests_by_ids(self, ids: list[str]) -> list[TestDto]:
        """Return tests matching the provided test IDs."""
        pass

    @abstractmethod
    def get_tests_by_name(self, names: list[str]) -> list[TestDto]:
        """Return tests matching the provided test names."""
        pass

    @abstractmethod
    def get_tests_by_type(self, types: list[str]) -> list[TestDto]:
        """Return tests matching the provided test types."""
        pass
