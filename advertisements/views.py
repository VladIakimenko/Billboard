from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser, User
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favorite
from advertisements.serializers import AdvertisementSerializer, FavoriteSerializer, UserSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            response.data['token'] = token.key
        return response


class AdvertisementViewSet(ModelViewSet):
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Advertisement.objects.all()
        elif user.is_anonymous:
            queryset = Advertisement.objects.filter(draft=False)
        else:
            queryset = Advertisement.objects.filter(
                Q(draft=False) |
                Q(draft=True, creator=user)
            )
        return queryset

    def get_permissions(self):
        if self.request.user.is_staff or self.action not in [
            'update',
            'partial_update',
            'destroy',
            'create'
        ]:
            return []
        else:
            if self.action != 'create':
                obj = get_object_or_404(Advertisement, id=self.kwargs['pk'])
                if self.request.user != obj.creator:
                    raise PermissionDenied("User is not the owner of the advertisement or not authenticated")
            return [IsAuthenticated()]


class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_staff:
            return Favorite.objects.all()
        else:
            return Favorite.objects.filter(user=user)

    def get_permissions(self):
        return [IsAuthenticated()]
