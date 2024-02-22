from django.urls import path
from core import views

urlpatterns = [
    path("api/recipes/", views.RecipeList.as_view(), name="recipe-list"),
    path(
        "api/recipes/<slug:slug>/", views.RecipeDetail.as_view(), name="recipe-detail"
    ),
    path("api/register/", views.UserRegistrationAPIView.as_view(), name="register"),
    path("api/login/", views.UserLoginAPIView.as_view(), name="login"),
    path("api/logout/", views.UserLogoutAPIView.as_view(), name="logout"),
]
