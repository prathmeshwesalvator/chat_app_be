import httpx
from fastapi import Request, Response

async def forward_request(base_url: str, endpoint: str, request: Request) -> Response:
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    try:
        method = request.method
        body = await request.body()

        # Only forward essential headers from client
        safe_headers = {}
        if "authorization" in request.headers:
            safe_headers["Authorization"] = request.headers["authorization"]
        if "content-type" in request.headers:
            safe_headers["Content-Type"] = request.headers["content-type"]

        async with httpx.AsyncClient() as client:
            resp = await client.request(
                method=method,
                url=url,
                headers=safe_headers,
                content=body,
                timeout=15.0
            )

        # Remove problematic headers
        excluded_headers = {"content-encoding", "transfer-encoding", "connection", "content-length"}

        response_headers = {
            k: v for k, v in resp.headers.items()
            if k.lower() not in excluded_headers
        }

        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=response_headers,
            media_type=resp.headers.get("content-type")
        )

    except httpx.RequestError as e:
        return Response(
            content=f"Upstream request failed: {str(e)}",
            status_code=502
        )
