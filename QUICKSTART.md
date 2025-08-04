# EV Spot - Quick Start Guide

Get your EV Spot application up and running in minutes!

## 🚀 Quick Setup (5 minutes)

### Option 1: Automated Setup (Recommended)

1. **Run the setup script:**
   ```bash
   python setup.py
   ```

2. **Follow the prompts** to create a superuser and populate sample data

3. **Start the server:**
   ```bash
   # Windows
   venv\Scripts\activate
   python manage.py runserver
   
   # macOS/Linux
   source venv/bin/activate
   python manage.py runserver
   ```

4. **Open your browser** and go to: http://localhost:8000

### Option 2: Manual Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Populate sample data (optional):**
   ```bash
   python manage.py populate_sample_data
   ```

7. **Start the server:**
   ```bash
   python manage.py runserver
   ```

## 🎯 What You'll Get

### Frontend Features
- ✅ Beautiful, responsive homepage
- ✅ Interactive map with Leaflet.js
- ✅ User authentication (login/register)
- ✅ Station search and filtering
- ✅ Real-time station availability
- ✅ Mobile-friendly design

### Backend Features
- ✅ Django REST API
- ✅ User management system
- ✅ Charging station management
- ✅ Session tracking
- ✅ Reviews and ratings
- ✅ Admin panel

### Sample Data
- ✅ 8 charging stations across different locations
- ✅ 5 sample users
- ✅ Multiple reviews and ratings
- ✅ Various charging types (slow, fast, super)

## 🔗 Important URLs

- **Main Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/api/

## 👤 Default Users

After running the sample data population, you can log in with:

- **Username**: user1, user2, user3, user4, user5
- **Password**: password123

## 🗺️ Sample Charging Stations

The sample data includes stations at:
- Downtown EV Station
- Mall Parking Garage
- Highway Rest Stop
- University Campus
- Office Complex
- Residential Complex
- Shopping Center
- Airport Parking

## 🛠️ Development

### Making Changes
1. Edit the Django models in `stations/models.py`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Restart the server

### Adding New Features
- **Frontend**: Edit templates in `templates/` and static files in `static/`
- **Backend**: Add views in `stations/views.py` and URLs in `stations/urls.py`
- **API**: Extend serializers in `stations/serializers.py`

## 🐛 Troubleshooting

### Common Issues

**Port already in use:**
```bash
python manage.py runserver 8001
```

**Database errors:**
```bash
python manage.py migrate --run-syncdb
```

**Static files not loading:**
```bash
python manage.py collectstatic
```

**Permission errors (Linux/macOS):**
```bash
chmod +x setup.py
```

### Getting Help

1. Check the full [README.md](README.md) for detailed documentation
2. Look at the Django error messages in the terminal
3. Check the browser console for JavaScript errors
4. Verify all dependencies are installed: `pip list`

## 🎉 You're Ready!

Your EV Spot application is now running! Explore the features:

1. **Browse the homepage** and see the beautiful UI
2. **Try the interactive map** to find charging stations
3. **Register a new account** or use the sample users
4. **Explore the admin panel** to manage data
5. **Test the API endpoints** in your browser

Happy coding! ⚡🚗 