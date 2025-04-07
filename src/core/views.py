# pylint: disable=R0401
"""
* sahab tts wrapper REST service
* author: @alisharify7
* © under GPL-3.0 license.
* email: alisharifyofficial@gmail.com
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import json
import time

from flask import request
from flask_restx import Resource, abort

from src import http_status

from src.core import blp
from src.core.schem import CreateTTSRequest
from src.utils import (
    send_tts_request,
    check_cache_db,
    set_cache_db,
    download_audio,
    upload_to_s3,
    get_cached_db,
    api_key_required,
)
from common_library.utils import CryptoMethodUtils

crypto = CryptoMethodUtils()


@blp.route("/")
class TTSRouter(Resource):
    """Main api Resource class

    this class contains only a post method for creating
    tts voice.

    """

    @api_key_required  # api key required
    def post(self):
        """generate a tts voice request
        this endpoint is an entrypoint to requesting the Sahabt endpoint.

        this endpoint first generate hash value if the data field in
        request and check the cache db for any matching row with given
        hash value. if requested value is hashed before, its return
        hashed version otherwise it's going to make a request to sahab
        and cached the response and then return response.

        also this view return a http header called `x-cache-db`
        this field determine the freshness of the response if
        the value of this header is `True` it means response
        is generated recently. and it's not loaded from cache
        otherwise it means response is loaded from cache

        docs: https://isahab.ir/partai/TextToSpeech/1/description
        """
        try:
            data = json.loads(request.data.decode())
        except Exception:  # pylint:  disable=W0718
            return {
                "status": "failed",
                "message": "request body is not a valid JSON.",
            }, http_status.HTTP_400_BAD_REQUEST

        request_validator = CreateTTSRequest()
        try:
            request_validator.load(data)
        except Exception as e:  # pylint:  disable=W0718
            abort(
                status="failed",
                message=e.messages,  # pylint: disable=E1101
                code=http_status.HTTP_400_BAD_REQUEST,
            )

        normalized_data_field = request_validator.normalize_data(data["data"])
        hashed_data = crypto.to_sha256(normalized_data_field)

        if check_cache_db(cache_key=hashed_data):
            result = get_cached_db(cache_key=hashed_data)
            return (
                result,
                http_status.HTTP_200_OK,
                {"x-cache-db": "1", "x-read-from-cache": "1"},
            )

        # request is not cache, send request to sahab tts service.
        response = send_tts_request(body=request.data)

        if response.status_code == http_status.HTTP_200_OK:
            tts_response = response.json()
            audio_link = "https://" + tts_response["data"]["data"]["filePath"]
            audio_file_content = download_audio(audio_url=audio_link)
            if not audio_file_content:
                abort(
                    status="failed",
                    message="an issue occurred in downloading tts media \
                     voice from tts upstream server.",
                    code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            file_link_aws = upload_to_s3(
                bucket_name="ttsbucket",
                file_content=audio_file_content,
                file_name_key=f"{tts_response['meta']['requestId']}.\
                    {time.time_ns()}.{hashed_data}.mp3",
            )
            if not file_link_aws:
                abort(
                    status="failed",
                    message="an issue occurred in uploading the tts media \
                     voice in upstream s3 server..",
                    code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            tts_response["data"]["data"]["filePath"] = file_link_aws
            tts_response["unique_hash"] = hashed_data
            set_cache_db(cache_key=hashed_data, cache_data=tts_response)
            return (
                tts_response,
                http_status.HTTP_200_OK,
                {"x-cache-db": "0", "x-read-from-cache": "0"},
            )

        return (
            {
                "status": "failed",
                "message": "an error occurred, see logs for more information.",
                **response.json(),
                "from-sahab": True,
            },
            response.status_code,
        )
