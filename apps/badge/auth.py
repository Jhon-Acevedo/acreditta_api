import re

import boto3
import requests
from botocore.exceptions import ClientError
from django.contrib.auth.models import User
from ninja.errors import HttpError
from ninja.security import HttpBearer, HttpBasicAuth
from jose import jwt, JWTError
from django.conf import settings


def get_cognito_client():
    return boto3.client(
        'cognito-idp',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID_COGITO,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY_COGNITO,
        region_name=settings.COGNITO_REGION
    )


class CognitoAuth(HttpBearer):

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

    @staticmethod
    def get_token_user(email: str, password: str):
        try:
            client = boto3.client('cognito-idp', region_name=settings.COGNITO_REGION)
            response = client.initiate_auth(
                ClientId=settings.COGNITO_CLIENT_ID,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password,
                }
            )
            return {
                'access_token': response['AuthenticationResult']['AccessToken'],
                'refresh_token': response['AuthenticationResult']['RefreshToken'],
            }
        except ClientError as e:
            raise HttpError(401, f"Authentication Error: {str(e)}")

    @staticmethod
    def create_user(email: str, password: str, name: str):
        try:
            validate_password(password)

            client = get_cognito_client()
            response = client.admin_create_user(
                UserPoolId='us-east-2_7BOmm2Y6a',
                Username=email,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'name', 'Value': name},
                    {'Name': 'preferred_username', 'Value': name},
                ],
            )

            client.admin_set_user_password(
                UserPoolId=settings.COGNITO_POOL_ID,
                Username=email,
                Password=password,
                Permanent=True
            )

            user_created = User.objects.get_or_create(
                username=response['User']['Username'],
                defaults={'email': email}
            )

            return {
                'message': 'User created successfully, but you must validate your email in mail provider',
                'email': email,
            }
        except ValueError as e:
            raise HttpError(400, f"Password validation error: {str(e)}")
        except ClientError as e:
            raise HttpError(400, f"User creation error: {str(e)}")


def validate_password(password: str) -> None:
    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters")
    if not re.search(r'[a-z]', password):
        raise ValueError("Password must contain a lower case letter")
    if not re.search(r'[A-Z]', password):
        raise ValueError("Password must contain an upper case letter")
    if not re.search(r'[0-9]', password):
        raise ValueError("Password must contain a number")
    if not re.search(r'[!@#$%^&*(),.?":{}|<> ]', password):
        raise ValueError("Password must contain a special character or a space")
    if password[0] == ' ' or password[-1] == ' ':
        raise ValueError("Password must not contain a leading or trailing space")
