"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework import routers
from artrec import views

# Authentication imports
from rest_framework.authtoken.views import obtain_auth_token

# Setup a router for artworks, user profiles, and history lines as DB views
router = routers.DefaultRouter()
router.register(r'artworks', views.ArtworkView)
router.register(r'userprofiles', views.UserProfileView)
router.register(r'historylines', views.HistoryLineView)
router.register(r'getnewart', views.GetNewArt, basename='GetNewArt')

# Development router for test functions/apis/etc.
router_dev = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('auth/api-token-auth/', obtain_auth_token, name="api_token_auth"),
    path('auth/register/', views.UserCreate.as_view()),
    path('dev/', include(router_dev.urls)),
]
