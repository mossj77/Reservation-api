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

    def validate(self, attr):
        rooms_data = attr.get('rooms', None)
        room_numbers = [room['room_number'] for room in rooms_data]

        if len(room_numbers) != len(set(room_numbers)):
            raise serializers.ValidationError({'room_number': 'Room numbers must be unique over a hotel rooms.'})

        return attr

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

            # validate room_number
            updated_room_number = room_data.get('room_number')
            if updated_room_number and room_instance.room_number != updated_room_number:
                all_room_numbers = [room.room_number for room in Room.objects.filter(hotel=hotel)]
                if all_room_numbers.__contains__(updated_room_number):
                    raise serializers.ValidationError(
                        {'room_number': 'Room numbers must be unique over a hotel rooms.'}
                    )

            room_serializer = RoomSerializer(instance=room_instance, data=room_data, partial=True)
            if room_serializer.is_valid():
                room_serializer.save()
            else:
                raise serializers.ValidationError(room_serializer.errors)

        return hotel
