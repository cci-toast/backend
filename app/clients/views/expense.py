import json

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from clients.models import Expense, Client
from clients.serializers import ExpenseSerializer


class ExpenseDetail(APIView):
    def get_object(self, client_pk):
        try:
            return Expense.objects.get(client=client_pk)
        except Expense.DoesNotExist:
            raise Http404


    def get(self, request, client_pk):
        expense = self.get_object(client_pk)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)


    def post(self, request, client_pk):
        if not Client.objects.filter(pk=client_pk).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        # assign client to expense before attempting to save it
        request.data['client'] = client_pk

        serializer = ExpenseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


    def patch(self, request, client_pk):
        expense = self.get_object(client_pk)
        serializer = ExpenseSerializer(expense, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


    def delete(self, request, client_pk):
        expense = self.get_object(client_pk)
        expense.delete()

        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)


