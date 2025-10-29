import base64
import asyncio
import httpx
from typing import Any, Dict, Optional, List
from .schemas import FilePart

class ConnectorService:
    def __init__(self) -> None:
        pass

    async def send_request(
        self,
        *,
        method: str,
        scheme: str = "http",
        domain: str,
        port: Optional[int] = None,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Any] = None,
        files: Optional[List[FilePart]] = None,
        headers: Optional[Dict[str, str]] = None,
        accept: Optional[str] = None,
        content_type: Optional[str] = None,
        auth_type: str = "digest",
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: float = 30.0,
        retries: int = 3,
        verify_ssl: bool = False,
        follow_redirects: bool = True,
        response_mode: str = "auto",
    ) -> Dict[str, Any]:

        url = self._build_url(scheme, domain, port, path)

        auth = self._build_auth(auth_type, username, password)
        if username and password and auth is None:
            return {"status": 401, "error": "auth_missing", "response": {}}

        req_headers = {**(headers or {})}
        if accept and "accept" not in {k.lower() for k in req_headers}:
            req_headers["Accept"] = accept

        request_kwargs: Dict[str, Any] = {
            "method": method.upper(),
            "url": url,
            "headers": req_headers,
            "params": params or {},
            "auth": auth,
            "timeout": timeout,
            "follow_redirects": follow_redirects,
        }

        if files:
            mfiles = []
            for f in files:
                mfiles.append(
                    (f.field_name,
                     (f.filename, base64.b64decode(f.content_base64), f.content_type))
                )
            request_kwargs["files"] = mfiles
            if isinstance(payload, dict):
                request_kwargs["data"] = payload
        else:
            if isinstance(payload, (dict, list)):
                request_kwargs["json"] = payload
                req_headers.setdefault("Content-Type", "application/json")
                req_headers.setdefault("Accept", req_headers.get("Accept", "application/json"))
            elif payload is not None:
                request_kwargs["content"] = payload
                if content_type:
                    req_headers["Content-Type"] = content_type
                else:
                    req_headers.setdefault("Content-Type", "text/plain")

        retries = max(retries, 1)
        last_exc: Optional[Exception] = None
        async with httpx.AsyncClient(verify=verify_ssl) as client:
            for attempt in range(retries):
                try:
                    resp = await client.request(**request_kwargs)
                    return await self._handle_response(resp, response_mode)
                except (httpx.RequestError, httpx.TimeoutException) as e:
                    last_exc = e
                    await asyncio.sleep(0.5 * (2 ** attempt))

        return {
            "status": 599,
            "error": "request_failed",
            "detail": str(last_exc) if last_exc else "unknown error",
        }

    @staticmethod
    def _build_url(scheme: str, domain: str, port: Optional[int], path: str) -> str:
        path = path if path.startswith("/") else f"/{path}"
        return f"{scheme}://{domain}{':' + str(port) if port else ''}{path}"

    @staticmethod
    def _build_auth(auth_type: str, username: Optional[str], password: Optional[str]):
        if auth_type == "none":
            return None
        if not username or not password:
            return None
        if auth_type == "basic":
            return httpx.BasicAuth(username, password)
        return httpx.DigestAuth(username, password)

    @staticmethod
    async def _handle_response(response: httpx.Response, mode: str) -> Dict[str, Any]:
        ctype = response.headers.get("Content-Type", "")
        base = {
            "status": response.status_code,
            "headers": dict(response.headers),
            "url": str(response.request.url),
        }

        if mode == "auto":
            if "application/json" in ctype:
                try:
                    return {**base, "response": response.json(), "content_type": ctype}
                except Exception:
                    return {**base, "response": response.text, "content_type": ctype}
            if "xml" in ctype or "text/xml" in ctype or "text/" in ctype:
                return {**base, "response": response.text, "content_type": ctype}
            b = response.content
            return {
                **base,
                "response_base64": base64.b64encode(b).decode("ascii"),
                "size": len(b),
                "content_type": ctype or "application/octet-stream",
            }

        if mode == "json":
            try:
                return {**base, "response": response.json(), "content_type": ctype}
            except Exception:
                return {**base, "response": response.text, "content_type": ctype}

        if mode in ("text", "xml"):
            return {**base, "response": response.text, "content_type": ctype}

        if mode == "bytes":
            b = response.content
            return {
                **base,
                "response_base64": base64.b64encode(b).decode("ascii"),
                "size": len(b),
                "content_type": ctype or "application/octet-stream",
            }

        return {**base, "response": response.text, "content_type": ctype}
