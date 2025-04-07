"""
* sahab tts wrapper REST service
* author: @alisharify7
* © under GPL-3.0 license.
* email: alisharifyofficial@gmail.com
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import os
import pathlib
from pathlib import Path

import redis
from dotenv import load_dotenv
from common_library.utils import generate_random_string

load_dotenv()


class BaseSetting:
    """Base Setting class"""

    SECRET_KEY: str = os.environ.get(
        "APP_SECRET_KEY", generate_random_string()
    )
    if not os.environ.get("APP_SECRET_KEY", False):
        print(
            "SECRET_KEY was not found in .env file, fall back "
            "into generate_random_string() function. "
        )
    FLASK_DEBUG: bool = os.environ.get("APP_DEBUG", "") == "True"
    DEBUG: bool = FLASK_DEBUG
    FLASK_ENV = DEBUG
    SERVER_NAME: str = os.environ.get("SERVER_NAME", "localhost:8000")
    BASE_DIR: pathlib.Path = Path(__file__).parent.parent.resolve()
    MAX_CONTENT_LENGTH: int = 1024 * 1024 * 3  # global upload max size 3 MB

    # flask-resx config
    # https://flask-restx.readthedocs.io/en/latest/configuration.html
    RESTX_ERROR_404_HELP: bool = False
    RESTX_VALIDATE: bool = True

    # cache setting
    CACHE_ENABLE = os.environ.get("CACHE_ENABLE", "") == "True"

    def __str__(self):
        return "BaseSetting Class"

    def __repr__(self):
        return self.__str__()


class Setting(BaseSetting):
    """universal config class
    every property on this class will be automatically mapping to app.config
    """

    # redis config
    REDIS_DEFAULT_URI: str = os.environ.get("REDIS_DEFAULT_URI", "localhost")
    REDIS_DEFAULT_INTERFACE = redis.Redis().from_url(REDIS_DEFAULT_URI)

    REDIS_CACHE_URI = os.environ.get("REDIS_CACHE_URI", "localhost")
    REDIS_CACHE_INTERFACE = redis.Redis().from_url(REDIS_CACHE_URI)

    REDIS_API_KEY_URI: str = os.environ.get("REDIS_API_KEY_URI", "localhost")
    REDIS_API_KEY_INTERFACE = redis.Redis.from_url(REDIS_API_KEY_URI)

    # sahab tts service config
    TTS_SERVICE_API_KEY: str = os.environ.get("TTS_SERVICE_API_KEY", "")
    TTS_SERVICE_ENDPOINT: str = os.environ.get("TTS_SERVICE_ENDPOINT", "")

    # arvan AWS s3 object storage config
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_ENDPOINT_URL = os.environ.get("AWS_ENDPOINT_URL")

    # main API config
    API_NAME: str = os.environ.get("API_NAME", "api-service")
    API_DOCS_URL: str = f'{os.environ.get("API_DOCS_PREFIX_URL", "/docs/")}'
    API_ABSOLUTE_VERSION: str = os.environ.get("API_ABSOLUTE_VERSION", "1.0.0")
    API_SHORT_VERSION: str = os.environ.get("API_SHORT_VERSION", "1.0.0")
    API_BASE_URL: str = (
        f"/{os.environ.get('API_BASE_URL')}{API_SHORT_VERSION}/"
    )
    HIDE_SWAGGER: str = os.environ.get("HIDE_SWAGGER", "") != "True"
    # https://github.com/python-restx/flask-restx/issues/116

    def __str__(self):
        return "Setting Class"

    def __repr__(self):
        return self.__str__()


class Production(Setting):
    """Production config class

    use this class for Production config class.
    """

    FLASK_DEBUG: bool = False
    DEBUG: bool = FLASK_DEBUG
    FLASK_ENV = DEBUG

    def __str__(self):
        return "Production Config Class"

    def __repr__(self):
        return self.__str__()


class Development(Setting):
    """Development config class

    use this class for Development config class.
    """

    FLASK_DEBUG: bool = True
    DEBUG: bool = FLASK_DEBUG
    FLASK_ENV = DEBUG

    def __str__(self):
        return "Development Config Class"

    def __repr__(self):
        return self.__str__()


def get_config(debug: bool = BaseSetting.DEBUG):
    """Getting config setting class base on `environment` status.
    :return: object
    :rtype: object
    """
    match debug:
        case True:
            return Development
        case False:
            return Production
        case _:
            return Production
