class ServiceException(Exception):
    """Base exception class for API service"""
    def __init__(self, message) -> None:
        super().__init__(self, message)
