from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter, FavouriteFilter
from advertisements.models import Advertisement, Favourite
from advertisements.permissions import IsOwnerOrReadOnly, IsNotOwner
from advertisements.serializers import AdvertisementSerializer, FavouriteSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        """Получение объявлений для всех пользователей со статусом "открыто" и "закрыто"
        и для пользователя-создателя + объявления со статусом "черновик"."""
        user = self.request.user
        ads = Advertisement.objects.filter(status = 'OPEN'and'CLOSED')

        if user.is_authenticated:
            user_ads = Advertisement.objects.filter(creator=user)
            return (ads | user_ads).distinct()
        else:
            return ads

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "delete"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []


class FavouriteViewSet(ModelViewSet):
    """ViewSet для избранного."""
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated, IsNotOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FavouriteFilter

    def get_permission(self):
        if self.action in ['create', 'delete']:
            return [IsAuthenticated(), IsNotOwner()]
        return []
