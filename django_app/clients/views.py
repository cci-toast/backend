import json
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Client, Advisor, Expense
from .serializers import ClientSerializer, AdvisorSerializer, ExpenseSerializer


def index(request):
    return HttpResponse("Welcome to Toast! Go to localhost:8000/api/clients to hit the first endpoint")


'''
advisor API
'''
def post_advisor(request):
    serializer = AdvisorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_advisors(request):
    data = Advisor.objects.all()
    serializer = AdvisorSerializer(data, many=True, context={'request': request})
    return Response(serializer.data)


def get_advisor(request, advisor_pk):
    try:
        advisor = Advisor.objects.get(pk=advisor_pk)
    except Advisor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AdvisorSerializer(advisor)
    return Response(serializer.data)


def patch_advisor(request, advisor_pk):
    try:
        advisor = Advisor.objects.get(pk=advisor_pk)
    except Advisor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AdvisorSerializer(advisor, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_advisor(request, advisor_pk):
    try:
        advisor = Advisor.objects.get(pk=advisor_pk)
    except Advisor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    advisor.delete()
    serializer = AdvisorSerializer(advisor)
    return Response(serializer.data)


@api_view(['POST', 'GET'])
def advisors_list(request):
    if request.method == 'POST':
        return post_advisor(request)

    if request.method == 'GET':
        return get_advisors(request)


@api_view(['GET', 'PATCH', 'DELETE'])
def advisors_detail(request, advisor_pk):
    if request.method == 'GET':
        return get_advisor(request, advisor_pk)

    if request.method == 'PATCH':
        return patch_advisor(request, advisor_pk)

    if request.method == 'DELETE':
        return delete_advisor(request, advisor_pk)


'''
advisors clients relationship
'''
def get_client_from_body(request):
    # parse client id in the request body
    body = json.loads(request.body)
    try:
        client_pk = body['id']
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # find the client
    try:
        client = Client.objects.get(pk=client_pk)
        return client
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


def get_advisors_clients(request, advisor_pk):
    if not Advisor.objects.filter(pk=advisor_pk).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    clients = Client.objects.filter(advisor=advisor_pk)
    serializer = ClientSerializer(clients, many=True, context={'request': request})
    return Response(serializer.data)


def patch_advisors_clients(request, advisor_pk):
    # get advisor
    try:
        advisor = Advisor.objects.get(pk=advisor_pk)
    except Advisor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get client
    data = get_client_from_body(request)
    if type(data) is Response:
        return data
    client = data

    # add client to the advisor
    client.advisor = advisor
    client.save()
    serializer = ClientSerializer(client)
    return Response(serializer.data)


def delete_advisors_clients(request, advisor_pk):
    # get advisor
    try:
        advisor = Advisor.objects.get(pk=advisor_pk)
    except Advisor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get client
    data = get_client_from_body(request)
    if type(data) is Response:
        return data
    client = data
    
    # client must be under advisor management
    if client.advisor != advisor.id:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # remove client from the advisor management
    advisor.client_set.remove(client)
    serializer = ClientSerializer(client)
    return Response(serializer.data)


@api_view(['GET', 'PATCH', 'DELETE'])
def advisors_clients(request, advisor_pk):
    if request.method == 'GET':
        return get_advisors_clients(request, advisor_pk)

    if request.method == 'PATCH':
        return patch_advisors_clients(request, advisor_pk)

    if request.method == 'DELETE':
        return delete_advisors_clients(request, advisor_pk)


'''
client API
'''
def post_client(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_clients(request):
    data = Client.objects.all()
    serializer = ClientSerializer(data, many=True, context={'request': request})
    return Response(serializer.data)


def get_client(request, client_pk):
    try:
        client = Client.objects.get(pk=client_pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ClientSerializer(client)
    return Response(serializer.data)


def patch_client(request, client_pk):
    try:
        client = Client.objects.get(pk=client_pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ClientSerializer(client, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_client(request, client_pk):
    try:
        client = Client.objects.get(pk=client_pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    client.delete()
    serializer = ClientSerializer(client)
    return Response(serializer.data)


@api_view(['POST', 'GET'])
def clients_list(request):
    if request.method == 'POST':
        return post_client(request)

    if request.method == 'GET':
        return get_clients(request)


@api_view(['GET', 'PATCH', 'DELETE'])
def clients_detail(request, client_pk):
    if request.method == 'GET':
        return get_client(request, client_pk)

    if request.method == 'PATCH':
        return patch_client(request, client_pk)

    if request.method == 'DELETE':
        return delete_client(request, client_pk)


'''
expense API
'''
def post_expense(request, client_pk):
    if not Client.objects.filter(pk=client_pk).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    # assign client to expense before attempting to save it
    request.data['client'] = client_pk

    serializer = ExpenseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_expense(request, client_pk):
    try:
        expense = Expense.objects.get(client=client_pk)
    except Expense.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ExpenseSerializer(expense)
    return Response(serializer.data)


def patch_expense(request, client_pk):
    try:
        expense = Expense.objects.get(client=client_pk)
    except Expense.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ExpenseSerializer(expense, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_expense(request, client_pk):
    try:
        expense = Expense.objects.get(client=client_pk)
    except Expense.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    expense.delete()

    serializer = ExpenseSerializer(expense)
    return Response(serializer.data)


@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
def expenses_detail(request, client_pk):
    if request.method == 'POST':
        return post_expense(request, client_pk)

    if request.method == 'GET':
        return get_expense(request, client_pk)

    if request.method == 'PATCH':
        return patch_expense(request, client_pk)

    if request.method == 'DELETE':
        return delete_expense(request, client_pk)
