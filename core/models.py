from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    ingredients = models.JSONField(help_text="Store ingredients as JSON data")
    steps = models.TextField(help_text="Detailed steps for the recipe")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)
