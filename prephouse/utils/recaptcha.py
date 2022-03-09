import os

import requests  # type: ignore


def validate_recaptcha(token: str, expected_action: str) -> bool:
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": os.environ["RECAPTCHA_SECRET_KEY"],
            "response": token,
        },
    )
    response = response.json()
    return response["action"] == expected_action and response["success"] and response["score"] > 0.5
