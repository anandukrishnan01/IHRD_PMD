from __future__ import annotations

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

from .serializers import LoginSerializer
from .serializers import UserSerializer
from .serializers import RegisterSerializer
from core_viewsets.custom_viewsets import CreateViewSet

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.db import IntegrityError

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import WorldPopulation,Token
from .forms import WorldPopulationSearchForm
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action

class RegisterViewSet(CreateViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterSerializer
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):
        # Deserialize the request data using the RegisterSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        first_name = serializer.validated_data.get('first_name')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        phone_number = serializer.validated_data.get('phone_number')

        # Validate phone number 
        if not (phone_number and phone_number.isdigit() and len(phone_number) == 10):
            return Response({'code': 400, 'message': 'Invalid phone number format.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate password strength
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({'code': 400, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Validate proper email format
        try:
            validate_email(email)
        except ValidationError:
            return Response({'code': 400, 'message': 'Invalid email format.'}, status=status.HTTP_400_BAD_REQUEST)


        # Create user
        try:
            user = get_user_model().objects.create_user(
                email=email, 
                password=password, 
                phone_number=phone_number,
                first_name=first_name
                )

            return Response({'code': 200, 'message': 'success', 'user_id': user.pk}, status=status.HTTP_200_OK)

        except IntegrityError:
                return Response({'code': 400, 'message': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(CreateViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Update last login time
            user.last_login = timezone.now()
            user.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Create and save Token instance
            token = Token.objects.create(
                user_id=user,
                refresh_token=refresh_token,
                access_token=access_token,
            )
            return Response(
                {
                    'code': 200,
                    'message': 'success',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user_id': user.pk,
                    'name': user.first_name,
                    'email': user.email,
                    'last_login': user.last_login,
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'code': 401, 'message': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )



class MeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    

def home(request):
    form = WorldPopulationSearchForm(request.GET)
    data = WorldPopulation.objects.all()

    search_results = []

    if request.method == 'GET':
        country_name = request.GET.get('country', '')
        if country_name:
            # Perform filtering based on the country_name
            search_results = WorldPopulation.objects.filter(country__icontains=country_name)

    return render(request, 'home.html', {'data': data, 'search_results': search_results})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get all tokens associated with the user and delete them
        user_tokens = Token.objects.filter(user_id=request.user)
        user_tokens.delete()

        return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)