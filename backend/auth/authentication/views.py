from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
import logging

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # Récupère tous les utilisateurs
    serializer_class = UserSerializer  # Utilise le serializer pour convertir les données


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Stockage du JWT dans un cookie HTTP
        response.set_cookie(
            key='access',
            value=response.data['access'],
            httponly=True,  # Protège le cookie des accès JavaScript
            secure=True,    # Assure que le cookie est transmis uniquement sur HTTPS
            samesite='Lax', # Limite l'utilisation du cookie aux requêtes de même site
        )

        return response

from rest_framework.views import APIView

class LogoutView(APIView):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            logger.info("Entered if condition")
            user.is_active = False
            user.save()
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')  # Effacer le cookie contenant le JWT
        return response
    