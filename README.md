# EV Spot - Electric Vehicle Charging Station Finder

A comprehensive Django-based web application that helps EV users find and manage charging stations. Built with Django REST API and modern frontend technologies.

## 🚀 Features

### Core Features
- **Interactive Map**: Find charging stations near you using Leaflet.js
- **Real-time Availability**: Check station availability and port status
- **User Authentication**: Secure login/registration system
- **Charging Sessions**: Start and stop charging sessions
- **Reviews & Ratings**: Rate and review charging stations
- **Favorites**: Save your preferred charging stations
- **Search & Filter**: Filter stations by type, distance, and availability

### Advanced Features
- **GPS Integration**: Automatic location detection
- **Distance Calculation**: Find stations within specified radius
- **Cost Tracking**: Monitor charging costs and energy consumption
- **Mobile Responsive**: Works perfectly on all devices
- **Real-time Updates**: Live station status updates

## 🛠️ Technology Stack

### Backend
- **Django 4.2.7**: Web framework
- **Django REST Framework**: API development
- **SQLite**: Database (can be upgraded to PostgreSQL)
- **Django CORS Headers**: Cross-origin resource sharing

### Frontend
- **Bootstrap 5**: UI framework
- **Font Awesome**: Icons
- **Leaflet.js**: Interactive maps
- **Vanilla JavaScript**: Frontend logic

### Development Tools
- **Python 3.8+**: Programming language
- **Pillow**: Image processing
- **django-filter**: Advanced filtering

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Automated Setup (Recommended)
```bash
python setup_project.py
```

### Manual Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ev-spot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Populate sample data (optional)**
   ```bash
   python manage.py populate_sample_data
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main application: http://localhost:8000
   - Admin panel: http://localhost:8000/admin
   - API documentation: http://localhost:8000/api/

### Testing the Setup
```bash
python test_project.py
```

## 🗄️ Database Models

### ChargingStation
- Name, address, coordinates
- Charging type (slow/fast/super)
- Power output and pricing
- Availability status
- Total and available ports

### ChargingSession
- User and station relationship
- Start/end times
- Energy consumption and cost
- Session status

### Review
- User ratings and comments
- Station-specific reviews
- Timestamp tracking

### CustomUser
- Extended user model
- Phone number and vehicle type
- Profile picture support

## 🔌 API Endpoints

### Authentication
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login
- `POST /api/users/logout/` - User logout
- `GET /api/users/profile/` - User profile

### Charging Stations
- `GET /api/stations/` - List all stations
- `GET /api/stations/{id}/` - Get station details
- `POST /api/stations/nearby/` - Find nearby stations
- `POST /api/stations/{id}/start_charging/` - Start charging
- `POST /api/stations/{id}/stop_charging/` - Stop charging

### Sessions & Reviews
- `GET /api/sessions/` - User's charging sessions
- `GET /api/reviews/` - Station reviews
- `POST /api/reviews/` - Create review
- `GET /api/favorites/` - User's favorite stations

## 🎨 UI Components

### Hero Section
- Eye-catching gradient background
- Call-to-action buttons
- Responsive design

### Interactive Map
- Leaflet.js integration
- Custom markers for stations
- Popup information windows
- User location detection

### Search Interface
- Radius slider (1-50km)
- Charging type filters
- Real-time results

### Station Cards
- Station information display
- Availability indicators
- Quick action buttons

## 🚀 Deployment

### Production Setup

1. **Environment Variables**
   ```bash
   export DEBUG=False
   export SECRET_KEY='your-secret-key'
   export ALLOWED_HOSTS='your-domain.com'
   ```

2. **Database Setup**
   ```bash
   # For PostgreSQL
   pip install psycopg2-binary
   ```

3. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

4. **Web Server**
   - Use Gunicorn or uWSGI
   - Configure Nginx as reverse proxy

### Docker Deployment
```bash
# Build image
docker build -t ev-spot .

# Run container
docker run -p 8000:8000 ev-spot
```

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### API Testing
```bash
# Using curl
curl -X GET http://localhost:8000/api/stations/

# Using Django REST Framework browsable API
# Visit http://localhost:8000/api/stations/ in browser
```

## 📱 Mobile Features

- **Responsive Design**: Works on all screen sizes
- **Touch-friendly**: Optimized for mobile interaction
- **GPS Integration**: Automatic location services
- **Offline Support**: Basic functionality without internet

## 🔒 Security Features

- **CSRF Protection**: Built-in Django CSRF tokens
- **Authentication**: Secure user authentication
- **Input Validation**: Server-side validation
- **SQL Injection Protection**: Django ORM protection
- **XSS Protection**: Template auto-escaping

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact: support@evspot.com

## 🔮 Future Enhancements

- **Payment Integration**: Direct payment processing
- **Push Notifications**: Real-time alerts
- **Social Features**: User communities
- **Analytics Dashboard**: Usage statistics
- **IoT Integration**: Real-time station monitoring
- **Multi-language Support**: Internationalization

## 📊 Performance

- **Page Load Time**: < 3 seconds
- **API Response Time**: < 500ms
- **Database Queries**: Optimized with select_related/prefetch_related
- **Caching**: Redis integration ready

---

**EV Spot** - Making EV charging accessible and convenient for everyone! ⚡🚗 