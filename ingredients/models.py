from django.db import models
from django.conf import settings

# Create your models here.


class Ingredient(models.Model):
    '''Ingredients for recipes.'''
    name = models.CharField(max_length=120)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
