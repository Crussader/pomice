class InvalidDeezerURL(Exception):
    """When an Invalid URL is given to the Client"""

class DeezerRequestException(Exception):
    """Thrown when the status of a request is not 200"""