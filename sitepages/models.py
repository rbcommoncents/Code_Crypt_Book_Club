from django.db import models

class Drink(models.Model):
    CATEGORY_CHOICES = [
        ('coffee', 'Coffee'),
        ('tea', 'Tea'),
        ('hot chocolate', 'Hot Chocolate'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    ingredients = models.TextField(help_text="List ingredients separated by commas")
    method = models.TextField(help_text="Preparation method")

    def __str__(self):
        return self.name
