"""
* sahab tts wrapper REST service
* author: @alisharify7
* © under GPL-3.0 license.
* email: alisharifyofficial@gmail.com
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import base64
import hashlib
import random
import string

from flask import Flask
from celery import Celery, Task


SysRandom = random.SystemRandom()


def generate_random_string(length: int = 6, punctuation: bool = True) -> str:
    """generate strong random strings

    :param length: length of random string - default is 6
    :type length: int

    :param punctuation: if this flag is set to `true`, punctuation will be added to random strings
    :type punctuation: bool

     :return: str: random string
    """
    letters = string.ascii_letters
    if punctuation:
        letters += string.punctuation
    random_string = SysRandom.choices(letters, k=length)

    return "".join(random_string)


def celery_init_app(app: Flask) -> Celery:
    """celery init function method"""

    class FlaskTask(Task):  # pylint: disable=W0223
        """Every time a task is added to queue
        __call__ is call.
        """

        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.Task = FlaskTask
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


class CryptoMethodUtils:
    """cryptography utils class"""

    def to_base64(self, data: str) -> str:
        """Converts a string to base64 encoding.

        Args:
          data: The string to be encoded.

        Returns:
          The base64 encoded string.
        """

        encoded_bytes = base64.b64encode(data.encode("utf-8"))
        return encoded_bytes.decode("utf-8")

    def to_sha256(self, data: str) -> str:
        """Converts a string to md5.

        Args:
          data: The string to be encoded.

        Returns:
          The md5 encoded string.
        """
        return hashlib.sha256(data.encode("utf-8")).hexdigest()
