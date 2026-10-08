"""Доменные исключения сервиса доставки."""

class BaseDeliveryServiceException(Exception):
    """Базовое исключение предметной области сервиса доставки."""
    pass


class InvalidParcelTypeException(BaseDeliveryServiceException):
    """Ошибка при указании несуществующего типа посылки."""
    pass


class ParcelNotFoundException(BaseDeliveryServiceException):
    """ORM-представление посылки пользователя и рассчитанной стоимости доставки."""
    pass


class SimilarVectorNotFoundException(BaseDeliveryServiceException):
    """Ошибка при отсутствии подходящего фрагмента в базе знаний."""
    pass
