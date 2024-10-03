from rest_framework import serializers

from core.models import Hotel, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'room_number', 'price', 'type')


class HotelSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True)

    class Meta:
        model = Hotel
        fields = '__all__'

    def create(self, validated_data):
        rooms_data = validated_data.pop('rooms', None)
        hotel = Hotel.objects.create(**validated_data)

        for room_data in rooms_data:
            Room.objects.create(hotel=hotel, **room_data)

        return hotel

    def update(self, instance, validated_data):
        rooms_data = validated_data.pop('rooms', None)
        hotel = super().update(instance, validated_data)

        for room_data in rooms_data:
            room_instance = Room.objects.get('id')
            room_instance.update(room_data)
            room_instance.save()

        return hotel
