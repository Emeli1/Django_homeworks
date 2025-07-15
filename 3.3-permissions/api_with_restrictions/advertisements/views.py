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

        if self.request.user.is_authenticated:
            # Объединяем открытые/закрытые объявления и свои объявления (включая черновики)
            return (Advertisement.objects.filter(status__in=['OPEN', 'CLOSED']) |
                    Advertisement.objects.filter(creator=self.user))
        else:
            # Для неавторизованных - только открытые/закрытые объявления
            return Advertisement.objects.filter(status__in=['OPEN', 'CLOSED'])

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
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
        if self.action in ["create", "destroy"]:
            return [IsAuthenticated(), IsNotOwner()]
        return []
