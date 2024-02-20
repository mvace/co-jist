from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Recipe
from django.db.utils import IntegrityError


class UserTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpass123"))


class RecipeModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser", password="testpass123"
        )

    def test_create_recipe(self):
        recipe = Recipe.objects.create(
            title="Tea",
            ingredients='[{"name": "Water", "quantity": "250ml"}]',
            steps="1. Boil water\n2. add Tea",
            author=self.user,
        )

        self.assertEqual(recipe.title, "Tea")
        self.assertIsNotNone(recipe.slug)
        self.assertIn("Water", recipe.ingredients)
        self.assertTrue("Boil water" in recipe.steps)
        self.assertEqual(recipe.author, self.user)

    def test_slug_generation(self):

        recipe = Recipe(
            title="Unique Recipe Title",
            ingredients='[{"name": "Water", "quantity": "250ml"}]',
            steps="1. Boil water\n2. add Tea",
            author=self.user,
        )
        recipe.save()
        self.assertEqual(recipe.slug, "unique-recipe-title")

    def test_recipe_unique_constraints(self):

        Recipe.objects.create(
            title="Another Recipe",
            slug="another-recipe",
            ingredients="[]",
            steps="",
            author=self.user,
        )
        with self.assertRaises(IntegrityError):
            Recipe.objects.create(
                title="Another Recipe",
                slug="another-recipe",
                ingredients="[]",
                steps="",
                author=self.user,
            )
