import requests
from ninja.errors import HttpError
from ninja.security import HttpBearer, HttpBasicAuth
from jose import jwt, JWTError
from django.conf import settings


class CognitoTokenValidator(HttpBearer):
    def authenticate(self, request, token: str):
        try:
            jwks_url = f'https://cognito-idp.{settings.COGNITO_REGION}.amazonaws.com/{settings.COGNITO_POOL_ID}/.well-known/jwks.json'
            jwks = requests.get(jwks_url).json()

            header = jwt.get_unverified_header(token)
            kid = header.get('kid')

            key = next((k for k in jwks['keys'] if k['kid'] == kid), None)
            if key is None:
                raise JWTError("Clave pública no encontrada")

            decoded_token = jwt.decode(
                token,
                key,
                algorithms=['RS256'],
                audience=settings.COGNITO_CLIENT_ID,
                issuer=f'https://cognito-idp.{settings.COGNITO_REGION}.amazonaws.com/{settings.COGNITO_POOL_ID}'
            )
            return decoded_token
        except (JWTError, requests.exceptions.RequestException) as e:
            raise HttpError(401, f"Token inválido: {str(e)}")
