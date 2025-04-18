"""
* REST TTS wrapper
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import typing
import requests
from flask import Flask, Blueprint

from src.config import get_config
from common_library import http_status


Setting = get_config()


def setup_init_extensions(app: Flask, config_class) -> None:
    """
    Initialize and configure extensions for the Flask application.

    This function initializes S3 manager, CORS, API manager with specifications,
    and registers API namespaces based on the urlpatterns.

    :param app: The Flask application instance.
    :type app: Flask

    :param config_class: The configuration class that contains settings like
                          `API_BASE_URL` and `HIDE_SWAGGER`.
    :type config_class: class
    """
    from src.extensions import s3_manager, api_manager, cors_manager
    from src import urlpatterns

    # Initialize S3 Manager
    app.extensions["s3_manager"] = s3_manager

    # Initialize CORS
    cors_manager.init_app(app=app)

    # Initialize API Manager with Swagger documentation control
    api_blueprint = Blueprint("api", __name__)
    api_manager.init_app(
        api_blueprint,
        add_specs=config_class.HIDE_SWAGGER,
        doc=config_class.HIDE_SWAGGER,
    )

    # Register the API blueprint with the given base URL
    app.register_blueprint(api_blueprint, url_prefix=config_class.API_BASE_URL)

    # Register API namespaces
    for each in urlpatterns:
        api_manager.add_namespace(each["obj"], path=each["url_prefix"])


def download_audio(audio_url: str) -> typing.Union[bytes, bool]:
    """
    Download audio content from a given URL.

    :param audio_url: Direct URL to the audio file.
    :type audio_url: str

    :return: Binary content of the audio if successful, otherwise False.
    :rtype: Union[bytes, bool]
    """
    try:
        response = requests.get(audio_url, timeout=120)
        if response.status_code == http_status.HTTP_200_OK:
            return response.content
    except requests.exceptions.RequestException as e:
        pass
    return False
