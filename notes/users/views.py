from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from .serializers import userSerializer
from rest_framework import status
from .models import User
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import jwt,datetime
import logging
logger = logging.getLogger('django')
# Create your views here.

# view for user login
@api_view(["POST"])
def user_login(request):
    try:
        user = User.objects.get(email=request.data['email'])
        if not user.check_password(request.data['password']):
            return Response('Wrong password', status=status.HTTP_400_BAD_REQUEST)
        else:
            payload = {
                "id": user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=3600),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, 'some-large-secret-in-production', algorithm='HS256').decode('utf-8')
            return Response({"message": "User logged in successfully", "data": {"token": token}}, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        return Response('User does not exists', status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f'User login:{e}')
        return Response('Something went wrong at our end', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# view for user signup
@api_view(["POST"])
def user_signup(request):
    try:
        serializer = userSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f'User Signup:{e}')
        return Response('Something went wrong at our end', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
