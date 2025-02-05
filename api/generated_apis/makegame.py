from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..plugin.load_plugin import load_plugin

@api_view(['POST'])
def makegame(request):
    password = request.data.get('password')
    email = request.data.get('email')
    try:
        plugin = load_plugin('Plugin_1730005536993')
        email = plugin.run(email)
    except ValueError as ve:
        return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({ 'password': password, 'h1': email })