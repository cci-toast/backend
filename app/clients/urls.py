from django.urls import path

from clients.models import (ActionItem, Children, Debt, Expense, Goal, Partner,
                            Plan)
from clients.serializers import (ActionItemSerializer, ChildrenSerializer,
                                 DebtSerializer, ExpenseSerializer,
                                 GoalSerializer, PartnerSerializer,
                                 PlanSerializer)
from clients.views import AdvisorView, ClientDependentModelView, ClientView

urlpatterns = [
    path('advisors', AdvisorView.as_view()),

    path('clients', ClientView.as_view()),

    path('expenses', ClientDependentModelView.as_view(
        queryset=Expense.objects.all(), serializer_class=ExpenseSerializer)),

    path('partner', ClientDependentModelView.as_view(
        queryset=Partner.objects.all(), serializer_class=PartnerSerializer)),

    path('children', ClientDependentModelView.as_view(
        queryset=Children.objects.all(), serializer_class=ChildrenSerializer)),

    path('goals', ClientDependentModelView.as_view(
        queryset=Goal.objects.all(), serializer_class=GoalSerializer)),

    path('plan', ClientDependentModelView.as_view(
        queryset=Plan.objects.all(), serializer_class=PlanSerializer)),

    path('debt', ClientDependentModelView.as_view(
        queryset=Debt.objects.all(), serializer_class=DebtSerializer)),

    path('action_items', ClientDependentModelView.as_view(
        queryset=ActionItem.objects.all(), serializer_class=ActionItemSerializer)),

]
