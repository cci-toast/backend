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
from clients import views

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^api/advisors/$', views.advisors_list),
    re_path(r'^api/advisors/(?P<advisor_pk>[0-9]+)$', views.advisors_detail),
    re_path(r'^api/advisors/(?P<advisor_pk>[0-9]+)/clients$', views.advisors_clients),

    re_path(r'^api/clients/$', views.clients_list),
    re_path(r'^api/clients/(?P<client_pk>[0-9]+)$', views.clients_detail),

    re_path(r'^api/clients/(?P<client_pk>[0-9]+)/expenses$', views.expenses_detail),

    re_path(r'^$', views.index, name='index')
]
