from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics


class ClientDependenceList(generics.ListCreateAPIView):
    lookup_field = 'client'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def post(self, request, *args, **kwargs):
        request.data['client'] = kwargs['client']
        return self.create(request, *args, **kwargs)


class ClientDependenceDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_fields = ['client', 'pk']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
    http_method_names = ['get', 'patch', 'delete']

    def patch(self, request, *args, **kwargs):
        request.data.pop('client', None)
        return self.partial_update(request, *args, **kwargs)
