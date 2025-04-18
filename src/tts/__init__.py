"""
* REST TTS wrapper
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

from flask_restx import Namespace

blp = Namespace(name="tts", description="Operations on tts service")

import src.tts.views  # pylint: disable=C0413
