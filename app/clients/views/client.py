from clients.models import Client
from clients.serializers import ClientSerializer

from .generics import ModelView


class ClientView(ModelView):
    queryset = Client.objects.all()
    model_class = Client
    serializer_class = ClientSerializer
