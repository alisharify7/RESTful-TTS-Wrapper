"""
* sahab tts wrapper REST service
* author: @alisharify7
* © under GPL-3.0 license.
* email: alisharifyofficial@gmail.com
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

from flask_restx import Namespace

blp = Namespace(name="tts", description="Operations on tts service")

import src.core.views  # pylint: disable=C0413
