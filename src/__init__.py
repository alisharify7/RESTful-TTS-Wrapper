"""
* REST TTS wrapper
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from src.urls import urlpatterns
from src.config import get_config
from src.utils import setup_init_extensions

from common_library.utils import print_api_info
from common_library.sentry import init_sentry


Setting = get_config()


def create_app(config_class) -> Flask:
    """
    factory function for creating flask application

    :param config_cls: Main config class
    :type config_cls: object

    :return: Flask application
    :rtype: Flask
    """
    # pylint: disable=W0621
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.testing = config_class.DEBUG

    setup_init_extensions(app=app, config_class=config_class)
    # init_sentry(config_class=config_class)

    # https://flask.palletsprojects.com/en/3.0.x/deploying/proxy_fix/
    app.wsgi_app = (
        ProxyFix(  # FIX proxy headers, tell flask is behind a reverse proxy
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )
    )

    return app


app = create_app(config_class=Setting)
print_api_info(app)

import src.main_base_views  # pylint: disable=C0413
