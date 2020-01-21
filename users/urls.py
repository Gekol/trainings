from django.urls import path
from . import views

urlpatterns = [
    path("login", views.LoginFormView.as_view(), name="login"),
    path("register", views.register, name="logout"),
    path("logout", views.my_logout, name="register"),
]