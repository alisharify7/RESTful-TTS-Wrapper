# pylint: disable=R0401
"""
* REST TTS wrapper
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/RESTful-tts-wrapper
"""


from flask import request
from flask_restx import Resource

from src.tts import blp
from common_library import http_status
from common_library.utils import to_sha256
from common_library.api_key import api_key_required
from src.tts.mixins import TTSGeneratorMixin


@blp.route("/")
class TTSRouter(Resource, TTSGeneratorMixin):
    """Main API Resource class for generating TTS voice requests."""

    @api_key_required  # api key required
    def post(self):
        """Generate a TTS voice request.

        The endpoint processes the TTS request by first checking for a cached version.
        If not found, it makes a request to the TTS service and caches the response.

        Returns a header 'x-cache-db' to indicate whether the response was fetched from the cache or generated recently.
        """
        # Parsing and validating the incoming data
        data = self._parse_request_data(request.data)
        if not data:
            return {
                "status": "failed",
                "message": "request body is not a valid JSON.",
            }, http_status.HTTP_400_BAD_REQUEST

        validation_errors = self._validate_request_data(data)
        if validation_errors:
            return {
                "status": "failed",
                "message": validation_errors,
            }, http_status.HTTP_400_BAD_REQUEST

        # Generate the hash for the data
        normalized_data = self._normalize_data(data["data"])
        data_hash = to_sha256(normalized_data)

        # Check if the request is cached
        if self._check_cache(data_hash):
            return self._get_cached_response(data_hash)

        # If not cached, send request to TTS service and process the response
        response = self._send_tts_request(request.data)
        if response.status_code == http_status.HTTP_200_OK:
            return self._process_tts_response(response.json(), data_hash)

        return self._handle_tts_error(response)
