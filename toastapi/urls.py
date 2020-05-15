from django.urls import path

from toastapi.models import (ActionItem, Children, Debt, Expense, Goal, Partner,
                             Plan)
from toastapi.serializers import (ActionItemSerializer, ChildrenSerializer,
                                  DebtSerializer, ExpenseSerializer,
                                  GoalSerializer, PartnerSerializer,
                                  PlanSerializer)
from toastapi.views import (AdvisorClientList, AdvisorDetail, AdvisorList,
                            ClientDependentDetail, ClientDependentList,
                            ClientDetail, ClientList)

urlpatterns = [
    path('advisors', AdvisorList.as_view()),

    path('advisors/<uuid:pk>', AdvisorDetail.as_view()),

    path('advisors/<uuid:advisor_pk>/clients/<uuid:client_pk>',
         AdvisorClientList.as_view()),

    path('clients', ClientList.as_view()),

    path('clients/<uuid:pk>', ClientDetail.as_view()),

    path('expenses', ClientDependentList.as_view(
        queryset=Expense.objects.all(), serializer_class=ExpenseSerializer)),
    path('expenses/<uuid:pk>', ClientDependentDetail.as_view(
        queryset=Expense.objects.all(), serializer_class=ExpenseSerializer)),

    path('partner', ClientDependentList.as_view(
        queryset=Partner.objects.all(), serializer_class=PartnerSerializer)),
    path('partner/<uuid:pk>', ClientDependentDetail.as_view(
        queryset=Partner.objects.all(), serializer_class=PartnerSerializer)),

    path('children', ClientDependentList.as_view(
        queryset=Children.objects.all(), serializer_class=ChildrenSerializer)),
    path('children/<uuid:pk>', ClientDependentDetail.as_view(
        queryset=Children.objects.all(), serializer_class=ChildrenSerializer)),

    path('goals', ClientDependentList.as_view(
        queryset=Goal.objects.all(), serializer_class=GoalSerializer)),
    path('goals/<uuid:pk>', ClientDependentDetail.as_view(
        queryset=Goal.objects.all(), serializer_class=GoalSerializer)),

    path('plan', ClientDependentList.as_view(
        queryset=Plan.objects.all(), serializer_class=PlanSerializer)),
    path('plan/<uuid:pk>', ClientDependentDetail.as_view(
        queryset=Plan.objects.all(), serializer_class=PlanSerializer)),

    path('debt', ClientDependentList.as_view(
        queryset=Debt.objects.all(), serializer_class=DebtSerializer)),
    path('debt/<uuid:pk>', ClientDependentDetail.as_view(
        queryset=Debt.objects.all(), serializer_class=DebtSerializer)),

    path('action_items', ClientDependentList.as_view(
        queryset=ActionItem.objects.all(), serializer_class=ActionItemSerializer)),
    path('action_items/<uuid:pk>', ClientDependentDetail.as_view(
        queryset=ActionItem.objects.all(), serializer_class=ActionItemSerializer)),
]
