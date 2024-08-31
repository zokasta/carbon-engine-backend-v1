import re
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def makegame(request):
    username = request.data.get('username')
    return Response({ 'email': username })