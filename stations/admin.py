from django.contrib import admin
from .models import ChargingStation, ChargingSession, Review, FavoriteStation


@admin.register(ChargingStation)
class ChargingStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'charging_type', 'status', 'available_ports', 'total_ports', 'price_per_kwh']
    list_filter = ['charging_type', 'status', 'created_at']
    search_fields = ['name', 'address']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ChargingSession)
class ChargingSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'station', 'start_time', 'end_time', 'status', 'energy_consumed', 'total_cost']
    list_filter = ['status', 'start_time']
    search_fields = ['user__username', 'station__name']
    readonly_fields = ['start_time']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'station', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'station__name', 'comment']
    readonly_fields = ['created_at']


@admin.register(FavoriteStation)
class FavoriteStationAdmin(admin.ModelAdmin):
    list_display = ['user', 'station', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'station__name']
    readonly_fields = ['created_at'] 