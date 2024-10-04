from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import *


class HotelViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()

    def get_serializer_class(self):
        if self.action == 'upload_image':
            return HotelImageSerializer
        else:
            return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        hotel = self.get_object()
        serializer = self.get_serializer(
            hotel,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
