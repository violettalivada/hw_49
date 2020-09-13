from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', RegisterView.as_view(), name='create'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('profiles/', ListProfileView.as_view(), name='profile_list'),
]