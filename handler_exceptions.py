from typing import Any, Dict, Optional

from fastapi import HTTPException


class PostFeedbackException(HTTPException):
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail


class PostRatingException(HTTPException):
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
