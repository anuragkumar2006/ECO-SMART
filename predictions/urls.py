from django.urls import path
from .views import PredictionListCreateAPIView, PredictionDetailAPIView

urlpatterns = [
    path('', PredictionListCreateAPIView.as_view(), name='api_predictions_list_create'),
    path('<int:pk>/', PredictionDetailAPIView.as_view(), name='api_predictions_detail'),
]
