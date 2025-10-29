from fastapi import APIRouter, Depends

from . import schemas
from . import services

router = APIRouter(
    prefix="/tunnel",
    tags=["Worker"]
)



@router.post("/")
async def create_worker(
    schema: schemas.CommonSchema,
    service: services.ConnectorService = Depends(services.ConnectorService)
):
    return await service.send_request(
        method=schema.method,
        scheme=schema.scheme,
        domain=schema.domain,
        port=schema.port,
        path=schema.url,
        params=schema.params,
        payload=schema.payload,
        files=schema.files,
        headers=schema.headers,
        accept=schema.accept,
        content_type=schema.content_type,
        auth_type=schema.auth_type,
        username=schema.username,
        password=schema.password,
        timeout=schema.timeout,
        retries=schema.retries,
        verify_ssl=schema.verify_ssl,
        follow_redirects=schema.follow_redirects,
        response_mode=schema.response_mode,
    )
