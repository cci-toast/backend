from django.urls import path

from clients.models import (ActionItem, Children, Debt, Expense, Goal, Partner,
                            Plan)
from clients.serializers import (ActionItemSerializer, ChildrenSerializer,
                                 DebtSerializer, ExpenseSerializer,
                                 GoalSerializer, PartnerSerializer,
                                 PlanSerializer)
from clients.views import (AdvisorDetail, AdvisorList, ClientDependenceDetail,
                           ClientDependenceList, ClientDetail, ClientList)

urlpatterns = [
    path('advisors', AdvisorList.as_view()),

    path('advisors/<uuid:pk>', AdvisorDetail.as_view()),

    path('clients', ClientList.as_view()),

    path('clients/<uuid:pk>', ClientDetail.as_view()),

    path('clients/<uuid:client>/expenses', ClientDependenceList.as_view(
        queryset=Expense.objects.all(), serializer_class=ExpenseSerializer)),
    path('clients/<uuid:client>/expenses/<uuid:pk>', ClientDependenceDetail.as_view(
        queryset=Expense.objects.all(), serializer_class=ExpenseSerializer)),

    path('clients/<uuid:client>/partner', ClientDependenceList.as_view(
        queryset=Partner.objects.all(), serializer_class=PartnerSerializer)),
    path('clients/<uuid:client>/partner/<uuid:pk>', ClientDependenceDetail.as_view(
        queryset=Partner.objects.all(), serializer_class=PartnerSerializer)),

    path('clients/<uuid:client>/children', ClientDependenceList.as_view(
        queryset=Children.objects.all(), serializer_class=ChildrenSerializer)),
    path('clients/<uuid:client>/children/<uuid:pk>', ClientDependenceDetail.as_view(
        queryset=Children.objects.all(), serializer_class=ChildrenSerializer)),

    path('clients/<uuid:client>/goals', ClientDependenceList.as_view(
        queryset=Goal.objects.all(), serializer_class=GoalSerializer)),
    path('clients/<uuid:client>/goals/<uuid:pk>', ClientDependenceDetail.as_view(
        queryset=Goal.objects.all(), serializer_class=GoalSerializer)),

    path('clients/<uuid:client>/plan', ClientDependenceList.as_view(
        queryset=Plan.objects.all(), serializer_class=PlanSerializer)),
    path('clients/<uuid:client>/plan/<uuid:pk>', ClientDependenceDetail.as_view(
        queryset=Plan.objects.all(), serializer_class=PlanSerializer)),

    path('clients/<uuid:client>/debt', ClientDependenceList.as_view(
        queryset=Debt.objects.all(), serializer_class=DebtSerializer)),
    path('clients/<uuid:client>/debt/<uuid:pk>', ClientDependenceDetail.as_view(
        queryset=Debt.objects.all(), serializer_class=DebtSerializer)),

    path('clients/<uuid:client>/action_items', ClientDependenceList.as_view(
        queryset=ActionItem.objects.all(), serializer_class=ActionItemSerializer)),
    path('clients/<uuid:client>/action_items/<uuid:pk>', ClientDependenceDetail.as_view(
        queryset=ActionItem.objects.all(), serializer_class=ActionItemSerializer)),
]
