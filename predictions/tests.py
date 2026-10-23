from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from recommendations.models import RecommendationRule
from recommendations.services import get_recommendation_for_category
from ml.predictor import get_waste_predictor
import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class EcoSmartSystemTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='Password123',
            name='Test User'
        )

        # Seed recommendation rules
        RecommendationRule.objects.create(
            category='organic',
            bin_type='Green Bin',
            bin_color_code='#2E8B57',
            biodegradable=True,
            suggestion='Dispose in wet waste compost bin.'
        )
        RecommendationRule.objects.create(
            category='recyclable',
            bin_type='Blue Bin',
            bin_color_code='#3B82F6',
            biodegradable=False,
            suggestion='Dispose in dry recyclable bin.'
        )

    def test_user_authentication(self):
        # Login to get JWT
        response = self.client.post('/api/auth/login/', {
            'email': 'testuser@example.com',
            'password': 'Password123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_recommendation_engine(self):
        rec = get_recommendation_for_category('organic')
        self.assertEqual(rec['bin_type'], 'Green Bin')
        self.assertTrue(rec['biodegradable'])

    def test_prediction_api_upload(self):
        # Authenticate client
        login_res = self.client.post('/api/auth/login/', {
            'email': 'testuser@example.com',
            'password': 'Password123'
        })
        token = login_res.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Create dummy image in memory
        img = Image.new('RGB', (100, 100), color='green')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)

        uploaded = SimpleUploadedFile("apple.jpg", img_bytes.read(), content_type="image/jpeg")

        response = self.client.post('/api/predictions/', {'image': uploaded}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['category'], 'organic')
        self.assertIn('confidence', response.data)

        # Verify analytics endpoint reflecting prediction
        analytics_res = self.client.get('/api/analytics/summary/')
        self.assertEqual(analytics_res.status_code, status.HTTP_200_OK)
        self.assertEqual(analytics_res.data['total_scans'], 1)
        self.assertEqual(analytics_res.data['organic_count'], 1)
