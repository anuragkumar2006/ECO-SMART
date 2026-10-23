from django.urls import path
from .ui_views import landing_view, login_view, register_view

urlpatterns = [
    path('', landing_view, name='ui_landing'),
    path('login/', login_view, name='ui_login'),
    path('register/', register_view, name='ui_register'),
]
