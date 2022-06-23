
"""newsApi URL Configuration
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
from django.urls import path,include
from newsapp import views
from knox import views as knox_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/news/', views.news),
    path('api/sources/', views.update_sources),
    path('api/account/', views.UserAccountDetail.as_view()),
    path('api/newsfeed/', views.UserNewsfeed.as_view()),
    path('api/register/', views.RegisterAPI.as_view()),
    path('api/login/', views.LoginAPI.as_view()),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/',knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]