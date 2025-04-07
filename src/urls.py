"""
* sahab tts wrapper REST service
* author: @alisharify7
* © under GPL-3.0 license.
* email: alisharifyofficial@gmail.com
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

from api.tts import blp

# API URL
urlpatterns = [{"url_prefix": "", "obj": blp}]
