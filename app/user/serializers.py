from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'f_name', 'l_name')
        extra_kwargs = {
            'password': {'min_length': 8, 'write_only': True, 'required': True}
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        exclude = ['password']


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_kwargs = {
            'password': {'min_length': 8, 'write_only': True, 'required': True}
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
