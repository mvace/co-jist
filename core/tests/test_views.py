from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from core.models import Recipe


class RecipeAPITests(APITestCase):

    def setUp(self):
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


class UserRegistrationAPITestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "complex_password",
        }

    def test_user_registration_success(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")

    def test_user_registration_with_missing_data(self):
        incomplete_data = self.user_data.copy()
        del incomplete_data["username"]
        response = self.client.post(self.register_url, incomplete_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_with_invalid_data(self):
        invalid_data = self.user_data.copy()
        invalid_data["email"] = "invalid_email"
        response = self.client.post(self.register_url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_user_registration(self):
        self.client.post(self.register_url, self.user_data, format="json")
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)


class UserLoginAPITestCase(APITestCase):
    def setUp(self):
        self.login_url = reverse("login")
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.correct_credentials = {
            "username": "testuser",
            "password": "testpassword",
        }
        self.incorrect_credentials = {
            "username": "testuser",
            "password": "wrongpassword",
        }

    def test_successfull_login(self):
        response = self.client.post(
            self.login_url, self.correct_credentials, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unsuccessfull_login(self):
        response = self.client.post(
            self.login_url, self.incorrect_credentials, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("token", response.data)

    def test_no_password_login(self):
        response = self.client.post(
            self.login_url, {"username": "testuser"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("token", response.data)


class UserLogoutAPITestCase(APITestCase):
    def setUp(self):
        self.logout_url = reverse("logout")
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_successful_logout(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_logout_without_being_logged_in(self):
        self.client.credentials()
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
