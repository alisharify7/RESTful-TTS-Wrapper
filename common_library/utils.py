"""
* REST TTS wrapper
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import base64
import hashlib
import random
import string

from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)
SysRandom = random.SystemRandom()


def print_api_info(app):
    def styled(text, color, underline=False, bold=False):
        underline_code = "\033[4m" if underline else ""
        bold_code = Style.BRIGHT if bold else ""
        return f"{bold_code}{color}{underline_code}{text}{Style.RESET_ALL}"

    print(
        " *",
        styled("© RESTful TTS wrapper", Fore.RED, underline=True, bold=True),
    )
    print(
        " *",
        styled("©", Fore.RED, underline=True, bold=True),
        styled(
            f"{app.config.get('API_NAME')} REST API",
            Fore.RED,
            underline=True,
            bold=True,
        ),
    )

    print(
        " *",
        styled("API", Fore.GREEN, underline=True, bold=True),
        "base url:",
        styled(app.config.get("API_BASE_URL"), Fore.YELLOW, bold=True),
    )

    print(
        " *",
        styled("Swagger", Fore.GREEN, underline=True, bold=True),
        "base url:",
        styled(app.config.get("API_DOCS_URL"), Fore.YELLOW, bold=True),
    )

    print(
        " *",
        styled("API", Fore.GREEN, underline=True, bold=True),
        "short version:",
        styled(app.config.get("API_SHORT_VERSION"), Fore.YELLOW, bold=True),
    )

    print(
        " *",
        styled("API", Fore.GREEN, underline=True, bold=True),
        "absolute version:",
        styled(app.config.get("API_ABSOLUTE_VERSION"), Fore.YELLOW, bold=True),
    )


def generate_random_string(length: int = 6, punctuation: bool = True) -> str:
    """
    Generate a strong random string.

    :param length: Length of the random string. Default is 6.
    :param punctuation: If True, punctuation characters will be included.
    :return: A randomly generated string.
    """
    characters = string.ascii_letters + string.digits
    if punctuation:
        characters += string.punctuation
    return "".join(SysRandom.choices(characters, k=length))


def to_base64(data: str) -> str:
    """
    Encode a string to Base64 format.

    :param data: Input string to encode.
    :return: Base64 encoded string.
    """
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")


def to_sha256(data: str) -> str:
    """
    Generate SHA-256 hash of a string.

    :param data: Input string to hash.
    :return: SHA-256 hexadecimal digest.
    """
    return hashlib.sha256(data.encode("utf-8")).hexdigest()
