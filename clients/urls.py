from django.urls import path

from clients.models import (ActionItem, Children, Debt, Expense, Goal, Partner,
                            Plan)
from clients.serializers import (ActionItemSerializer, ChildrenSerializer,
                                 DebtSerializer, ExpenseSerializer,
                                 GoalSerializer, PartnerSerializer,
                                 PlanSerializer)
from clients.views import (AdvisorClientList, AdvisorDetail, AdvisorList,
                           ClientDependenceDetail, ClientDependenceList,
                           ClientDetail, ClientList)

urlpatterns = [
    path('advisors', AdvisorList.as_view()),

    path('advisors/<uuid:pk>', AdvisorDetail.as_view()),

    path('advisors/<uuid:advisor_pk>/clients/<uuid:client_pk>',
         AdvisorClientList.as_view()),

    path('clients', ClientList.as_view()),

    path('clients/<uuid:pk>', ClientDetail.as_view()),

    path('expenses', ClientDependenceList.as_view(
        queryset=Expense.objects.all(), serializer_class=ExpenseSerializer)),
    path('expenses/<uuid:pk>', ClientDependenceDetail.as_view(
        queryset=Expense.objects.all(), serializer_class=ExpenseSerializer)),

    path('partner', ClientDependenceList.as_view(
        queryset=Partner.objects.all(), serializer_class=PartnerSerializer)),
    path('partner/<uuid:pk>', ClientDependenceDetail.as_view(
        queryset=Partner.objects.all(), serializer_class=PartnerSerializer)),

    path('children', ClientDependenceList.as_view(
        queryset=Children.objects.all(), serializer_class=ChildrenSerializer)),
    path('children/<uuid:pk>', ClientDependenceDetail.as_view(
        queryset=Children.objects.all(), serializer_class=ChildrenSerializer)),

    path('goals', ClientDependenceList.as_view(
        queryset=Goal.objects.all(), serializer_class=GoalSerializer)),
    path('goals/<uuid:pk>', ClientDependenceDetail.as_view(
        queryset=Goal.objects.all(), serializer_class=GoalSerializer)),

    path('plan', ClientDependenceList.as_view(
        queryset=Plan.objects.all(), serializer_class=PlanSerializer)),
    path('plan/<uuid:pk>', ClientDependenceDetail.as_view(
        queryset=Plan.objects.all(), serializer_class=PlanSerializer)),

    path('debt', ClientDependenceList.as_view(
        queryset=Debt.objects.all(), serializer_class=DebtSerializer)),
    path('debt/<uuid:pk>', ClientDependenceDetail.as_view(
        queryset=Debt.objects.all(), serializer_class=DebtSerializer)),

    path('action_items', ClientDependenceList.as_view(
        queryset=ActionItem.objects.all(), serializer_class=ActionItemSerializer)),
    path('action_items/<uuid:pk>', ClientDependenceDetail.as_view(
        queryset=ActionItem.objects.all(), serializer_class=ActionItemSerializer)),
]
