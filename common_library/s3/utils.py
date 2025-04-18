"""
* REST TTS wrapper
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import typing
from src.extensions import s3_manager


def upload_to_s3(
    bucket_name, file_name_key, file_content
) -> typing.Union[str, bool]:
    """upload an object into aws s3 bucket,
    this function take a bucket name and file name and file content and
    upload it into aws s3 bucket,
    """
    try:
        s3_manager.put_object(
            ACL="public-read",
            Body=file_content,
            Key=file_name_key,
            Bucket=bucket_name,
        )
    except Exception as e:  # pylint: disable=W0718
        return False

    return (
        f"https://s3.ir-thr-at1.arvanstorage.ir/{bucket_name}/{file_name_key}"
    )
