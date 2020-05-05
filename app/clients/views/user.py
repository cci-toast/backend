from django.contrib.auth.models import User
from rest_framework import viewsets
from clients.permissions.permissions import IsAuthenticatedOrWriteOnly
from clients.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrWriteOnly,)
    filterset_fields = "__all__"
    ordering_fields = "__all__"

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
