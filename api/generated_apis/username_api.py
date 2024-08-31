from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def generated_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    return Response({ 'username': username, 'password': password })