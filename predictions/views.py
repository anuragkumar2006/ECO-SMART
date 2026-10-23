from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Prediction
from .serializers import PredictionSerializer, PredictionUploadSerializer
from ml.predictor import get_waste_predictor
from recommendations.services import get_recommendation_for_category
from django.db.models import F

class PredictionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        queryset = Prediction.objects.filter(user=self.request.user)
        category_filter = self.request.query_params.get('category', None)
        if category_filter:
            queryset = queryset.filter(category=category_filter.lower())
        return queryset

    def create(self, request, *args, **kwargs):
        upload_serializer = PredictionUploadSerializer(data=request.data)
        upload_serializer.is_valid(raise_exception=True)
        image_file = upload_serializer.validated_data['image']

        # 1. AI Prediction via PyTorch Engine
        try:
            predictor = get_waste_predictor()
            ml_result = predictor.predict(image_file)
        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'AI analysis error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 2. Recommendation Engine Lookup
        rec_data = get_recommendation_for_category(ml_result['category'])

        # 3. Save Prediction Record
        prediction = Prediction.objects.create(
            user=request.user,
            image=image_file,
            category=ml_result['category'],
            confidence=ml_result['confidence'],
            bin_type=rec_data['bin_type'],
            bin_color_code=rec_data['bin_color_code'],
            biodegradable=rec_data['biodegradable'],
            recommendation_text=rec_data['suggestion'],
            is_low_confidence=ml_result['is_low_confidence']
        )

        # 4. Increment user total predictions count
        request.user.total_predictions = F('total_predictions') + 1
        request.user.save(update_fields=['total_predictions'])

        response_serializer = self.get_serializer(prediction)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class PredictionDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)
