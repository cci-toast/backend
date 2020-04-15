from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from clients.models import Advisor, Client
from clients.serializers import IDSerializer, AdvisorSerializer, ClientSerializer


class AdvisorClientView(APIView):
    def get(self, request):
        id_serializer = IDSerializer(data=request.data) 
        if not id_serializer.is_valid():
            return Response(id_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        advisor_id = id_serializer.data['id']
        if not Advisor.objects.filter(id=advisor_id).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        clients = Client.objects.filter(advisor=advisor_id)
        serializer = ClientSerializer(clients, many=True, context={'request': request})
        return Response(serializer.data)


class AdvisorView(APIView):
    def get_advisor_by_id(self, advisor_id):
        try:
            return Advisor.objects.get(id=advisor_id)
        except Advisor.DoesNotExist:
            raise Http404


    def get(self, request):
        advisor_id = request.data.get('id', None) 
        if advisor_id is None:
            # get list of advisors if no id provided
            data = Advisor.objects.all()
            serializer = AdvisorSerializer(data, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            # retrieve info of a advisor
            id_serializer = IDSerializer(data=request.data)
            if not id_serializer.is_valid():
                return Response(id_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            advisor_id = id_serializer.data['id']
            advisor = self.get_advisor_by_id(advisor_id)
            serializer = AdvisorSerializer(advisor)
            return Response(serializer.data)


    def post(self, request):
        serializer = AdvisorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


    def patch(self, request):
        id_serializer = IDSerializer(data=request.data) 
        if not id_serializer.is_valid():
            return Response(id_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        advisor_id = id_serializer.data['id']
        advisor = self.get_advisor_by_id(advisor_id)
        serializer = AdvisorSerializer(advisor, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


    def delete(self, request):
        id_serializer = IDSerializer(data=request.data) 
        if not id_serializer.is_valid():
            return Response(id_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        advisor_id = id_serializer.data['id']
        advisor = self.get_advisor_by_id(advisor_id)
        advisor.delete()
        serializer = AdvisorSerializer(advisor)
        return Response(serializer.data)