from django.urls import path
from . import views

app_name = 'encyclopedia'

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("newentry", views.newentry, name="newentry"),
    path("editentry/<str:entry_title>", views.editentry, name="editentry"),
    path("randompage", views.randompage, name="randompage")
]