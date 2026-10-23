from django.urls import path
from .views import (
    AnalyticsSummaryView,
    AnalyticsCategoriesView,
    AnalyticsBiodegradabilityView,
    AnalyticsBinUsageView,
    AnalyticsTrendsView
)

urlpatterns = [
    path('summary/', AnalyticsSummaryView.as_view(), name='api_analytics_summary'),
    path('categories/', AnalyticsCategoriesView.as_view(), name='api_analytics_categories'),
    path('biodegradability/', AnalyticsBiodegradabilityView.as_view(), name='api_analytics_biodegradability'),
    path('bin-usage/', AnalyticsBinUsageView.as_view(), name='api_analytics_bin_usage'),
    path('trends/', AnalyticsTrendsView.as_view(), name='api_analytics_trends'),
]
