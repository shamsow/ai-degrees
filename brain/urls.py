from django.urls import path
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("ajax/validate_name", views.validate_name, name="validate_name"), 
  path("ajax/find_path", views.find_path, name="find_path")
]