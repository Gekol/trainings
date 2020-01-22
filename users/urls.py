from django.urls import path
from . import views

urlpatterns = [
    path("login", views.LoginFormView.as_view(), name="login"),
    path("register", views.register, name="logout"),
    path("logout", views.my_logout, name="register"),
    path("", views.users, name="users"),
    path(r"deactivate/<str:username>", views.deactivate, name="deactivate"),
    path(r"activate/<str:username>", views.activate, name="activate"),
    path(r"<str:username>/entries/", views.change_password, name="user_entries"),
    path(r"<str:username>/password/", views.change_password, name="password"),
    path("new_user", views.add_user, name="new_user"),

]