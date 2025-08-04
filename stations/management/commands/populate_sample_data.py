from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from stations.models import ChargingStation, Review
from decimal import Decimal
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with sample charging station data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create sample users
        users = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'user{i+1}',
                defaults={
                    'email': f'user{i+1}@example.com',
                    'first_name': f'User{i+1}',
                    'last_name': 'Test',
                    'phone_number': f'+1-555-{1000+i}',
                    'vehicle_type': random.choice(['Tesla Model 3', 'Nissan Leaf', 'Chevrolet Bolt', 'BMW i3'])
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
            self.stdout.write(f'Created user: {user.username}')

        # Sample charging stations data
        stations_data = [
            {
                'name': 'Downtown EV Station',
                'address': '123 Main St, Downtown, CA 90210',
                'latitude': Decimal('37.7749'),
                'longitude': Decimal('-122.4194'),
                'charging_type': 'fast',
                'power_output': 50,
                'price_per_kwh': Decimal('0.35'),
                'total_ports': 4,
                'available_ports': 2,
                'description': 'Convenient downtown location with fast charging capabilities.',
                'amenities': ['Restrooms', 'Coffee Shop', 'WiFi']
            },
            {
                'name': 'Mall Parking Garage',
                'address': '456 Shopping Ave, Mall District, CA 90211',
                'latitude': Decimal('37.7849'),
                'longitude': Decimal('-122.4094'),
                'charging_type': 'super',
                'power_output': 150,
                'price_per_kwh': Decimal('0.45'),
                'total_ports': 2,
                'available_ports': 1,
                'description': 'High-speed charging in mall parking garage.',
                'amenities': ['Shopping', 'Food Court', 'Security']
            },
            {
                'name': 'Highway Rest Stop',
                'address': '789 Freeway Exit, Highway 101, CA 90212',
                'latitude': Decimal('37.7949'),
                'longitude': Decimal('-122.3994'),
                'charging_type': 'super',
                'power_output': 200,
                'price_per_kwh': Decimal('0.50'),
                'total_ports': 6,
                'available_ports': 4,
                'description': 'Convenient highway rest stop with multiple charging ports.',
                'amenities': ['Restrooms', 'Vending Machines', '24/7 Access']
            },
            {
                'name': 'University Campus',
                'address': '321 College Blvd, University District, CA 90213',
                'latitude': Decimal('37.8049'),
                'longitude': Decimal('-122.3894'),
                'charging_type': 'slow',
                'power_output': 7,
                'price_per_kwh': Decimal('0.25'),
                'total_ports': 8,
                'available_ports': 6,
                'description': 'Affordable slow charging for students and staff.',
                'amenities': ['Library', 'Cafeteria', 'Student Center']
            },
            {
                'name': 'Office Complex',
                'address': '654 Business Park Dr, Tech District, CA 90214',
                'latitude': Decimal('37.8149'),
                'longitude': Decimal('-122.3794'),
                'charging_type': 'fast',
                'power_output': 75,
                'price_per_kwh': Decimal('0.40'),
                'total_ports': 3,
                'available_ports': 1,
                'description': 'Fast charging for office workers and visitors.',
                'amenities': ['Office Buildings', 'Café', 'Meeting Rooms']
            },
            {
                'name': 'Residential Complex',
                'address': '987 Home St, Residential Area, CA 90215',
                'latitude': Decimal('37.8249'),
                'longitude': Decimal('-122.3694'),
                'charging_type': 'slow',
                'power_output': 11,
                'price_per_kwh': Decimal('0.30'),
                'total_ports': 5,
                'available_ports': 3,
                'description': 'Overnight charging for residents.',
                'amenities': ['Residential', 'Parking', 'Security']
            },
            {
                'name': 'Shopping Center',
                'address': '147 Retail Blvd, Shopping District, CA 90216',
                'latitude': Decimal('37.8349'),
                'longitude': Decimal('-122.3594'),
                'charging_type': 'fast',
                'power_output': 60,
                'price_per_kwh': Decimal('0.38'),
                'total_ports': 4,
                'available_ports': 2,
                'description': 'Charge while you shop at the retail center.',
                'amenities': ['Shopping', 'Restaurants', 'Entertainment']
            },
            {
                'name': 'Airport Parking',
                'address': '258 Airport Rd, Airport District, CA 90217',
                'latitude': Decimal('37.8449'),
                'longitude': Decimal('-122.3494'),
                'charging_type': 'super',
                'power_output': 180,
                'price_per_kwh': Decimal('0.55'),
                'total_ports': 8,
                'available_ports': 5,
                'description': 'High-speed charging for airport travelers.',
                'amenities': ['Airport', 'Parking', 'Shuttle Service']
            }
        ]

        # Create charging stations
        stations = []
        for data in stations_data:
            station, created = ChargingStation.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                stations.append(station)
                self.stdout.write(f'Created station: {station.name}')

        # Create sample reviews
        review_texts = [
            "Great location and fast charging!",
            "Convenient spot, but a bit expensive.",
            "Perfect for my daily commute.",
            "Clean and well-maintained station.",
            "Staff is very helpful and friendly.",
            "Good value for money.",
            "Always available when I need it.",
            "Modern equipment and easy to use.",
            "Safe location with good lighting.",
            "Excellent service and fast charging."
        ]

        for station in stations:
            # Create 2-4 reviews per station
            num_reviews = random.randint(2, 4)
            for _ in range(num_reviews):
                user = random.choice(users)
                rating = random.randint(3, 5)
                comment = random.choice(review_texts)
                
                review, created = Review.objects.get_or_create(
                    user=user,
                    station=station,
                    defaults={
                        'rating': rating,
                        'comment': comment
                    }
                )
                if created:
                    self.stdout.write(f'Created review for {station.name} by {user.username}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(users)} users, {len(stations)} stations, and multiple reviews!'
            )
        ) 