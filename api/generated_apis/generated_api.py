from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..plugin.load_plugin import load_plugin

@api_view(['POST'])
def makegame(request):
	email = request.data.get('email')
	password = request.data.get('password')
	try:
		email_validator = load_plugin('email_validator')
		email_validator.run(email)
	except:
		return Response({'error':'Invalid email address'})
	return Response({ email:email, email:password })