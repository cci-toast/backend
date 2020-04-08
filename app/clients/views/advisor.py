import json

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from clients.models import Advisor
from clients.serializers import AdvisorSerializer


class AdvisorList(APIView):
    def get(self, request):
        data = Advisor.objects.all()
        serializer = AdvisorSerializer(data, many=True, context={'request': request})
        return Response(serializer.data)


    def post(self, request):
        serializer = AdvisorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


class AdvisorDetail(APIView):
    def get_object(self, advisor_pk):
        try:
            return Advisor.objects.get(pk=advisor_pk)
        except Advisor.DoesNotExist:
            raise Http404


    def get(self, request, advisor_pk):
        advisor = self.get_object(advisor_pk)
        serializer = AdvisorSerializer(advisor)
        return Response(serializer.data)


    def patch(self, request, advisor_pk):
        advisor = self.get_object(advisor_pk)
        serializer = AdvisorSerializer(advisor, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


    def delete(self, request, advisor_pk):
        advisor = self.get_object(advisor_pk)
        advisor.delete()
        serializer = AdvisorSerializer(advisor)
        return Response(serializer.data)