from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def generated_api(request):
    email = request.data.get('email')
    password = request.data.get('password')
    return Response({ 'email': email, 'password': password })