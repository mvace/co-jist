from django.urls import path
from core import views

urlpatterns = [
    path("recipes/", views.RecipeList.as_view(), name="recipe-list"),
    path("recipes/<slug:slug>/", views.RecipeDetail.as_view(), name="recipe-detail"),
]
