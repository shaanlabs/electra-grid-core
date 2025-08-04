from django.db import models
from django.contrib.auth.models import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class ChargingStation(models.Model):
    CHARGING_TYPES = [
        ('slow', 'Slow Charging'),
        ('fast', 'Fast Charging'),
        ('super', 'Super Fast Charging'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Under Maintenance'),
        ('inactive', 'Inactive'),
    ]
    
    name = models.CharField(max_length=200)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    charging_type = models.CharField(max_length=10, choices=CHARGING_TYPES)
    power_output = models.IntegerField(help_text="Power output in kW")
    price_per_kwh = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    total_ports = models.IntegerField(default=1)
    available_ports = models.IntegerField(default=1)
    image = models.ImageField(upload_to='station_images/', blank=True, null=True)
    description = models.TextField(blank=True)
    amenities = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.address}"
    
    @property
    def is_available(self):
        return self.available_ports > 0 and self.status == 'active'


class ChargingSession(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    energy_consumed = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    class Meta:
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.user.username} - {self.station.name}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'station']
    
    def __str__(self):
        return f"{self.user.username} - {self.station.name} - {self.rating} stars"


class FavoriteStation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'station']
    
    def __str__(self):
        return f"{self.user.username} - {self.station.name}" 