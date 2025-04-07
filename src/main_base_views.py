"""
* sahab tts wrapper REST service
* author: @alisharify7
* © under GPL-3.0 license.
* email: alisharifyofficial@gmail.com
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

from flask import current_app
from src import app


@app.get("/")
def index():
    """root index view"""
    return {
        "status": "success",
        "message": "we are up !",
        "api-version": current_app.config.get("API_ABSOLUTE_VERSION"),
        "api-short-version": current_app.config.get("API_SHORT_VERSION"),
        "api-base-url": current_app.config.get("API_BASE_URL"),
        "x-well-configured": current_app.debug,
    }
