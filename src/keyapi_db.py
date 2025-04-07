"""
* sahab tts wrapper REST service
* author: @alisharify7
* © under GPL-3.0 license.
* email: alisharifyofficial@gmail.com
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

from src.settings import get_config

Setting = get_config()


def check_api_key_exists(api_key: str) -> bool:
    """validating api key

    checking api key is valid or not,
    this function makes query to redis
    and check is there any record in redis
    with given api key or not

    :param api_key: api key
    :type api_key: str
    :return: true if api key is valid, false otherwise
    :rtype: bool
    """
    db = Setting.REDIS_API_KEY_INTERFACE

    if not (has_access := db.get(name=api_key) or b""):
        return False
    data = has_access.decode()
    if data:
        return True
    return False


def set_api_key(api_key_name: str, api_key_value: str, ex=None) -> bool:
    """set api key in api key in api cache db

    :param api_key_name: api key name if redis
    :type api_key_name: str

    :param api_key_value: value of api key in redis
    :type api_key_value: str

    :param ex: expire time, seconds
    :type ex: int

    :return: true if api key is valid, false otherwise
    :rtype: bool
    """
    db = Setting.REDIS_API_KEY_INTERFACE
    if ex:
        return db.set(name=api_key_name, value=api_key_value, ex=ex)

    return db.set(
        name=api_key_name,
        value=api_key_value,
    )


def get_api_key(api_key: str) -> str:
    """get a api key from api cache db

    :param api_key: api key
    :type api_key: str
    :return: api key
    :rtype: str
    """
    db = Setting.REDIS_API_KEY_INTERFACE

    data = db.get(name=api_key) or b""
    return data.decode()


def delete_api_key(api_key: str) -> None:
    """delete a api key from api cache db
    :param api_key: api key
    :type api_key: str
    """
    db = Setting.REDIS_API_KEY_INTERFACE

    return db.delete(api_key)
