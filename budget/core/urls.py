from django.urls import path
from django.contrib.auth import views as auth_views

from .views import index, login

app_name = "core"

urlpatterns = [
    path("", index, name="index"),
    path("login/", login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),    
]