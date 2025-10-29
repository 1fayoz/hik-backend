from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field

AuthType = Literal["digest", "basic", "none"]
ResponseMode = Literal["auto", "json", "text", "xml", "bytes"]

class FilePart(BaseModel):
    field_name: str = Field(..., description="multipart maydon nomi, masalan 'img' yoki 'faceURL'")
    filename: Optional[str] = None
    content_type: str = "application/octet-stream"
    content_base64: str = Field(..., description="Fayl baytlarining base64 ko‘rinishi")

class CommonSchema(BaseModel):
    method: str = Field(..., examples=["GET","POST","PUT","PATCH","DELETE"])
    domain: str = Field(..., examples=["192.168.0.106","example.com"])
    url: str = Field(..., description="Masalan: /ISAPI/AccessControl/UserInfo/SetUp")

    scheme: Literal["http","https"] = "http"
    params: Optional[Dict[str, Any]] = {}

    payload: Optional[Any] = {}
    files: Optional[List[FilePart]] = None

    headers: Optional[Dict[str, str]] = {}
    accept: Optional[str] = {}
    content_type: Optional[str] = {}

    username: Optional[str] = None
    password: Optional[str] = None

    timeout: float = 30.0
    retries: int = 3
