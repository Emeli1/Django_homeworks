from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, Favourite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию

        creator = self.context['request'].user   # Получаем текущего пользователя

        # Проверка, может ли пользователь менять статус чужого объявления
        if self.instance and data.get('status') != self.instance.status:
            # Проверяем, является ли текущий пользователь создателем объявления
            if self.instance.creator != creator:
                raise serializers.ValidationError(
                    'Вы не можете поменять статус этого объявления, так как не являетесь его создателем.')

        if self.instance is None:
            if data.get("status") == "OPEN":
                if Advertisement.objects.filter(creator=creator, status="OPEN").count() == 10:
                    raise serializers.ValidationError(f'Доступно не более 10 открытых объявлений')

        return data


class FavouriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        read_only=True,
    )
    advertisement = AdvertisementSerializer(
        read_only=True
    )

    class Meta:
        model = Favourite
        fields = ('user', 'advertisement')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['advertisement'] = self.context['request']['advertisement']
        return super().create(validated_data)
