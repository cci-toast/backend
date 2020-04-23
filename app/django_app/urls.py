"""django_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clients.models import Partner, Expense, Children, Goal, Plan, Debt, ActionItem
from clients.serializers import PartnerSerializer, \
    ExpenseSerializer, ChildrenSerializer, GoalSerializer, \
    PlanSerializer, DebtSerializer, ActionItemSerializer
from clients.views import AdvisorView, ClientView, ClientDependModelView
from django.http import JsonResponse


def home(request):
    return JsonResponse({"hello": "world!"})


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),

    path('api/advisors', AdvisorView.as_view()),

    path('api/clients', ClientView.as_view()),

    path('api/expenses', ClientDependModelView.as_view(
        queryset=Expense.objects.all(), serializer_class=ExpenseSerializer)),

    path('api/partner', ClientDependModelView.as_view(
        queryset=Partner.objects.all(), serializer_class=PartnerSerializer)),

    path('api/children', ClientDependModelView.as_view(
        queryset=Children.objects.all(), serializer_class=ChildrenSerializer)),

    path('api/goals', ClientDependModelView.as_view(
        queryset=Goal.objects.all(), serializer_class=GoalSerializer)),

    path('api/plan', ClientDependModelView.as_view(
        queryset=Plan.objects.all(), serializer_class=PlanSerializer)),

    path('api/debt', ClientDependModelView.as_view(
        queryset=Debt.objects.all(), serializer_class=DebtSerializer)),

    path('api/action_items', ClientDependModelView.as_view(
        queryset=ActionItem.objects.all(), serializer_class=ActionItemSerializer)),
]
