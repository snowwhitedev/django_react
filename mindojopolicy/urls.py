"""mindojopolicy URL Configuration

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
from django.urls import path, include
from django.conf.urls import url
from backend.views import getMaxPolicyItemId
from backend.views import checkValidBody

from rest_framework.authtoken.models import Token

urlpatterns = [
    path('', include('frontend.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('backend.api.urls')),
    url(r'^ajax/getMaxPolicyItemId/$', getMaxPolicyItemId, name="getMaxPolicyItemId"),
    url(r'^ajax/checkValidBody/$', checkValidBody, name="checkValidBody"),
    url('markdownx/', include( 'markdownx.urls'))
]

