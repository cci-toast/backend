import json

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from clients.models import Client
from clients.serializers import ClientSerializer


class ClientList(APIView):
    def get(self, request):
        data = Client.objects.all()
        serializer = ClientSerializer(data, many=True, context={'request': request})
        return Response(serializer.data)


    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


class ClientDetail(APIView):
    def get_object(self, client_pk):
        try:
            return Client.objects.get(pk=client_pk)
        except Client.DoesNotExist:
            raise Http404


    def get(self, request, client_pk):
        client = self.get_object(client_pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)


    def patch(self, request, client_pk):
        client = self.get_object(client_pk)
        serializer = ClientSerializer(client, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


    def delete(self, request, client_pk):
        client = self.get_object(client_pk)
        client.delete()
        serializer = ClientSerializer(client)
        return Response(serializer.data)