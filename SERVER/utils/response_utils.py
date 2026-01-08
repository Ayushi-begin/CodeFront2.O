# backend/utils/response_utils.py

def success_response(message: str, data: dict = None):
    """
    Returns a standardized success JSON response.

    Args:
        message (str): Message describing the success.
        data (dict, optional): Payload data. Defaults to None.

    Returns:
        dict: Response object with success status and message.
    """
    return {
        "status": "success",
        "message": message,
        "data": data or {}
    }


def error_response(message: str, code: int = 400):
    """
    Returns a standardized error JSON response.

    Args:
        message (str): Error message.
        code (int, optional): HTTP status code. Defaults to 400.

    Returns:
        dict: Response object with error status and message.
    """
    return {
        "status": "error",
        "message": message,
        "code": code
    }
