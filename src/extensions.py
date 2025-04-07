"""
* sahab tts wrapper REST service
* author: @alisharify7
* © under GPL-3.0 license.
* email: alisharifyofficial@gmail.com
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import boto3
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restx import Api

from src.settings import Setting
from src.logger import get_logger

cors = CORS(resources={r"/api/*": {"origins": "*"}})
db = SQLAlchemy()
migrate = Migrate()

aws_object_storage = boto3.client(
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

global_logger = get_logger(logger_name="tts-logger", log_level=10)
