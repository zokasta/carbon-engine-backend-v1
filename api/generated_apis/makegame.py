from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..plugin.load_plugin import load_plugin

@api_view(['POST'])
def makegame(request):
	email = request.data.get('email')
	password = request.data.get('password')
	try:
		email_validator = load_plugin('Email.py')
		result = email_validator.run(email)
	except Exception as e:
		return Response({'error':str(e)})
	return Response({ "password":password, "email":result })