from rest_framework import viewsets, mixins

from .serializers import *


class HotelViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()
