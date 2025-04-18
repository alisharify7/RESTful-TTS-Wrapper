"""
* REST TTS wrapper
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import json

import requests
from requests import Response

from flask import current_app
from src.config import get_config

Setting = get_config()


def cache_exists(key: str) -> bool:
    """
    Check if a given key exists in the cache database.

    :param key: The cache key to look for.
    :type key: str

    :return: True if the key exists and has a value, otherwise False.
    :rtype: bool
    """
    db = Setting.REDIS_CACHE_INTERFACE
    value = db.get(key)
    return bool(value and value.decode())


def get_cache(key: str) -> dict:
    """
    Retrieve cached data from the cache database.

    :param key: The cache key to retrieve.
    :type key: str

    :return: Cached data as a dictionary.
    :rtype: dict

    :raises json.JSONDecodeError: If the cached data is not a valid JSON.
    """
    db = Setting.REDIS_CACHE_INTERFACE
    value = db.get(key)
    if not value:
        return {}

    try:
        return json.loads(value.decode())
    except json.JSONDecodeError:
        # global_logger.warning("[W] Invalid JSON in cache for key: %s", key)
        return {}


def set_cache(key: str, data: dict, ex: int = None) -> bool:
    """
    Set a dictionary as JSON in the cache database.

    :param key: The cache key under which data is stored.
    :type key: str

    :param data: The dictionary to cache.
    :type data: dict

    :param ex: Expiry time in seconds (optional).
    :type ex: int

    :return: True if data is successfully cached, otherwise False.
    :rtype: bool
    """
    if not current_app.config.get("CACHE_ENABLE", True):
        return True  # Caching disabled, consider it successful

    db = Setting.REDIS_CACHE_INTERFACE
    value = json.dumps(data)

    if ex:
        return db.set(name=key, value=value, ex=ex)

    return db.set(name=key, value=value)


def mock_tts_response():
    example_response = {
        "data": {
            "data": {
                "base64": "test",
                "checksum": "test",
                "filePath": "fake-path",
            },
            "error": None,
            "status": "success",
        },
        "meta": {
            "requestId": "########-####-####-#####-############",
            "shamsiDate": "140##############",
        },
    }
    response = Response()
    response.status_code = 200
    response._content = json.dumps(example_response).encode("utf-8")
    return response


def send_tts_request(body: str) -> Response:
    """
    Send a POST request to Sahab TTS API.

    See: https://isahab.ir/partai/TextToSpeech/1/description

    Example JSON body:
        {
            "data": "این یک نمونه از صدای من است.",
            "filePath": true,
            "base64": "1",
            "checksum": "1",
            "timestamp": "1",
            "speaker": "3",
            "speed": "1"
        }

    :param body: JSON stringified body to send.
    :return: requests.Response object
    """
    if current_app.testing:
        return mock_tts_response()

    # global_logger.debug("[N] Sending HTTP request to %s", Setting.TTS_SERVICE_ENDPOINT)

    headers = {
        "Content-Type": "application/json",
        "gateway-token": Setting.TTS_SERVICE_API_KEY,
    }

    try:
        return requests.post(
            url=Setting.TTS_SERVICE_ENDPOINT,
            headers=headers,
            data=body,
            timeout=10,
        )
    except requests.exceptions.RequestException as e:
        # global_logger.exception("[E] Request to Sahab failed: %s", str(e))
        response = Response()
        response.status_code = 408
        response._content = json.dumps(
            {"error": "timeout error from upstream server."}
        ).encode("utf-8")
        return response
