"""
* REST TTS wrapper
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

from flask import current_app
from src import app


@app.get("/")
@app.get("/version/")
@app.get("/up/")
@app.get("/status/")
@app.get("/health/")
@app.get("/health-check/")
@app.get("/ping/")
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
