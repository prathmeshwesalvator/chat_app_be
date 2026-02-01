from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from django.conf import settings

from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()

        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)

        token = query_params.get("token")

        if token:
            try:
                raw_token = token[0]

                # 1️⃣ Validate token (expiry, signature)
                UntypedToken(raw_token)

                # 2️⃣ Decode payload (SAFE defaults)
                algorithm = settings.SIMPLE_JWT.get("ALGORITHM", "HS256")
                signing_key = settings.SIMPLE_JWT.get(
                    "SIGNING_KEY", settings.SECRET_KEY
                )

                backend = TokenBackend(
                    algorithm=algorithm,
                    signing_key=signing_key,
                )

                payload = backend.decode(raw_token, verify=True)

                # 3️⃣ Resolve user
                user_id = payload.get("user_id")
                scope["user"] = await self.get_user(user_id)

            except (InvalidToken, TokenError, User.DoesNotExist):
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    async def get_user(self, user_id):
        try:
            return await User.objects.aget(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()
