import hashlib
import json

from backend.interfaces.state_repository import StateRepository


class LocalStateRepository(StateRepository):
    """Implement StateRepository with only in-memory local database."""

    def __init__(self) -> None:
        """Initialize local storage repository."""
        self._store: dict[str, str] = {}

    def save_state(self, state: dict) -> str:
        """Save the state dictionary in memory, keyed by its SHA256 hash (shortened)."""
        state_str = json.dumps(state, sort_keys=True)
        state_hash = hashlib.sha256(state_str.encode()).hexdigest()[:10]
        self._store[state_hash] = state_str
        return state_hash

    def load_state(self, state_hash: str) -> dict:
        """Load the state from memory based on the hash. Raises ValueError if not found."""
        state_str = self._store.get(state_hash)
        if not state_str:
            msg = f"No state found for hash: {state_hash}"
            raise ValueError(msg)
        return json.loads(state_str)
