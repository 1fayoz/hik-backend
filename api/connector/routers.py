import json

import aiohttp
from fastapi import APIRouter, Depends, HTTPException

from .schemas import CommonSchema, AddFaceSchema
from .services import ConnectorService

router = APIRouter(
    prefix="/connector",
    tags=["Worker"]
)


@router.post("/common")
async def create_worker(
        schema: CommonSchema,
        service: ConnectorService = Depends(ConnectorService)
):
    auth = None
    if schema.username and schema.password:
        auth = aiohttp.BasicAuth(schema.username, schema.password)

    return await service.send_request(
        method=schema.method,
        domain=schema.domain,
        url=schema.url,
        payload=schema.payload,
        auth=auth
    )


@router.post("/add-face")
async def create_worker(
        schema: AddFaceSchema.as_form,
        service: ConnectorService = Depends(ConnectorService)
):
    try:
        payload_dict = json.loads(schema.payload)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid payload JSON format")

    file = {schema.image_key: schema.image}
    if not file:
        raise HTTPException(status_code=400, detail="Invalid payload JSON format")

    auth = None
    if schema.username and schema.password:
        auth = aiohttp.BasicAuth(schema.username, schema.password)

    return await service.send_face_request(
        method=schema.method,
        domain=schema.domain,
        url=schema.url,
        payload=payload_dict,
        file=file,
        auth=auth
    )

