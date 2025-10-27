from typing import Optional, Any, Literal

from pydantic import BaseModel
from fastapi import UploadFile
from utils.decorators import as_form


class CommonSchema(BaseModel):
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
    domain: str
    url: str
    payload: dict[str, Any]
    username: str
    password: str


@as_form
class AddFaceSchema(BaseModel):
    method: str
    domain: str
    url: str
    payload: str
    image: UploadFile
    image_key: str
    username: str
    password: str
