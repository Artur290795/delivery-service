"""Сервис регистрации и просмотра посылок."""

from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from app.exceptions import InvalidParcelTypeException, ParcelNotFoundException
from app.models import Parcel, LogData
from app.protocols import Cache, RateProvider
from app.repositories import ParcelRepository, ParcelTypeRepository
from app.schemas import (
    ParcelCreate,
    ParcelResponse,
    ParcelType,
)
from app.services.delivery_cost_log import DeliveryCostLogService
from app.services.delivery_cost import DeliveryCostService
from app.services.exchange_rate import ExchangeRateService


class ParcelService:
    """ORM-представление посылки пользователя и рассчитанной стоимости доставки."""

    @staticmethod
    async def create_calculated(
        session: AsyncSession,
        parcel_create: ParcelCreate,
        session_id: str,
        cache: Cache,
        rate_provider: RateProvider,
        delivery_cost_log_service: DeliveryCostLogService,
    ) -> int:
        parcel_data = parcel_create.model_dump()
        parcel_data["session_id"] = session_id

        parcel_type = await ParcelTypeRepository.get_by_name(
            session, parcel_create.type.value
        )
        if not parcel_type:
            raise InvalidParcelTypeException("Invalid type of parcel")

        parcel_data["type_id"] = parcel_type.id
        del parcel_data["type"]

        try:
            rate = await ExchangeRateService.get_usd_rub_rate(cache, rate_provider)
            delivery_cost = DeliveryCostService.calculate(
                weight=parcel_create.weight,
                content_cost_usd=parcel_create.content_cost_usd,
                usd_rub_rate=rate,
            )
            parcel_data["delivery_cost_rub"] = delivery_cost
            new_parcel = await ParcelRepository.create(session, parcel_data)
            parcel_id = new_parcel.id
            parcel_type_name = parcel_type.name
            await session.commit()

            await delivery_cost_log_service.create_log(
                LogData(
                    parcel_id=parcel_id,
                    parcel_type=parcel_type_name,
                    delivery_cost=delivery_cost,
                    calculated_at=datetime.now(timezone.utc),
                )
            )
            logger.info(
                "Parcel persisted: parcel_id={parcel_id}, delivery_cost={delivery_cost}",
                parcel_id=parcel_id,
                delivery_cost=delivery_cost,
            )
            return parcel_id
        except Exception:
            logger.exception("Failed to persist parcel registration")
            await session.rollback()
            raise

    @staticmethod
    async def get_user_parcels(
        session: AsyncSession,
        session_id: str,
        limit: int,
        offset: int,
        parcel_type: ParcelType | None = None,
        delivery_cost_calculated: bool | None = None,
    ) -> list[ParcelResponse]:
        parcels = await ParcelRepository.get_user_parcels(
            session,
            session_id,
            limit,
            offset,
            parcel_type.value if parcel_type else None,
            delivery_cost_calculated,
        )

        result = []
        for parcel in parcels:
            parcel_dict = ParcelService.get_parcel(parcel)
            result.append(ParcelResponse(**parcel_dict))
        return result

    @staticmethod
    async def get_parcel_by_id(
        session: AsyncSession, parcel_id: int, session_id: str
    ) -> ParcelResponse:

        parcel = await ParcelRepository.get_parcel_by_id(session, parcel_id, session_id)
        if not parcel:
            raise ParcelNotFoundException(
                f"Parcel with id {parcel_id} not found for the given session."
            )
        parcel_dict = ParcelService.get_parcel(parcel)
        return ParcelResponse(**parcel_dict)

    @staticmethod
    def get_parcel(parcel: Parcel) -> ParcelResponse:
        parcel_dict = {
            "id": parcel.id,
            "name": parcel.name,
            "weight": parcel.weight,
            "type": parcel.type.name,
            "content_cost_usd": parcel.content_cost_usd,
            "delivery_cost_rub": (
                parcel.delivery_cost_rub
                if parcel.delivery_cost_rub is not None
                else "Стоимость посылки еще не рассчитана"
            ),
        }
        return parcel_dict
