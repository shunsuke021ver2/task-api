"""テスト共通の fixture。

各テストに対して空の InMemoryTaskRepository を注入し、
テスト間でデータが共有されないようにする。
"""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_task_repository
from app.main import create_app
from app.repository import InMemoryTaskRepository


@pytest.fixture
def client() -> Iterator[TestClient]:
    app = create_app()
    repo = InMemoryTaskRepository()
    app.dependency_overrides[get_task_repository] = lambda: repo
    with TestClient(app) as test_client:
        yield test_client
