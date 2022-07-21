from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from .serializers import RegistrationSerializer

@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        print(request.data)
        data = {}
        if serializer.is_valid():
            customuser = serializer.save()
            data['response'] = "Registration Successful"
            data['username'] = customuser.username
            data['first_name'] = customuser.first_name
            data['last_name'] = customuser.last_name
            data['email'] = customuser.email
            data['phone'] = customuser.phone
            token = Token.objects.get(user=customuser).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)