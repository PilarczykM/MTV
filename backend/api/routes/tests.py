from fastapi import APIRouter, Depends, Query, Request

from backend.interfaces.test_repository import TestRepository
from backend.models.test_dto import TestDto

router = APIRouter()


def get_repository(request: Request) -> TestRepository:
    """Get repository."""
    return request.app.state.test_repository


@router.get("/tests", response_model=list[TestDto])
def get_all_tests(repo: TestRepository = Depends(get_repository)) -> list[TestDto]:
    """Return all test records from the data source."""
    return repo.get_all_tests()


@router.get("/tests/by-id", response_model=list[TestDto])
def get_tests_by_id(
    test_id: list[str] = Query(...),
    repo: TestRepository = Depends(get_repository),
) -> list[TestDto]:
    """
    Return multiple tests by a list of IDs provided as repeated query parameters.

    Example: /tests/by-id?test_id=T-001&test_id=T-002
    """
    return repo.get_tests_by_ids(test_id)


@router.get("/tests/by-name", response_model=list[TestDto])
def get_tests_by_name(
    test_name: list[str] = Query(...),
    repo: TestRepository = Depends(get_repository),
) -> list[TestDto]:
    """
    Return multiple tests by a list of names provided as repeated query parameters.

    Example: /tests/by-name?test_name=TestA&test_name=TestB
    """
    return repo.get_tests_by_name(test_name)


@router.get("/tests/by-type", response_model=list[TestDto])
def get_tests_by_type(
    test_type: list[str] = Query(...),
    repo: TestRepository = Depends(get_repository),
) -> list[TestDto]:
    """
    Return multiple tests by a list of types provided as repeated query parameters.

    Example: /tests/by-type?test_type=Stress&test_type=Functional
    """
    return repo.get_tests_by_type(test_type)
