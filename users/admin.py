from django.contrib import admin # Noqa

from users.models import User
# Register your models here.

admin.site.register(User)
