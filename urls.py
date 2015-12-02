"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from tb import views
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^logout_request/', views.logout_request, name='logout_request'),
    url(r'^login_request/', views.login_request, name='login_request'),
    url(r'^change_title/', views.change_title, name='change_title'),
    url(r'^change_header/', views.change_header, name='change_header'),
    url(r'^change_requirement/', views.change_requirement, name='change_requirement'),
    url(r'^delete_requirement/', views.delete_requirement, name='delete_requirement'),
    url(r'^add_step/', views.add_step, name='add_step'),
    url(r'^add_substep/', views.add_substep, name='add_substep'),
    url(r'^delete_step/', views.delete_step, name='delete_step'),
    url(r'^delete_substep/', views.delete_substep, name='delete_substep'),
    url(r'^add_code/', views.add_code, name='add_code'),
    url(r'^delete_code/', views.delete_code, name='delete_code'),
    url(r'^add_image/', views.add_image, name='add_image'),
    url(r'^delete_image/', views.delete_image, name='delete_image'),

    url(r'^live/', views.live, name='live'),
    url(r'^(?P<name>\w+)/$', views.pub_view, name = 'pub_view'),
]
