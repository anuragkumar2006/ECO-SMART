from rest_framework import serializers
from .models import Prediction

class PredictionSerializer(serializers.ModelSerializer):
    confidence_percentage = serializers.SerializerMethodField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Prediction
        fields = [
            'id',
            'user',
            'image',
            'category',
            'category_display',
            'confidence',
            'confidence_percentage',
            'bin_type',
            'bin_color_code',
            'biodegradable',
            'recommendation_text',
            'is_low_confidence',
            'created_at'
        ]
        read_only_fields = [
            'id',
            'user',
            'category',
            'confidence',
            'bin_type',
            'bin_color_code',
            'biodegradable',
            'recommendation_text',
            'is_low_confidence',
            'created_at'
        ]

    def get_confidence_percentage(self, obj):
        return round(obj.confidence * 100, 1)

class PredictionUploadSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
