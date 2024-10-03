from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import *


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class RetrieveUserView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = get_user_model().objects.all()
    lookup_field = 'email'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user and request.user.email == kwargs['email']:
            return self.retrieve(request, *args, **kwargs)
        else:
            return Response({'message': 'user access denied!!'}, status.HTTP_401_UNAUTHORIZED)


class ListUserView(generics.ListAPIView):
    serializer_class = UserDetailSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAdminUser]


class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = get_user_model().objects.all()
    lookup_field = 'email'
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        if request.user and request.user.email == kwargs['email']:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({'message': 'user access denied!!'}, status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        if request.user and request.user.email == kwargs['email']:
            return self.update(request, *args, **kwargs)
        else:
            return Response({'message': 'user access denied!!'}, status.HTTP_401_UNAUTHORIZED)


class DeleteUserView(generics.DestroyAPIView):
    queryset = get_user_model().objects.all()
    lookup_field = 'email'
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        if request.user and request.user.email == kwargs['email']:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message': 'user deleted successfully!'}, status.HTTP_200_OK)
        else:
            return Response({'message': 'user access denied!!'}, status.HTTP_401_UNAUTHORIZED)
