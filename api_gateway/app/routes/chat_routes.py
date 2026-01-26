from fastapi import APIRouter, Request
from app.services.service_forward import forward_request

router = APIRouter()


CHAT_SERVICE_URL = "http://0.0.0.0:8002"


@router.get('')
async def root_proxy (request : Request):
    return await forward_request(CHAT_SERVICE_URL , '/' , request)


