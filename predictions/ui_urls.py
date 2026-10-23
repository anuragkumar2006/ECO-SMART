from django.urls import path
from .ui_views import (
    dashboard_view,
    scan_view,
    result_view,
    history_view,
    analytics_view,
    profile_view
)

urlpatterns = [
    path('dashboard/', dashboard_view, name='ui_dashboard'),
    path('scan/', scan_view, name='ui_scan'),
    path('result/<int:prediction_id>/', result_view, name='ui_result'),
    path('history/', history_view, name='ui_history'),
    path('analytics/', analytics_view, name='ui_analytics'),
    path('profile/', profile_view, name='ui_profile'),
]
