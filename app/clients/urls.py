from django.urls import path, include

from clients.models import Partner, Expense, Children, Goal, Plan, Debt, ActionItem
from clients.serializers import PartnerSerializer, \
    ExpenseSerializer, ChildrenSerializer, GoalSerializer, \
    PlanSerializer, DebtSerializer, ActionItemSerializer
from clients.views import AdvisorView, ClientView, ClientDependentModelView

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

    path('admin/', include('rest_framework.urls')),
]
