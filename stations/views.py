from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
import math
from .models import ChargingStation, ChargingSession, Review, FavoriteStation
from .serializers import (
    ChargingStationSerializer, ChargingSessionSerializer, 
    ReviewSerializer, FavoriteStationSerializer, NearbyStationsSerializer
)


class ChargingStationViewSet(viewsets.ModelViewSet):
    queryset = ChargingStation.objects.all()
    serializer_class = ChargingStationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['charging_type', 'status', 'power_output']
    search_fields = ['name', 'address', 'description']
    ordering_fields = ['name', 'price_per_kwh', 'created_at']
    
    @action(detail=False, methods=['post'])
    def nearby(self, request):
        try:
            serializer = NearbyStationsSerializer(data=request.data)
            if serializer.is_valid():
                lat = serializer.validated_data['latitude']
                lng = serializer.validated_data['longitude']
                radius = serializer.validated_data['radius']
                
                # Validate coordinates
                if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                    return Response({'error': 'Invalid coordinates'}, status=status.HTTP_400_BAD_REQUEST)
                
                if radius <= 0 or radius > 100:  # Max 100km radius
                    return Response({'error': 'Invalid radius (must be between 0 and 100 km)'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Simple distance calculation (Haversine formula)
                stations = []
                for station in ChargingStation.objects.filter(status='active'):
                    distance = self.calculate_distance(lat, lng, station.latitude, station.longitude)
                    if distance <= radius:
                        station_data = ChargingStationSerializer(station, context={'request': request}).data
                        station_data['distance'] = round(distance, 2)
                        stations.append(station_data)
                
                # Sort by distance
                stations.sort(key=lambda x: x['distance'])
                return Response(stations)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An error occurred while fetching nearby stations'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def calculate_distance(self, lat1, lng1, lat2, lng2):
        """Calculate distance between two points using Haversine formula"""
        R = 6371  # Earth's radius in kilometers
        
        lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))
        distance = R * c
        
        return distance
    
    @action(detail=True, methods=['post'])
    def start_charging(self, request, pk=None):
        try:
            station = self.get_object()
            if not station.is_available:
                return Response({'error': 'Station is not available'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if user already has an active session
            active_session = ChargingSession.objects.filter(user=request.user, status='active').first()
            if active_session:
                return Response({'error': 'You already have an active charging session'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create new charging session
            session = ChargingSession.objects.create(user=request.user, station=station)
            station.available_ports -= 1
            station.save()
            
            serializer = ChargingSessionSerializer(session)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'An error occurred while starting charging session'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def stop_charging(self, request, pk=None):
        try:
            station = self.get_object()
            session = ChargingSession.objects.filter(user=request.user, station=station, status='active').first()
            
            if not session:
                return Response({'error': 'No active charging session found'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Update session
            session.status = 'completed'
            session.save()
            
            # Update station availability
            station.available_ports += 1
            station.save()
            
            serializer = ChargingSessionSerializer(session)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': 'An error occurred while stopping charging session'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChargingSessionViewSet(viewsets.ModelViewSet):
    serializer_class = ChargingSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChargingSession.objects.filter(user=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteStationViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteStationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FavoriteStation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 