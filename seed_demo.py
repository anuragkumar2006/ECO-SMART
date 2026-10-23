import os
import sys
import django
from datetime import timedelta
from django.utils import timezone
from PIL import Image, ImageDraw
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from predictions.models import Prediction
from recommendations.services import get_recommendation_for_category
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

def create_sample_image(color_name, label):
    img = Image.new('RGB', (300, 300), color=color_name)
    draw = ImageDraw.Draw(img)
    draw.text((30, 140), f"EcoSmart Demo: {label}", fill=(255, 255, 255))
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return SimpleUploadedFile(f"{label.lower().replace(' ', '_')}.jpg", buffer.read(), content_type="image/jpeg")

def seed():
    # 1. Create Demo User
    user, created = User.objects.get_or_create(
        email='user@example.com',
        defaults={'name': 'Anurag Demo User'}
    )
    if created or not user.check_password('Password123'):
        user.set_password('Password123')
        user.save()
        print(f"Created demo user: user@example.com / Password123")
    else:
        print(f"Demo user already exists: user@example.com")

    # 2. Populate Sample Predictions across past 30 days
    sample_items = [
        ('organic', 'Apple Core', '#2E8B57', 0.9620, 2),
        ('recyclable', 'Plastic Bottle', '#3B82F6', 0.9420, 3),
        ('recyclable', 'Cardboard Box', '#3B82F6', 0.9150, 5),
        ('organic', 'Banana Peel', '#2E8B57', 0.9380, 8),
        ('hazardous', 'Lithium Battery', '#B45309', 0.9640, 10),
        ('recyclable', 'Aluminum Can', '#3B82F6', 0.9250, 12),
        ('organic', 'Vegetable Waste', '#2E8B57', 0.9180, 15),
        ('hazardous', 'Paint Container', '#B45309', 0.8850, 18),
        ('recyclable', 'Glass Jar', '#3B82F6', 0.9560, 22),
        ('organic', 'Garden Leaves', '#2E8B57', 0.9020, 25),
    ]

    now = timezone.now()
    count_created = 0

    for cat, label, color, conf, days_ago in sample_items:
        rec = get_recommendation_for_category(cat)
        img_file = create_sample_image(color, label)
        
        pred = Prediction.objects.create(
            user=user,
            image=img_file,
            category=cat,
            confidence=conf,
            bin_type=rec['bin_type'],
            bin_color_code=rec['bin_color_code'],
            biodegradable=rec['biodegradable'],
            recommendation_text=rec['suggestion'],
            is_low_confidence=(conf < 0.70)
        )
        # Override created_at for historical trends visualization
        Prediction.objects.filter(id=pred.id).update(created_at=now - timedelta(days=days_ago))
        count_created += 1

    user.total_predictions = Prediction.objects.filter(user=user).count()
    user.save()
    print(f"Successfully seeded {count_created} sample predictions for demonstration!")

if __name__ == '__main__':
    seed()
