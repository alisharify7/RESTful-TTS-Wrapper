"""
* REST TTS wrapper
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import uuid
from time import sleep

import pytest
from src.config import get_config
from common_library.api_key import (
    store_api_key,
    is_api_key_valid,
    fetch_api_key_value,
    delete_api_key,
)

Setting = get_config()

api_key_name = uuid.uuid4().hex
api_key_value = uuid.uuid4().hex


@pytest.fixture
def setup_api_key():
    """Fixture to set up and tear down API keys for each test."""
    store_api_key(api_key_name, api_key_value)
    yield
    delete_api_key(api_key_name)


def test_set_api_key_with_expire_time(setup_api_key):
    """Test setting an API key with an expiration time."""
    # Set the API key with an expiration time of 1 second
    store_api_key(api_key_name, api_key_value, ex=1)
    sleep(1.2)  # Wait for the key to expire
    assert is_api_key_valid(api_key_name) == False


def test_set_api_key_without_expire_time(setup_api_key):
    """Test setting an API key without an expiration time."""
    # Set the API key without an expiration time
    store_api_key(api_key_name, api_key_value)
    sleep(1)  # Short sleep to simulate checking immediately
    assert is_api_key_valid(api_key_name) == True
    delete_api_key(api_key_name)


def test_get_api_key_method(setup_api_key):
    """Test that the API key can be retrieved correctly."""
    store_api_key(api_key_name, api_key_value)
    assert fetch_api_key_value(api_key_name) == api_key_value
    delete_api_key(api_key_name)


def test_check_api_key_exists(setup_api_key):
    """Test checking if the API key exists."""
    # Ensure key is present
    store_api_key(api_key_name, api_key_value)
    assert is_api_key_valid(api_key_name) == True
    delete_api_key(api_key_name)

    # Ensure key is absent after deletion
    delete_api_key(api_key_name)
    assert is_api_key_valid(api_key_name) == False


def test_delete_api_key(setup_api_key):
    """Test deleting the API key."""
    store_api_key(api_key_name, api_key_value)
    delete_api_key(api_key_name)
    assert is_api_key_valid(api_key_name) == False
