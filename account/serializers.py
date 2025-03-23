from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    # username = serializers.SerializerMethodField(source=)
    class Meta:
        model = User
        fields = ['username', 'full_name', 'phone', 'melicode', 'email']
        read_only_fields = ['id', 'is_active']