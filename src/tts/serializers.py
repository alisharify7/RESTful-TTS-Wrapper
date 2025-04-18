"""
* REST TTS wrapper
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

from marshmallow import Schema, fields, validate


class TTSSerializer(Schema):
    """TTS request JSON serializer and validator class."""

    data = fields.String(
        required=True,
        error_messages={"required": "`data` field is required."},
        validate=validate.Length(min=1, error="`data` field cannot be empty."),
    )
    filePath = fields.Boolean(
        required=True,
        error_messages={"required": "`filePath` field is required."},
    )
    base64 = fields.String(
        required=True,
        error_messages={"required": "`base64` field is required."},
        validate=validate.Length(
            min=1, error="`base64` field cannot be empty."
        ),
    )
    checksum = fields.String(
        required=True,
        error_messages={"required": "`checksum` field is required."},
        validate=validate.Length(
            min=1, error="`checksum` field cannot be empty."
        ),
    )
    speaker = fields.String(
        required=True,
        error_messages={"required": "`speaker` field is required."},
        validate=validate.Length(
            min=1, error="`speaker` field cannot be empty."
        ),
    )
    speed = fields.Float(
        required=True,
        error_messages={"required": "`speed` field is required."},
        validate=validate.Range(
            min=0, error="`speed` must be a positive number."
        ),
    )

    def clean_data(self, data: str) -> str:
        """Normalize the data field, remove all unnecessary spaces and concatenate all text together."""
        return "".join(data.split())
