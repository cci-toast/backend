from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from clients.models import Advisor, Client
from clients.serializers import AdvisorSerializer, ClientSerializer


class AdvisorList(generics.ListCreateAPIView):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'


class AdvisorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advisor.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AdvisorSerializer


class AdvisorClientList(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, advisor_pk, client_pk):
        advisor = get_object_or_404(Advisor, pk=advisor_pk)
        client = get_object_or_404(Client, pk=client_pk)
        client.advisor = advisor
        client.save()
        serializer = ClientSerializer(client)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, advisor_pk, client_pk):
        advisor = get_object_or_404(Advisor, pk=advisor_pk)
        client = get_object_or_404(Client, pk=client_pk)
        if client.advisor == advisor:
            client.advisor = None
            client.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Client and Advisor mismatched", status=status.HTTP_400_BAD_REQUEST)
