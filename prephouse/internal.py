from flask import Request

from prephouse.models import User


class PrephouseRequest(Request):
    user: User | None = None
