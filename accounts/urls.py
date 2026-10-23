from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomTokenObtainPairView, ProfileView, ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api_register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='api_login'),
    path('refresh/', TokenRefreshView.as_view(), name='api_refresh'),
    path('profile/', ProfileView.as_view(), name='api_profile'),
    path('change-password/', ChangePasswordView.as_view(), name='api_change_password'),
]
