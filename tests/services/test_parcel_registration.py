from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from app.schemas import ParcelCreate, ParcelType
from app.services import ParcelService
from tests.services.test_exchange_rate import FakeCache, FakeRateProvider

@pytest.mark.asyncio
async def test_creates_parcel_with_calculated_delivery_cost():
    session = AsyncMock()
    log_service = AsyncMock()
    
    parcel_type = SimpleNamespace(id=2, name="electronics")
    saved_parcel = SimpleNamespace(id=42)

    parcel = ParcelCreate(
        name="Test Parcel",
        weight=Decimal("2.0"),
        type=ParcelType.ELECTRONICS,
        content_cost_usd=Decimal("100.0"),
    )

    with (
        patch(
            "app.services.parcel.ParcelTypeRepository.get_by_name",
            return_value=parcel_type,
        ),
        patch(
            "app.services.parcel.ParcelRepository.create",
            return_value=saved_parcel,
        ) as create,
    ):
        parcel_id = await ParcelService.create_calculated(
            session=session,
            parcel_create=parcel,
            session_id="test_session",
            cache=FakeCache(),
            rate_provider=FakeRateProvider(),
            delivery_cost_log_service=log_service,
        )
    assert parcel_id == 42
    assert create.await_args.args[1]["delivery_cost_rub"] == Decimal("161.0")
    session.commit.assert_awaited_once()
    log_service.create_log.assert_awaited_once()