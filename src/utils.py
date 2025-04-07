"""
* sahab tts wrapper REST service
* author: @alisharify7
* © under GPL-3.0 license.
* email: alisharifyofficial@gmail.com
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import json
import typing

import requests
from flask import current_app

from src import http_status
from src.settings import Setting
from src.extensions import aws_object_storage, global_logger


from functools import wraps
from flask import request
from src.keyapi_db import check_api_key_exists
from src import http_status


def api_key_required(f):
    """
    api_key_required decorator

    this function runs before every function view and check
    if incoming request doesn't have any `gateway-token` it will
    raise an error, this function just make sure that incoming
    request contain `gateway-token` header and also token in
    header is valid and exist in api key db.
    """

    @wraps(f)
    def inner_decorator(*args, **kwargs):
        api_key_header = request.headers.get("gateway-token")
        if not api_key_header:
            return {
                "status": "failed",
                "message": "missing `gateway-token` in headers.",
            }, http_status.HTTP_400_BAD_REQUEST

        if not check_api_key_exists(api_key=api_key_header):
            return {
                "status": "failed",
                "message": "`gateway-token` api-key has been expired or its invalid.",
            }, http_status.HTTP_403_FORBIDDEN

        return f(*args, **kwargs)

    return inner_decorator


def send_tts_request(body: str) -> requests.Response:
    """send a http request to sahab api endpoint,

    https://isahab.ir/partai/TextToSpeech/1/description

    this data should send as a json stringify data
        "data": "این یک نمونه از صدای من است.",
        "filePath": true,
        "base64": "1",
        "checksum": "1",
        "timestamp": "1",
        "speaker": "3",
        "speed": "1"

    :param body: body of the post request
    :type body: str

    :return: requests.Response
    :rtype: requests.Response

    """
    if current_app.testing:
        example_testing_response = {
            "data": {
                "data": {
                    "base64": "test",
                    "checksum": "test",
                    "filePath": "fake-path",  # pylint: disable=C0301
                },
                "error": None,
                "status": "success",
            },
            "meta": {
                "requestId": "########-####-####-#####-############",
                "shamsiDate": "140##############",
            },
        }

        r = requests.Response()
        r.status_code = 200
        r.json = lambda: example_testing_response
        return r

    global_logger.debug(
        "[N] SEND A HTTP REQUEST TO %s", Setting.TTS_SERVICE_ENDPOINT
    )
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
    except Exception as e:  # pylint: disable=W0718
        # pylint: disable=W0104
        global_logger.debug("[E] Error in sending request to sahab %s", e)
        response = requests.Response()
        response.status_code == 408
        response.json = lambda: {"err": "timeout error from upstream server."}
        return response


def upload_to_s3(
    bucket_name, file_name_key, file_content
) -> typing.Union[str, bool]:
    """upload an object into aws s3 bucket,
    this function take a bucket name and file name and file content and
    upload it into aws s3 bucket,
    """

    global_logger.debug("[N] Upload to aws storage %s", file_name_key)

    try:
        aws_object_storage.put_object(
            ACL="public-read",
            Body=file_content,
            Key=file_name_key,
            Bucket=bucket_name,
        )
    except Exception as e:  # pylint: disable=W0718
        global_logger.debug("[E] Error in uploading data in aws storage %s", e)
        return False

    return (
        f"https://s3.ir-thr-at1.arvanstorage.ir/{bucket_name}/{file_name_key}"
    )


def download_audio(audio_url: str) -> typing.Union[bool, bytes]:
    """Download audio from given url

    :param audio_url: url of the audio to download
    :type audio_url: str

    :return: audio.bin
    :rtype: str
    """
    global_logger.debug("[N] Downloading new audio from url %s", audio_url)
    try:
        response = requests.get(audio_url, timeout=120)
    except Exception as e:  # pylint: disable=W0718
        global_logger.debug(
            "[E] Error in Downloading new audio from url %s, \n %s",
            audio_url,
            e,
        )
        return False
    if response.status_code != http_status.HTTP_200_OK:
        global_logger.debug(
            "[E] Error in Downloading new audio from url %s, \
            got status code %s",
            audio_url,
            response.status_code,
        )
        return False
    return response.content


def check_cache_db(cache_key: str) -> bool:
    """this function check a key is in cache db or not.
    if cache key was not in data this function returns False
    otherwise its return True

    :param cache_key: key of the key to be checked
    :type cache_key: str

    :return: `True` if cache key was in cache db
    :rtype: bool
    """
    db = Setting.REDIS_CACHE_INTERFACE
    result = db.get(cache_key) or b""
    result = result.decode()
    if result:
        return True
    return False


def get_cached_db(cache_key: str) -> dict:
    """get a cached data from cache db.

    this function get a cache key name and return
    cached data from cache db

    :param cache_key: key of the key to be checked
    :type cache_key: str

    :return: data dict
    :rtype: dict
    """
    db = Setting.REDIS_CACHE_INTERFACE
    result = db.get(cache_key) or b""
    result = result.decode()
    return json.loads(result)


def set_cache_db(cache_key: str, cache_data: dict) -> bool:
    """set cached data into redis database

    this function set a cached data into cache db.

    :param cache_key: key of the key to be checked
    :type cache_key: str

    :param cache_data: data to be cached
    :type cache_data: dict

    :return: `True` if cache was set in db otherwise `False`
    :rtype: bool
    """
    if not current_app.config.get("CACHE_ENABLE", ""):
        return True  # if cache is disable by pass caching

    db = Setting.REDIS_CACHE_INTERFACE
    return db.set(name=cache_key, value=json.dumps(cache_data))
