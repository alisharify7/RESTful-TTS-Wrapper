"""
* sahab tts wrapper REST service
* author: @alisharify7
* © under GPL-3.0 license.
* email: alisharifyofficial@gmail.com
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

from api import create_app
from api.config import get_config

flask_app = create_app(config_cls=get_config())
celery_app = flask_app.extensions["celery"]
