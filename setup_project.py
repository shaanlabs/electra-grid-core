#!/usr/bin/env python3
"""
EV Spot Project Setup Script
This script will set up the entire EV Spot project including:
- Virtual environment creation
- Dependency installation
- Database setup
- Static files collection
- Sample data population
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def create_virtual_environment():
    """Create virtual environment"""
    venv_name = "venv"
    if os.path.exists(venv_name):
        print(f"✅ Virtual environment '{venv_name}' already exists")
        return True
    
    return run_command(f"python -m venv {venv_name}", "Creating virtual environment")

def activate_venv_and_install():
    """Activate virtual environment and install dependencies"""
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        return False
    
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        return False
    
    return True

def setup_django():
    """Setup Django project"""
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    # Run migrations
    if not run_command(f"{python_cmd} manage.py makemigrations", "Creating migrations"):
        return False
    
    if not run_command(f"{python_cmd} manage.py migrate", "Running migrations"):
        return False
    
    # Collect static files
    if not run_command(f"{python_cmd} manage.py collectstatic --noinput", "Collecting static files"):
        return False
    
    return True

def create_superuser():
    """Create superuser interactively"""
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    print("\n👤 Creating superuser...")
    print("Please enter the following details:")
    
    try:
        subprocess.run(f"{python_cmd} manage.py createsuperuser", shell=True, check=True)
        print("✅ Superuser created successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Superuser creation failed or was cancelled")
        return False

def populate_sample_data():
    """Populate sample data"""
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    response = input("\n📊 Would you like to populate sample data? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        if run_command(f"{python_cmd} manage.py populate_sample_data", "Populating sample data"):
            print("✅ Sample data populated successfully")
            return True
        else:
            print("❌ Sample data population failed")
            return False
    else:
        print("⏭️ Skipping sample data population")
        return True

def create_directories():
    """Create necessary directories"""
    directories = [
        "media",
        "media/profile_pics",
        "media/station_images",
        "staticfiles",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def main():
    """Main setup function"""
    print("🚀 EV Spot Project Setup")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Create directories
    print("\n📁 Creating necessary directories...")
    create_directories()
    
    # Create virtual environment
    if not create_virtual_environment():
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not activate_venv_and_install():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Setup Django
    if not setup_django():
        print("❌ Failed to setup Django")
        sys.exit(1)
    
    # Create superuser
    create_superuser()
    
    # Populate sample data
    populate_sample_data()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate virtual environment:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Run the development server:")
    print("   python manage.py runserver")
    print("3. Open your browser and go to: http://127.0.0.1:8000")
    print("\n📚 For more information, check README.md and QUICKSTART.md")

if __name__ == "__main__":
    main() 