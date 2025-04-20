from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from backend.interfaces.state_repository import StateRepository

router = APIRouter()


def get_repository(request: Request) -> StateRepository:
    """Get repository."""
    return request.app.state.state_repository


@router.post("/state")
async def save_state(state: dict[str, Any], repo: StateRepository = Depends(get_repository)) -> JSONResponse:  # noqa: B008
    """Save hashed state for page."""
    state_hash = repo.save_state(state)
    return JSONResponse(content={"state_hash": state_hash})


@router.get("/state/{state_hash}")
async def get_state(state_hash: str, repo: StateRepository = Depends(get_repository)) -> JSONResponse:  # noqa: B008
    """Return hashed state for page."""
    try:
        state = repo.load_state(state_hash)
        return JSONResponse(content=state)
    except ValueError:
        return JSONResponse(status_code=404, content={"error": "State not found"})
