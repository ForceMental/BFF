from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
import jwt
import requests

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
import jwt

class AzureADBackend(BaseBackend):
    def authenticate(self, request, token=None, **kwargs):
        if token is None:
            return None

        try:
            decoded_token = jwt.decode(token, verify=False)
            user_sub = decoded_token.get('sub')
            user_first_name = decoded_token.get('name')
            user_email = decoded_token.get('email')

            # Obtén o crea un usuario en tu base de datos usando el campo 'sub' como 'username'
            user, created = get_user_model().objects.get_or_create(
                username=user_sub,
                defaults={'first_name': user_first_name, 'email': user_email}
            )

            # Si el usuario ya existía, actualiza los campos si es necesario
            if not created:
                update_fields = []
                if user.first_name != user_first_name:
                    user.first_name = user_first_name
                    update_fields.append('first_name')

                if user.email != user_email:
                    user.email = user_email
                    update_fields.append('email')

                if update_fields:
                    user.save(update_fields=update_fields)

            return user
        except jwt.DecodeError:
            return None

    def get_user(self, user_sub):
        try:
            return get_user_model().objects.get(username=user_sub)
        except get_user_model().DoesNotExist:
            return None
