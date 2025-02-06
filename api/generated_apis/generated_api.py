from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..plugin.load_plugin import load_plugin

@api_view(['POST'])
def makegame(request):
	email = request.data.get('email')
	password = request.data.get('password')
	return Response({ email:email, email:password })