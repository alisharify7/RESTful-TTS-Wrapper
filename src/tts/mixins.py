# pylint: disable=R0401
"""
* REST TTS wrapper
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import json
import time
from typing import Optional

from flask_restx import abort
from requests import Response

from src.utils import download_audio
from src.tts.serializers import TTSSerializer
from src.tts.utils import get_cache, set_cache, cache_exists, send_tts_request
from common_library.s3 import upload_to_s3
from common_library import http_status


class TTSGeneratorMixin:

    def _parse_request_data(self, raw_data: bytes) -> Optional[dict]:
        """Helper method to parse request data."""
        try:
            return json.loads(raw_data.decode())
        except Exception:
            return None

    def _validate_request_data(self, data: dict) -> Optional[dict]:
        """Helper method to validate the TTS request data."""
        request_validator = TTSSerializer()
        errors = request_validator.validate(data)
        if errors:
            return errors
        return None

    def _normalize_data(self, data_field: str) -> str:
        """Helper method to normalize the data field."""
        return TTSSerializer().clean_data(data_field)

    def _check_cache(self, data_hash: str) -> bool:
        """Helper method to check if the data exists in the cache."""
        return cache_exists(key=data_hash)

    def _get_cached_response(self, data_hash: str) -> tuple:
        """Helper method to get the cached response."""
        cached_data = get_cache(key=data_hash)
        return (
            cached_data,
            http_status.HTTP_200_OK,
            {"x-cache-db": "1", "x-read-from-cache": "1"},
        )

    def _send_tts_request(self, request_body: str | bytes) -> Response:
        """Helper method to send the TTS request to the Sahab API."""
        return send_tts_request(body=request_body)

    def _process_tts_response(self, tts_data: dict, data_hash: str) -> tuple:
        """Helper method to process the TTS response, download the audio, and store it."""
        audio_url = "https://" + tts_data["data"]["data"]["filePath"]
        audio_file = download_audio(audio_url=audio_url)

        if not audio_file:
            abort(
                status="failed",
                message="an issue occurred in downloading tts media voice from the TTS server.",
                code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        file_link_aws = upload_to_s3(
            bucket_name="ttsbucket",  # TODO: read from config
            file_content=audio_file,
            file_name_key=f"{tts_data['meta']['requestId']}.{time.time_ns()}.{data_hash}.mp3",
        )

        if not file_link_aws:
            abort(
                status="failed",
                message="an issue occurred in uploading the tts media voice to the S3 server.",
                code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        tts_data["data"]["data"]["filePath"] = file_link_aws
        tts_data["unique_hash"] = data_hash
        set_cache(key=data_hash, data=tts_data)

        return (
            tts_data,
            http_status.HTTP_200_OK,
            {"x-cache-db": "0", "x-read-from-cache": "0"},
        )

    def _handle_tts_error(self, response: Response) -> tuple:
        """Helper method to handle TTS errors."""
        return {
            "status": "failed",
            "message": "an error occurred, see logs for more information.",
            **response.json(),
            "from-sahab": True,
        }, response.status_code
