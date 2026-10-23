from django.db import models
from django.conf import settings

class Prediction(models.Model):
    CATEGORY_CHOICES = [
        ('organic', 'Organic'),
        ('recyclable', 'Recyclable'),
        ('hazardous', 'Hazardous'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='predictions'
    )
    image = models.ImageField(upload_to='predictions/%Y/%m/%d/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    confidence = models.FloatField(help_text="Confidence score from 0.0 to 1.0")
    bin_type = models.CharField(max_length=100)
    bin_color_code = models.CharField(max_length=20, default="#2E8B57")
    biodegradable = models.BooleanField(default=False)
    recommendation_text = models.TextField()
    is_low_confidence = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.category} ({self.confidence * 100:.1f}%) on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
