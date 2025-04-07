"""
* sahab tts wrapper REST service
* author: @alisharify7
* © under GPL-3.0 license.
* email: alisharifyofficial@gmail.com
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from flask import Flask, Blueprint
from werkzeug.middleware.proxy_fix import ProxyFix

from src.settings import get_config
from src.extensions import cors, api_manager, aws_object_storage
from src.urls import urlpatterns

from common_library.color import Colors


def create_app(config_cls=None) -> Flask:
    """
    factory function for creating flask application

    :param config_cls: Main config class
    :type config_cls: object

    :return: Flask application
    :rtype: Flask
    """
    # pylint: disable=W0621
    app = Flask(__name__)
    app.config.from_object(config_cls)
    app.extensions["aws"] = aws_object_storage
    app.testing = config_cls.DEBUG
    # sentry_sdk.init(
    #     dsn="",
    #     # Set traces_sample_rate to 1.0 to capture 100%
    #     # of transactions for tracing.
    #     integrations=[FlaskIntegration()],
    #     traces_sample_rate=1.0,
    #     environment="development" if config_cls.DEBUG else "production",
    #     release=config_cls.API_ABSOLUTE_VERSION,
    # )

    api_blueprint = Blueprint("api", __name__)
    api_manager.init_app(
        api_blueprint,
        add_specs=config_cls.HIDE_SWAGGER,
        doc=config_cls.HIDE_SWAGGER,
    )
    app.register_blueprint(api_blueprint, url_prefix=config_cls.API_BASE_URL)

    # register api blueprints
    for each in urlpatterns:
        api_manager.add_namespace(each["obj"], path=each["url_prefix"])

    # register extensions
    cors.init_app(app=app)

    # https://flask.palletsprojects.com/en/3.0.x/deploying/proxy_fix/
    app.wsgi_app = (
        ProxyFix(  # FIX proxy headers, tell flask is behind a reverse proxy
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )
    )

    return app


app = create_app(config_cls=get_config())
print(
    f" * {Colors.BOLD}{Colors.RED}{Colors.UNDERLINE}© RESTful TTS wrapper "
    f"{Colors.RESET}"
)
print(
    f" * {Colors.BOLD}{Colors.RED}{Colors.UNDERLINE}© "
    f"{app.config.get('API_NAME')} REST API{Colors.RESET}"
)
print(
    f" * {Colors.BOLD}{Colors.GREEN}{Colors.UNDERLINE}"
    f"API{Colors.RESET} base url: {Colors.BOLD}"
    f"{Colors.WARNING}{app.config.get('API_BASE_URL')}{Colors.RESET}"
)
print(
    f" * {Colors.BOLD}{Colors.GREEN}{Colors.UNDERLINE}"
    f"Swagger{Colors.RESET} base url: {Colors.BOLD}"
    f"{Colors.WARNING}{app.config.get('API_DOCS_URL')}{Colors.RESET}"
)
print(
    f" * {Colors.BOLD}{Colors.GREEN}{Colors.UNDERLINE}"
    f"API{Colors.RESET} short version: {Colors.BOLD}"
    f"{Colors.WARNING}{app.config.get('API_SHORT_VERSION')}{Colors.RESET}"
)
print(
    f" * {Colors.BOLD}{Colors.GREEN}{Colors.UNDERLINE}"
    f"API{Colors.RESET} absolute version: {Colors.BOLD}"
    f"{Colors.WARNING}{app.config.get('API_ABSOLUTE_VERSION')}{Colors.RESET}"
)

import src.tasks  # pylint: disable=C0413
import src.decorators  # pylint: disable=C0413
import src.main_base_views  # pylint: disable=C0413
