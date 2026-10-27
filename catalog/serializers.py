from rest_framework import serializers
from .models import Country, Mountain, Route, Stop, Org, Trip

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name", "description"]

class MountainSerializer(serializers.ModelSerializer):
    country_id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), source="country")
    class Meta:
        model = Mountain
        fields = ["id", "country_id", "name", "height", "description", "image", "summit_view"]

class RouteSerializer(serializers.ModelSerializer):
    mountain_id = serializers.PrimaryKeyRelatedField(queryset=Mountain.objects.all(), source="mountain")
    class Meta:
        model = Route
        fields = ["id", "mountain_id", "name", "description", "difficult", "duration", "source"]

class StopSerializer(serializers.ModelSerializer):
    route_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Stop
        fields = ["id", "route_id", "position", "name", "altitude", "description"]

    def validate_position(self, value):
        if value <= 0:
           raise serializers.ValidationError("Номер зупинки має бути більшим за нуль.")
        else:
            return value 

class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = ["id", "name", "description", "email", "phone", "website"]

class TripSerializer(serializers.ModelSerializer):
    route_id = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all(), source="route")
    organizer_id = serializers.PrimaryKeyRelatedField(queryset=Org.objects.all(), source="organizer")
    class Meta:
        model = Trip
        fields = [
        "id", "route_id", "organizer_id", "title",
        "start_date", "end_date", "price", "capacity",
        "rent", "rent_detail", "sherpa", "support",
        "services", "requirements", "status",
        ]
    def validate_price(self, value):
        if value < 0:
           raise serializers.ValidationError("Ціна не може бути від’ємною.")
        else:
            return value 

    def validate_capacity(self, value):
        if value <= 0:
           raise serializers.ValidationError("Кількість місць має бути більшою за нуль.")
        else:
            return value     

