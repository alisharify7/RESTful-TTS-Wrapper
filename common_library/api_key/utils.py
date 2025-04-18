"""
* REST TTS wrapper
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

from functools import wraps
from typing import Optional

from flask import request, make_response, jsonify
from src.config import get_config
from common_library import http_status


Setting = get_config()


def is_api_key_valid(api_key: str) -> bool:
    """
    Check whether the given API key is valid.

    This function queries the Redis database to verify
    if the provided API key exists.

    :param api_key: API key to validate.
    :return: True if the key is valid, False otherwise.
    """
    db = Setting.REDIS_API_KEY_INTERFACE
    return bool(db.get(name=api_key))


def store_api_key(
    api_key_name: str, api_key_value: str, ex: Optional[int] = None
) -> bool:
    """
    Store an API key in Redis.

    :param api_key_name: The name (or identifier) of the API key in Redis.
    :param api_key_value: The actual API key value to store.
    :param ex: Expiration time in seconds (optional).
    :return: True if the operation was successful, False otherwise.
    """
    db = Setting.REDIS_API_KEY_INTERFACE
    return db.set(name=api_key_name, value=api_key_value, ex=ex)


def fetch_api_key_value(api_key: str) -> Optional[str]:
    """
    Retrieve the value of an API key from Redis.

    :param api_key: API key name to retrieve.
    :return: The API key value as a string if found, None otherwise.
    """
    db = Setting.REDIS_API_KEY_INTERFACE
    value = db.get(name=api_key)
    return value.decode() if value else None


def delete_api_key(api_key: str) -> bool:
    """
    Delete an API key from Redis.

    :param api_key: The API key name to delete.
    :return: True if the key was deleted, False if it didn't exist.
    """
    db = Setting.REDIS_API_KEY_INTERFACE
    return bool(db.delete(api_key))


def api_key_required(f):
    """
    Decorator to enforce API key validation via `gateway-token` header.

    Ensures that:
    - A `gateway-token` header is present in the incoming request.
    - The API key provided is valid (via Redis or DB check).

    Returns a 400 or 403 error if validation fails.
    """
    GATEWAY_HEADER = "gateway-token"

    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get(GATEWAY_HEADER)

        if not api_key:
            return make_response(
                jsonify(
                    {
                        "status": "failed",
                        "message": f"Missing `{GATEWAY_HEADER}` in headers.",
                    }
                ),
                http_status.HTTP_400_BAD_REQUEST,
            )

        if not is_api_key_valid(api_key):
            return make_response(
                jsonify(
                    {
                        "status": "failed",
                        "message": f"`{GATEWAY_HEADER}` is invalid or expired.",
                    }
                ),
                http_status.HTTP_403_FORBIDDEN,
            )

        return f(*args, **kwargs)

    return decorated_function
