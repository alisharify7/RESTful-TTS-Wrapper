"""
* sahab tts wrapper REST service
* author: @alisharify7
* © under GPL-3.0 license.
* email: alisharifyofficial@gmail.com
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

from marshmallow import Schema, fields


class CreateTTSRequest(Schema):
    """TTS request json serializer and validator class"""

    # TODO: add custom error, and remove default marshmallow error
    data = fields.String(required=True)
    filePath = fields.Boolean(required=True)
    base64 = fields.String(required=True)
    checksum = fields.String(required=True)
    speaker = fields.String(required=True)
    speed = fields.String(required=True)

    def normalize_data(self, data: str):
        """normalize data field, remove all white spaces
        and concat all text together"""
        text = ""
        for each in data:
            each = each.strip()
            if each and each != " ":
                text += each
        return text
