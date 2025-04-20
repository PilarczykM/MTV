from abc import ABC, abstractmethod


class StateRepository(ABC):
    """State repository interface."""

    @abstractmethod
    def save_state(self, state: dict) -> str:
        """Save the dashboard state and return a unique hash."""
        pass

    @abstractmethod
    def load_state(self, state_hash: str) -> dict:
        """Load a saved dashboard state by hash."""
        pass
