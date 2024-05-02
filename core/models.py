import uuid
from django.db import models


class BaseModel(models.Model):
    '''Timestamped Base class for database models'''
    id = models.UUIDField(
                            verbose_name='ID',
                            primary_key=True,
                            serialize=False,
                            auto_created=True,
                            default=uuid.uuid4,
                            editable=False
                        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
