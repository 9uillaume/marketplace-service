from django.db import models
from django.utils.text import slugify
from autoslug import AutoSlugField


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(unique=True, populate_from="title")

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    slug = AutoSlugField(unique=True, populate_from="title")

    def __str__(self):
        return self.title
