"""
* REST TTS wrapper
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import pytest
import redis

from src import create_app
from src.settings import Setting


class TestConfig(Setting):
    API_ABSOLUTE_VERSION = "1.1.1"
    API_SHORT_VERSION = "1.1.1"
    API_DOCS_URL = "/test/docs/"
    API_NAME = "test"
    SERVER_NAME = "localhost:8000"
    SWAGGER_ADD_SPECS = False
    HIDE_SWAGGER = False
    TESTING = True
    DEBUG = True
    CACHE_ENABLE = True


API_KEY_TOKEN = "token"


@pytest.fixture(name="app")
def app():
    app = create_app(TestConfig)
    db: redis.Redis = app.config.get("REDIS_API_KEY_INTERFACE")
    assert db.set(name=API_KEY_TOKEN, value=API_KEY_TOKEN) == True
    yield app


@pytest.fixture(name="client")
def client(app):
    with app.app_context():
        yield app.test_client()


@pytest.fixture(name="headers")
def headers():
    return {"gateway-token": API_KEY_TOKEN}
