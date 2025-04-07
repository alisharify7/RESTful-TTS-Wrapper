""" "
* sahab tts wrapper REST service
* author: @alisharify7
* © under GPL-3.0 license.
* email: alisharifyofficial@gmail.com
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import uuid
from time import sleep

from src.settings import Setting
from src.keyapi_db import (
    get_api_key,
    set_api_key,
    check_api_key_exists,
    delete_api_key,
)
from .conftest import API_KEY_TOKEN

api_key_name = uuid.uuid4().hex
api_key_value = uuid.uuid4().hex
db = Setting.REDIS_API_KEY_INTERFACE


def test_set_api_key_method():
    """testing setting new api key in db method"""

    # @ `assert` set api key method `with` expire time
    set_api_key(api_key_name, api_key_value, ex=1)
    sleep(1.2)
    assert check_api_key_exists(api_key_name) == False

    # @ `assert` set api key method `without` expire time
    set_api_key(api_key_name, api_key_value)
    sleep(1)
    assert check_api_key_exists(api_key_name) == True

    delete_api_key(api_key_name)


def test_get_api_key_method():
    """testing get api key method is ok"""
    set_api_key(api_key_name, api_key_value)
    assert get_api_key(api_key_name) == api_key_value
    delete_api_key(api_key_name)


def test_check_api_key_method():
    set_api_key(api_key_name, api_key_value)
    delete_api_key(api_key_name)
    assert check_api_key_exists(api_key_name) == False

    set_api_key(api_key_name, api_key_value)
    assert check_api_key_exists(api_key_name) == True
    delete_api_key(api_key_name)


def test_delete_api_key():
    """testing` delete api key` method is ok"""
    set_api_key(api_key_name, api_key_value)
    delete_api_key(api_key_name)
    assert check_api_key_exists(api_key_name) == False
