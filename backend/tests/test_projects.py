"""Project router tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_projects_empty(client: AsyncClient) -> None:
    response = await client.get("/api/v1/code/projects")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_and_get_project(client: AsyncClient) -> None:
    create_resp = await client.post(
        "/api/v1/code/projects",
        json={"name": "Test Project", "language": "python"},
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["name"] == "Test Project"

    get_resp = await client.get(f"/api/v1/code/projects/{created['id']}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Test Project"


@pytest.mark.asyncio
async def test_update_project(client: AsyncClient) -> None:
    create_resp = await client.post(
        "/api/v1/code/projects",
        json={"name": "Old Name"},
    )
    assert create_resp.status_code == 201
    pid = create_resp.json()["id"]

    resp = await client.put(
        f"/api/v1/code/projects/{pid}",
        json={"name": "New Name"},
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "New Name"


@pytest.mark.asyncio
async def test_delete_project(client: AsyncClient) -> None:
    create_resp = await client.post(
        "/api/v1/code/projects",
        json={"name": "To Delete"},
    )
    assert create_resp.status_code == 201
    pid = create_resp.json()["id"]

    resp = await client.delete(f"/api/v1/code/projects/{pid}")
    assert resp.status_code == 204

    get_resp = await client.get(f"/api/v1/code/projects/{pid}")
    assert get_resp.status_code == 404
