"""
* REST TTS wrapper
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import boto3
from flask_cors import CORS
from flask_restx import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from src.config import get_config

Setting = get_config()

db = SQLAlchemy()
cors_manager = CORS(resources={r"/api/*": {"origins": "*"}})
migrate_manager = Migrate()

s3_manager = boto3.client(
    "s3",
    aws_access_key_id=Setting.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Setting.AWS_SECRET_ACCESS_KEY,
    endpoint_url=Setting.AWS_ENDPOINT_URL,
)

api_manager = Api(
    version=Setting.API_ABSOLUTE_VERSION,
    title="GRAFANA API REST",
    description=" tts API REST service",
    terms_url="/terms/",
    contact="",
    doc=Setting.API_DOCS_URL,
    license="",
)
