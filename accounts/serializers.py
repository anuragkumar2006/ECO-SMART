from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data.get('name', '')
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'name': self.user.name,
        }
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    category_breakdown = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'total_predictions', 'category_breakdown', 'created_at']
        read_only_fields = ['id', 'email', 'total_predictions', 'category_breakdown', 'created_at']

    def get_category_breakdown(self, obj):
        from predictions.models import Prediction
        from django.db.models import Count
        qs = Prediction.objects.filter(user=obj).values('category').annotate(count=Count('id'))
        breakdown = {'organic': 0, 'recyclable': 0, 'hazardous': 0}
        for item in qs:
            cat = item['category'].lower()
            if cat in breakdown:
                breakdown[cat] = item['count']
        return breakdown

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
