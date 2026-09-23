class BaseDeliveryServiceException(Exception):
    pass

class InvalidParcelTypeException(BaseDeliveryServiceException):
    pass

class ParcelNotFoundException(BaseDeliveryServiceException):
    pass
