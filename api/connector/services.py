import json
from typing import Dict, Any

import aiohttp
import httpx
from fastapi import UploadFile


class ConnectorService:

    async def send_request(
            self,
            method: str,
            domain: str,
            url: str,
            payload: Dict[str, Any],
            auth:  httpx.DigestAuth,
            headers: Dict[str, str] | None = None,
    ) -> Dict[str, Any]:
        url = f"http://{domain}/{url}"

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method.upper(),
                url=url,
                json=payload,
                headers=headers,
                auth=auth,
                timeout=30.0
            )

        return await self._handle_response(response)

    async def send_face_request(
            self,
            method: str,
            domain: str,
            url: str,
            payload: Dict[str, Any],
            file: Dict[str, UploadFile],
            auth: aiohttp.BasicAuth,
            headers: Dict[str, str] | None = None,
    ) -> Dict[str, Any]:
        url = f"http://{domain}/{url}"

        async with aiohttp.ClientSession() as session:
            form_data = aiohttp.FormData()

            for key, value in payload.items():
                if isinstance(value, (dict, list)):
                    form_data.add_field(
                        key, json.dumps(value), content_type="application/json"
                    )
                else:
                    form_data.add_field(key, str(value))

            for key, upload in file.items():
                content = await upload.read()
                form_data.add_field(
                    key,
                    content,
                    filename=upload.filename,
                    content_type=upload.content_type or "application/octet-stream",
                )

            async with session.request(
                    method=method.upper(),
                    url=url,
                    data=form_data,
                    headers=headers,
                    auth=auth
            ) as resp:
                return await self._handle_response(resp)

    @staticmethod
    async def _handle_response(response: httpx.Response) -> Dict[str, Any]:
        try:
            data = response.json()
        except Exception:
            data = response.text
        return {
            "status": data.status_code,
            "response": data
        }
