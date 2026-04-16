from django.urls import path

from . import views

app_name = "notes"
urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("note/<int:note_id>/", views.note, name="note"),
    path("add/", views.add, name="add"),
]
