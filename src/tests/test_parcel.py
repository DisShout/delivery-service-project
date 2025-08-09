import uuid
import pytest
from unittest.mock import AsyncMock, patch

from src.app.models.parcel import Parcel

TEST_SESSION_ID = "123e4567-e89b-12d3-a456-426614174000"


@pytest.mark.asyncio
@patch(
    "src.app.routes.parcel.RabbitService.send_message_to_rabbit", new_callable=AsyncMock
)
async def test_create_parcel(mock_send, async_client):
    mock_send.return_value = None
    response = await async_client.post(
        "/parcels/",
        cookies={"session_id": TEST_SESSION_ID},
        json={
            "name": "Тестовая посылка",
            "weight": 2.5,
            "parcel_price_usd": 50,
            "type_id": 1,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "Тестовая посылка"


@pytest.mark.asyncio
async def test_get_parcels(async_client):
    response = await async_client.get(
        "/parcels/", cookies={"session_id": TEST_SESSION_ID}
    )
    assert response.status_code == 200
    parcels = response.json()
    assert isinstance(parcels, list)


@pytest.mark.asyncio
async def test_get_parcel_by_id(async_client, db_session):
    parcel_id = uuid.uuid4()
    parcel = Parcel(
        id=parcel_id,
        name="Посылка для ID теста",
        weight=1.0,
        parcel_price_usd=10,
        type_id=1,
        session_id=TEST_SESSION_ID,
    )
    db_session.add(parcel)
    await db_session.commit()

    response = await async_client.get(
        f"/parcels/{parcel_id}", cookies={"session_id": TEST_SESSION_ID}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Посылка для ID теста"
    assert "delivery_price_rub" in data
