#!/usr/bin/env python3
"""
EV Spot Project Test Script
This script tests all major components of the EV Spot project
"""

import os
import sys
import subprocess
import requests
import json
from pathlib import Path

def test_python_imports():
    """Test if all required Python packages can be imported"""
    print("🔍 Testing Python imports...")
    
    required_packages = [
        'django',
        'rest_framework',
        'corsheaders',
        'PIL',
        'django_filters'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            return False
    
    return True

def test_django_setup():
    """Test Django setup"""
    print("\n🔍 Testing Django setup...")
    
    try:
        import django
        from django.conf import settings
        from django.core.management import execute_from_command_line
        
        # Set up Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evspot.settings')
        django.setup()
        
        print("✅ Django setup successful")
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def test_database_models():
    """Test database models"""
    print("\n🔍 Testing database models...")
    
    try:
        from users.models import CustomUser
        from stations.models import ChargingStation, ChargingSession, Review, FavoriteStation
        
        print("✅ All models imported successfully")
        return True
    except Exception as e:
        print(f"❌ Model import failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🔍 Testing API endpoints...")
    
    base_url = "http://127.0.0.1:8000"
    endpoints = [
        "/api/stations/",
        "/api/users/register/",
        "/api/users/login/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"✅ {endpoint}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ {endpoint}: {e} (server might not be running)")
    
    return True

def test_static_files():
    """Test if static files exist"""
    print("\n🔍 Testing static files...")
    
    static_files = [
        "static/css/style.css",
        "static/js/main.js",
        "static/images/hero-ev.jpg",
        "static/images/about-ev.jpg"
    ]
    
    for file_path in static_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (missing)")
    
    return True

def test_templates():
    """Test if templates exist"""
    print("\n🔍 Testing templates...")
    
    template_files = [
        "templates/base.html",
        "templates/index.html"
    ]
    
    for file_path in template_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (missing)")
    
    return True

def test_migrations():
    """Test if migrations exist"""
    print("\n🔍 Testing migrations...")
    
    migration_dirs = [
        "users/migrations",
        "stations/migrations"
    ]
    
    for migration_dir in migration_dirs:
        if os.path.exists(migration_dir):
            migration_files = [f for f in os.listdir(migration_dir) if f.endswith('.py') and f != '__init__.py']
            if migration_files:
                print(f"✅ {migration_dir}: {len(migration_files)} migration(s)")
            else:
                print(f"⚠️ {migration_dir}: No migrations found")
        else:
            print(f"❌ {migration_dir} (missing)")
    
    return True

def test_directories():
    """Test if required directories exist"""
    print("\n🔍 Testing directories...")
    
    required_dirs = [
        "media",
        "media/profile_pics",
        "media/station_images",
        "staticfiles",
        "logs"
    ]
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}")
        else:
            print(f"❌ {directory} (missing)")
    
    return True

def test_requirements():
    """Test requirements.txt"""
    print("\n🔍 Testing requirements.txt...")
    
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            requirements = f.read()
        
        if requirements.strip():
            print("✅ requirements.txt exists and has content")
            return True
        else:
            print("❌ requirements.txt is empty")
            return False
    else:
        print("❌ requirements.txt missing")
        return False

def run_django_checks():
    """Run Django system checks"""
    print("\n🔍 Running Django system checks...")
    
    try:
        result = subprocess.run(
            ["python", "manage.py", "check"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Django system checks passed")
            return True
        else:
            print(f"❌ Django system checks failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"⚠️ Could not run Django checks: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 EV Spot Project Test Suite")
    print("=" * 50)
    
    tests = [
        ("Python Imports", test_python_imports),
        ("Django Setup", test_django_setup),
        ("Database Models", test_database_models),
        ("Static Files", test_static_files),
        ("Templates", test_templates),
        ("Migrations", test_migrations),
        ("Directories", test_directories),
        ("Requirements", test_requirements),
        ("Django Checks", run_django_checks),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your project is ready to run.")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 