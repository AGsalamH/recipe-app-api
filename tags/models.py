from django.db import models
from django.contrib.auth import get_user_model


class Tag(models.Model):
    '''Tag model representation.'''
    name = models.CharField(max_length=70)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name
