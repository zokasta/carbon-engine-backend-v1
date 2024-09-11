from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..plugin.load_plugin import load_plugin

@api_view(['POST'])
def makegame(request):
    username = request.data.get('username')
    password = request.data.get('password')
    return Response({ 'email': username, 'password': password })