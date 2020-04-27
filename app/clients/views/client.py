from clients.models import Client
from clients.serializers import ClientSerializer
from .generics import ModelView
from .permissions import IsOwnerOrReadOnly

class ClientView(ModelView):
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = Client.objects.all()
    model_class = Client
    serializer_class = ClientSerializer
