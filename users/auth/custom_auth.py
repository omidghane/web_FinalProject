from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework_simplejwt.tokens import UntypedToken


class Auth(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b"bearer":
            return None
        if len(auth) == 1:
            msg = "Invalid token header. No credentials provided."
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = "Invalid token header. Token string should not contain spaces."
            raise exceptions.AuthenticationFailed(msg)
        try:
            token = UntypedToken(auth[1])
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid token.")
        return token.payload["user_id"], token

    def authenticate_header(self, request):
        return "Bearer"
