from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, Favorite


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(write_only=True)
    is_superuser = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_staff',
            'is_superuser',
        )

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user



class AdvertisementSerializer(serializers.ModelSerializer):
    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = (
            'id',
            'title',
            'description',
            'creator',
            'status',
            'created_at',
            'draft'
        )

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        queryset = Advertisement.objects.filter(
            creator=self.context['request'].user,
            status='OPEN'
        )
        if len(queryset) >= 10:
            raise ValidationError("The limit of 10 open advertisements has been reached.")

        return data


class FavoriteSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ('advertisement',)
        read_only_fields = ('advertisement',)

    def to_representation(self, instance):
        if not self.context['request'].user.is_staff:
            return super().to_representation(instance)
        else:
            return {
                'user': instance.user.id,
                'advertisement': instance.advertisement.id
            }

    def create(self, validated_data):
        user = self.context['request'].user
        adv_id = self.context['request'].query_params.get('adv')
        advertisement = get_object_or_404(Advertisement, id=adv_id)
        favorite, created = Favorite.objects.get_or_create(user=user, advertisement=advertisement)
        if created:
            return favorite
        else:
            raise serializers.ValidationError('Advertisement is already in favorites.')

