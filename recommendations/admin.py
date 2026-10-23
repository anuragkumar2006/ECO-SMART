from django.contrib import admin
from .models import RecommendationRule

@admin.register(RecommendationRule)
class RecommendationRuleAdmin(admin.ModelAdmin):
    list_display = ('category', 'bin_type', 'bin_color_code', 'biodegradable', 'active', 'updated_at')
    list_filter = ('category', 'biodegradable', 'active')
    search_fields = ('category', 'bin_type', 'suggestion')
    list_editable = ('active', 'bin_type', 'bin_color_code', 'biodegradable')
