from django.db import models

class RecommendationRule(models.Model):
    CATEGORY_CHOICES = [
        ('organic', 'Organic'),
        ('recyclable', 'Recyclable'),
        ('hazardous', 'Hazardous'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    bin_type = models.CharField(max_length=100, help_text="e.g. Green Bin, Blue Bin, Red Bin")
    bin_color_code = models.CharField(max_length=20, default="#2E8B57", help_text="Hex or color name")
    biodegradable = models.BooleanField(default=False)
    suggestion = models.TextField(help_text="Actionable disposal guidance for the user")
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_category_display()} -> {self.bin_type}"
