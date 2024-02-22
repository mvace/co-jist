from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ["id", "title", "slug", "ingredients", "steps", "author"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
        )  # we're overriding the create method and using create_user method instead which handles hashing the password to provide security - the create method would just store the password as a plain text
        return user
