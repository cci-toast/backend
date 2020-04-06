import json

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from clients.models import Advisor, Client
from clients.serializers import AdvisorSerializer, ClientSerializer


class ClientAdvisorList(APIView):
    def get_advisor(self, advisor_pk):
        try:
            return Advisor.objects.get(pk=advisor_pk)
        except Advisor.DoesNotExist:
            raise Http404


    def get_client(self, client_pk):
        try:
            return Client.objects.get(pk=client_pk)
        except Client.DoesNotExist:
            raise Http404


    def get(self, request, advisor_pk):
        if not Advisor.objects.filter(pk=advisor_pk).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        clients = Client.objects.filter(advisor=advisor_pk)
        serializer = ClientSerializer(clients, many=True, context={'request': request})
        return Response(serializer.data)


    def patch(self, request, advisor_pk):
        # parse client id in the request body
        body = json.loads(request.body)
        try:
            client_pk = body['id']
        except KeyError:
            return Response(u'client field "id" required in the request body', status=status.HTTP_400_BAD_REQUEST)

        advisor = self.get_advisor(advisor_pk)
        client = self.get_client(client_pk)

        # add client to the advisor
        client.advisor = advisor
        client.save()
        serializer = ClientSerializer(client)
        return Response(serializer.data)


    def delete(self, request, advisor_pk):
        # parse client id in the request body
        body = json.loads(request.body)
        try:
            client_pk = body['id']
        except KeyError:
            return Response(u'client field "id" required in the request body', status=status.HTTP_400_BAD_REQUEST)

        advisor = self.get_advisor(advisor_pk)
        client = self.get_client(client_pk)

        # client must be under advisor management
        if client.advisor != advisor.id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # remove client from the advisor management
        client.advisor = None
        client.save()
        serializer = ClientSerializer(client)
        return Response(serializer.data)