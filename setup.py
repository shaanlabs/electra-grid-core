#!/usr/bin/env python3
"""
EV Spot Setup Script
This script helps you set up the EV Spot Django project.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version {sys.version.split()[0]} is compatible!")
    return True

def create_virtual_environment():
    """Create a virtual environment."""
    if os.path.exists("venv"):
        print("✅ Virtual environment already exists!")
        return True
    
    return run_command("python -m venv venv", "Creating virtual environment")

def activate_virtual_environment():
    """Activate virtual environment based on OS."""
    if os.name == 'nt':  # Windows
        activate_script = "venv\\Scripts\\activate"
    else:  # Unix/Linux/macOS
        activate_script = "source venv/bin/activate"
    
    print(f"📝 To activate virtual environment, run: {activate_script}")
    return activate_script

def install_dependencies():
    """Install Python dependencies."""
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_cmd = "venv/bin/pip"
    
    return run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies")

def run_migrations():
    """Run Django migrations."""
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        python_cmd = "venv/bin/python"
    
    success = True
    success &= run_command(f"{python_cmd} manage.py makemigrations", "Creating migrations")
    success &= run_command(f"{python_cmd} manage.py migrate", "Running migrations")
    return success

def create_superuser():
    """Create a superuser account."""
    print("👤 Would you like to create a superuser account? (y/n): ", end="")
    response = input().lower().strip()
    
    if response in ['y', 'yes']:
        if os.name == 'nt':  # Windows
            python_cmd = "venv\\Scripts\\python"
        else:  # Unix/Linux/macOS
            python_cmd = "venv/bin/python"
        
        run_command(f"{python_cmd} manage.py createsuperuser", "Creating superuser")

def populate_sample_data():
    """Populate database with sample data."""
    print("📊 Would you like to populate the database with sample data? (y/n): ", end="")
    response = input().lower().strip()
    
    if response in ['y', 'yes']:
        if os.name == 'nt':  # Windows
            python_cmd = "venv\\Scripts\\python"
        else:  # Unix/Linux/macOS
            python_cmd = "venv/bin/python"
        
        run_command(f"{python_cmd} manage.py populate_sample_data", "Populating sample data")

def create_static_directories():
    """Create necessary static file directories."""
    directories = [
        "static/images",
        "media/profile_pics",
        "media/station_images"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def main():
    """Main setup function."""
    print("🚀 EV Spot Setup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Get activation command
    activate_cmd = activate_virtual_environment()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies. Please check your internet connection.")
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        print("❌ Failed to run migrations.")
        sys.exit(1)
    
    # Create static directories
    create_static_directories()
    
    # Create superuser
    create_superuser()
    
    # Populate sample data
    populate_sample_data()
    
    print("\n🎉 Setup completed successfully!")
    print("=" * 50)
    print("📋 Next steps:")
    print(f"1. Activate virtual environment: {activate_cmd}")
    print("2. Start the development server: python manage.py runserver")
    print("3. Open your browser and go to: http://localhost:8000")
    print("4. Admin panel: http://localhost:8000/admin")
    print("\n📚 For more information, check the README.md file")

if __name__ == "__main__":
    main() 