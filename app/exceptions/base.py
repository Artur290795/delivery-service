"""Доменные исключения сервиса доставки."""


class BaseDeliveryServiceException(Exception):
    """Базовое исключение предметной области сервиса доставки."""


class InvalidParcelTypeException(BaseDeliveryServiceException):
    """Ошибка при указании несуществующего типа посылки."""


class ParcelNotFoundException(BaseDeliveryServiceException):
    """ORM-представление посылки пользователя и рассчитанной стоимости доставки."""


class SimilarVectorNotFoundException(BaseDeliveryServiceException):
    """Ошибка при отсутствии подходящего фрагмента в базе знаний."""
