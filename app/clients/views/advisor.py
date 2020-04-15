from clients.models import Advisor
from clients.serializers import AdvisorSerializer
from .generics import ModelView


class AdvisorView(ModelView):
    queryset = Advisor.objects.all()
    model_class = Advisor
    serializer_class = AdvisorSerializer
