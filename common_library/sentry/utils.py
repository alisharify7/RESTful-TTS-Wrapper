"""
* REST TTS wrapper
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


def init_sentry(config_class, dsn) -> None:
    sentry_sdk.init(
        dsn="",
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
        environment="development" if config_class.DEBUG else "production",
        release=config_class.API_ABSOLUTE_VERSION,
    )
