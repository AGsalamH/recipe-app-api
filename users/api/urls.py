'''
Users API endpoints.
'''
from django.urls import path
from users.api.views import CreateUserView


app_name = 'users_api'
urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
]
