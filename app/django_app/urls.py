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
from django.urls import path, re_path
from clients.views import AdvisorList, AdvisorDetail, \
    ClientList, ClientDetail, \
    ClientAdvisorList, \
    ExpenseDetail

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^api/advisors$', AdvisorList.as_view()),
    re_path(r'^api/advisors/(?P<advisor_pk>[0-9]+)$', AdvisorDetail.as_view()),
    re_path(r'^api/advisors/(?P<advisor_pk>[0-9]+)/clients$', ClientAdvisorList.as_view()),

    re_path(r'^api/clients$', ClientList.as_view()),
    re_path(r'^api/clients/(?P<client_pk>[0-9]+)$', ClientDetail.as_view()),

    re_path(r'^api/clients/(?P<client_pk>[0-9]+)/expenses$', ExpenseDetail.as_view()),
]
