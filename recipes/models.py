from django.db import models
from django.contrib.auth import get_user_model
from tags.models import Tag


class Recipe(models.Model):
    '''Recipes in the system are represented by this model.'''

    title = models.CharField(max_length=120)
    time_in_minutes = models.PositiveIntegerField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    description = models.TextField(blank=True)
    link = models.CharField(max_length=255, blank=True)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='recipes')

    def __str__(self):
        '''String representation of a recipe.'''
        return self.title
