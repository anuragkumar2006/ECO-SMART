from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'confidence_pct', 'bin_type', 'biodegradable', 'is_low_confidence', 'created_at')
    list_filter = ('category', 'biodegradable', 'is_low_confidence', 'created_at')
    search_fields = ('user__email', 'category', 'recommendation_text')
    readonly_fields = ('created_at',)

    def confidence_pct(self, obj):
        return f"{obj.confidence * 100:.1f}%"
    confidence_pct.short_description = 'Confidence'
