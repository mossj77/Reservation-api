from rest_framework import serializers

from core.models import Hotel, Room


class RoomSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

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
            room_instance = Room.objects.get(id=room_data.pop('id', None))
            room_serializer = RoomSerializer(instance=room_instance, data=room_data, partial=True)
            if room_serializer.is_valid():
                room_serializer.save()
            else:
                raise serializers.ValidationError(room_serializer.errors)

        return hotel
