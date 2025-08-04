from rest_framework import serializers
from .models import ChargingStation, ChargingSession, Review, FavoriteStation
from django.contrib.auth.models import get_user_model

User = get_user_model()


class ChargingStationSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    
    class Meta:
        model = ChargingStation
        fields = '__all__'
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    
    def get_total_reviews(self, obj):
        return obj.reviews.count()
    
    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return FavoriteStation.objects.filter(user=request.user, station=obj).exists()
        return False


class ChargingSessionSerializer(serializers.ModelSerializer):
    station_name = serializers.CharField(source='station.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ChargingSession
        fields = '__all__'
        read_only_fields = ['user', 'start_time', 'energy_consumed', 'total_cost']


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    station_name = serializers.CharField(source='station.name', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user']


class FavoriteStationSerializer(serializers.ModelSerializer):
    station_details = ChargingStationSerializer(source='station', read_only=True)
    
    class Meta:
        model = FavoriteStation
        fields = '__all__'
        read_only_fields = ['user']


class NearbyStationsSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    radius = serializers.IntegerField(default=10, min_value=1, max_value=100) 