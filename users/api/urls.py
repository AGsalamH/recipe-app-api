'''
Users API endpoints.
'''
from django.urls import path
from users.api.views import CreateUserView, RetrieveUpdateProfileView
from users.auth.views import ObtainToken


app_name = 'users_api'
urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('auth-token/', ObtainToken.as_view(), name='obtain-auth-token'),
    path('<pk>/', RetrieveUpdateProfileView.as_view(), name='me'),
]
