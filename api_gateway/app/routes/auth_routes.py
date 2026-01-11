# app/routes/auth_routes.py
from fastapi import APIRouter, Request
from app.services.service_forward import forward_request

router = APIRouter()


# AUTH_SERVICE_URL = "https://auth-service-xdh9.onrender.com"
AUTH_SERVICE_URL = "http://0.0.0.0:8001"


@router.get("/")
async def root_proxy(request: Request):
    return await forward_request(AUTH_SERVICE_URL, "/", request)

@router.get('/me/')
async def current_user_proxy(request : Request):
    return await forward_request(AUTH_SERVICE_URL, "/me/" , request)

@router.post('/token/')
async def token_proxy(request : Request):
    return await forward_request(base_url=AUTH_SERVICE_URL , endpoint='/token/' , request=request)


@router.post('/token/refresh/')
async def refresh_token_proxy(request : Request):
    return await forward_request(base_url=AUTH_SERVICE_URL , endpoint='/token/refresh/' , request=request)

@router.get('/check/')
async def check_token_proxy(request : Request):
    return await forward_request(base_url=AUTH_SERVICE_URL , endpoint='/check/' , request=request)


@router.post('/signup/')
async def signup_proxy(request : Request):
    print(AUTH_SERVICE_URL+'/signup/')
    return await forward_request(base_url=AUTH_SERVICE_URL , endpoint='/signup/' , request=request)

