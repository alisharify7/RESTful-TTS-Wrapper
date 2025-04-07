"""
* sahab tts wrapper REST service
* author: @alisharify7
* © under GPL-3.0 license.
* email: alisharifyofficial@gmail.com
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import json
import uuid
from copy import deepcopy

from flask import url_for

from common_library import http_status


def test_tts_invalid_request_method(app, client):
    """testing invalid http method type
    sending different http method to api service.
    """
    response = client.get(url_for("api.tts_tts_2"))  # GET
    assert response.status_code == http_status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.put(url_for("api.tts_tts_2"))  # PUT
    assert response.status_code == http_status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.patch(url_for("api.tts_tts_2"))  # PATCH
    assert response.status_code == http_status.HTTP_405_METHOD_NOT_ALLOWED


def test_tts_no_request_body_data(headers, client):
    """testing sending request with no json body"""
    r = client.post(url_for("api.tts_tts_3"))
    assert r.status_code == http_status.HTTP_400_BAD_REQUEST

    r = client.post(url_for("api.tts_tts_3"), data={})
    assert r.status_code == http_status.HTTP_400_BAD_REQUEST

    r = client.post(url_for("api.tts_tts_3"), data=headers)
    assert r.status_code == http_status.HTTP_400_BAD_REQUEST


def test_sending_request_with_no_gateway_token_header(app, client):
    """testing `gateway-token` header required decorator."""
    data = {
        "data": f"{uuid.uuid4()}",
        "filePath": "true",
        "base64": "1",
        "checksum": "1",
        "speaker": "3",
        "speed": "0.7",
    }
    response = client.post(
        url_for("api.tts_tts_4"),
        data=json.dumps(data),
        headers={"Content-Type": "application/json", "auth": "ok"},
    )
    assert response.status_code == http_status.HTTP_400_BAD_REQUEST
    assert response.json["message"] == "missing `gateway-token` in headers."
    assert response.json["status"] == "failed"


def test_invalid_gateway_token_header(client):
    """testing invalid gateway-token header"""
    data = {
        "data": f"{uuid.uuid4()}",
        "filePath": "true",
        "base64": "1",
        "checksum": "1",
        "speaker": "3",
        "speed": "0.7",
    }
    response = client.post(
        url_for("api.tts_tts_5"),
        data=json.dumps(data),
        headers={
            "Content-Type": "application/json",
            "gateway-token": "fake and invalid value",
        },
    )
    assert response.status_code == http_status.HTTP_403_FORBIDDEN
    assert (
        response.json["message"]
        == "`gateway-token` api-key has been expired or its invalid."
    )
    assert response.json["status"] == "failed"


def test_tts_normal_request(app, client, headers):
    """testing normal request with cache header reading"""
    data = {
        "data": f"{uuid.uuid4()}",
        "filePath": "true",
        "base64": "1",
        "checksum": "1",
        "speaker": "3",
        "speed": "0.7",
    }
    # test first fresh request with no caching
    response = client.post(
        url_for("api.tts_tts_6"), data=json.dumps(data), headers=headers
    )
    assert response.status_code == http_status.HTTP_200_OK
    assert response.headers.get("x-cache-db") == "0"
    assert response.headers.get("x-read-from-cache") == "0"

    # test cache
    response = client.post(
        url_for("api.tts_tts_6"), data=json.dumps(data), headers=headers
    )
    assert response.status_code == http_status.HTTP_200_OK
    assert response.headers.get("x-cache-db") == "1"
    assert response.headers.get("x-read-from-cache") == "1"


def test_invalid_json_body(client, headers):
    """testing invalid json body .

    testing to see validators works and return
    error.
    """
    data = {
        "data": "تست",
        "filePath": "true",
        "base64": "1",
        "checksum": "1",
        "speaker": "3",
        "speed": "0.7",
    }
    for key, value in data.items():
        # loop over all available json key and check one by one
        dt = deepcopy(data)
        dt.pop(key)
        response = client.post(
            url_for("api.tts_tts_7"), data=json.dumps(dt), headers=headers
        )
        assert response.status_code == http_status.HTTP_400_BAD_REQUEST
        assert "failed" == response.json["status"]
        assert key in response.json["message"]

        dt[key] = value
        response = client.post(
            url_for("api.tts_tts_7"), data=json.dumps(dt), headers=headers
        )
        assert response.status_code == http_status.HTTP_200_OK
