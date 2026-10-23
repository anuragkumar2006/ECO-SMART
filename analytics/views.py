from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .services import (
    get_analytics_summary,
    get_category_distribution,
    get_biodegradability_split,
    get_bin_usage_analytics,
    get_trends_analytics
)

class AnalyticsSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = get_analytics_summary(request.user)
        return Response(data, status=status.HTTP_200_OK)

class AnalyticsCategoriesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = get_category_distribution(request.user)
        return Response(data, status=status.HTTP_200_OK)

class AnalyticsBiodegradabilityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = get_biodegradability_split(request.user)
        return Response(data, status=status.HTTP_200_OK)

class AnalyticsBinUsageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = get_bin_usage_analytics(request.user)
        return Response(data, status=status.HTTP_200_OK)

class AnalyticsTrendsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        days_param = request.query_params.get('days', 30)
        try:
            days = int(days_param)
        except ValueError:
            days = 30
        data = get_trends_analytics(request.user, days=days)
        return Response(data, status=status.HTTP_200_OK)
