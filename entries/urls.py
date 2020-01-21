from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_main, name="main_page"),
    path("entries", views.show_entries, name="entries"),
    path("add_entry", views.add_entry, name="add_entry"),
    path(r"delete/<int:id>", views.delete_entry, name="delete_entry"),
    path("statistics", views.statistics, name="statistics"),
]