from typing import Generator

import pytest
from fastapi.testclient import TestClient

from src.flex.db.session import SessionLocal
from src.flex.main import app


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
