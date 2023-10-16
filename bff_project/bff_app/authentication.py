from rest_framework.authentication import BaseAuthentication
from .backends import AzureADBackend

class AzureADAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split('Bearer ')[1]
        
        backend = AzureADBackend()
        user = backend.authenticate(request, token=token)
        
        if user:
            return (user, token)
        
        return None