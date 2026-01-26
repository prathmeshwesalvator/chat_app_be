import httpx
from chat_app_be.api_gateway.app.routes.auth_routes import AUTH_SERVICE_URL


async def authVerification(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            AUTH_SERVICE_URL+'/me/',
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        response.raise_for_status()
        return response.json()


