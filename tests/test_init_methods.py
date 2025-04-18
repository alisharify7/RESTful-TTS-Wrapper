"""
* REST TTS wrapper
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

from src.config import get_config
from src.config.settings import Development, Production

Setting = get_config()


def test_get_config_method():
    """
    testing get_config method is ok and returns
    config class base on DEBUG variables
    """
    config_cls = get_config(True)
    assert config_cls is Development

    config_cls = get_config(False)
    assert config_cls is Production
