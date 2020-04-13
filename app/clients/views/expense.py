from django.http import Http404
from django.core import validators

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from clients.models import Expense, Client
from clients.serializers import ExpenseSerializer


class ExpenseView(APIView):
    def get_expense_by_client(self, client_id):
        try:
            return Expense.objects.get(client=client_id)
        except (validators.ValidationError, Expense.DoesNotExist):
            raise Http404


    def get_expense_by_id(self, expense_id):
        try:
            return Expense.objects.get(id=expense_id)
        except (validators.ValidationError, Expense.DoesNotExist):
            raise Http404


    def get(self, request):
        client_id = request.data.get('client', None) 
        if client_id is None:
            return Response(u'field "client" required in the url', status=status.HTTP_400_BAD_REQUEST)
        
        expense = self.get_expense_by_client(client_id)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)


    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


    def patch(self, request):
        expense_id = request.data.get('id', None) 
        if expense_id is None:
            return Response(u'field "id" required in the url', status=status.HTTP_400_BAD_REQUEST)

        expense = self.get_expense_by_id(expense_id)
        serializer = ExpenseSerializer(expense, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


    def delete(self, request):
        expense_id = request.data.get('id', None) 
        if expense_id is None:
            return Response(u'field "id" required in the url', status=status.HTTP_400_BAD_REQUEST)

        expense = self.get_expense_by_id(expense_id)
        expense.delete()

        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)


