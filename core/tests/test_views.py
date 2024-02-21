from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Recipe


class RecipeAPITests(APITestCase):

    def setUp(self):
        # Setup run before every test method.
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        Recipe.objects.create(
            title="Test Recipe",
            slug="test-recipe",
            ingredients='{"ingredient": "value"}',
            steps="Test steps",
            author=self.user,
        )

    def test_create_recipe(self):
        """
        Ensure we can create a new recipe object.
        """
        url = reverse("recipe-list")
        data = {
            "title": "New Test Recipe",
            "slug": "new-test-recipe",
            "ingredients": '{"ingredient": "new value"}',
            "steps": "New test steps",
            "author": self.user.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 2)
        self.assertEqual(
            Recipe.objects.get(slug="new-test-recipe").title, "New Test Recipe"
        )

    def test_retrieve_recipe(self):
        """
        Ensure we can retrieve a recipe object.
        """
        url = reverse("recipe-detail", args=["test-recipe"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Recipe")

    def test_update_recipe(self):
        """
        Ensure we can update an existing recipe object.
        """
        url = reverse("recipe-detail", args=["test-recipe"])
        data = {
            "title": "Updated Test Recipe",
            "ingredients": '{"ingredient": "updated value"}',
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Recipe.objects.get(slug="updated-test-recipe").title, "Updated Test Recipe"
        )

    def test_delete_recipe(self):
        """
        Ensure we can delete a recipe object.
        """
        url = reverse("recipe-detail", args=["test-recipe"])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0)
