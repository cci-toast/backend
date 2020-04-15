from django.http import Http404
from django.core import validators

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from clients.models import Client
from clients.serializers import IDSerializer, ClientSerializer


class ClientView(APIView):
    def get_client_by_id(self, client_id):
        try:
            return Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            raise Http404


    def get(self, request):
        client_id = request.data.get('id', None)
        if client_id is None:
            # get list of clients if no id provided
            data = Client.objects.all()
            serializer = ClientSerializer(data, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            # retrieve info of a client
            id_serializer = IDSerializer(data=request.data)
            if not id_serializer.is_valid():
                return Response(id_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            client_id = id_serializer.data['id']
            client = self.get_client_by_id(client_id)
            serializer = ClientSerializer(client)
            return Response(serializer.data)


    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


    def patch(self, request):
        id_serializer = IDSerializer(data=request.data) 
        if not id_serializer.is_valid():
            return Response(id_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        client_id = id_serializer.data['id']
        client = self.get_client_by_id(client_id)
        serializer = ClientSerializer(client, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


    def delete(self, request):
        id_serializer = IDSerializer(data=request.data) 
        if not id_serializer.is_valid():
            return Response(id_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        client_id = id_serializer.data['id']
        client = self.get_client_by_id(client_id)
        client.delete()
        serializer = ClientSerializer(client)
        return Response(serializer.data)