from django.contrib.auth.models import User
from rest_framework import serializers

class RegSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, max_length=128, trim_whitespace=False)
    confirmation = serializers.CharField(write_only=True, min_length=8, max_length=128, trim_whitespace=False)
    email = serializers.EmailField(required=True, max_length=254)
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", "confirmation"]

    def validate(self, data):
        if data["password"] == data["confirmation"]:
            return data
        else:
            raise serializers.ValidationError({"confirmation": "Паролі не збігаються."})

    def create(self, validated_data):
        validated_data.pop("confirmation")
        return User.objects.create_user(username=validated_data["username"], email=validated_data["email"], password=validated_data["password"], first_name=validated_data.get("first_name", ""), last_name=validated_data.get("last_name", ""))
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]