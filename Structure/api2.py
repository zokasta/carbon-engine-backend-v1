from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from ..api.plugin.load_plugin import load_plugin
from ..api.models import User

@api_view(['POST'])
def makegame(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        email_validator = load_plugin('Email.py')
        result1 = email_validator.run(email)
    except Exception as e:
        message1 = 'Email is not valid'
        return Response({"error":message1})
    
    try:
        password_validator = load_plugin('Password.py')
        result2 = password_validator.run(password)
    except Exception as e:
        message2 = 'Password is not valid'
        return Response({"error":message2})
    
    try:
        user = User.objects.filter(email=result1).first()
        user.check_password(result2)
    except Exception as e:
        message3 = 'User does not exist'
        return Response({"error":message3})
    
    try:
        token = Token.objects.create(user=user)
    except Exception as e:
        message4 = 'Token could not be created'
        return Response({"error":message4})
    
    return Response({'user':user, 'token':token})