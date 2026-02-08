#!/usr/bin/env python3
"""
AI Mock Interview System - Setup Script
Helps users configure the application for first-time use
"""

import os
import sys
import subprocess

def print_header():
    print("\n" + "="*70)
    print("🎯 AI MOCK INTERVIEW SYSTEM - SETUP")
    print("="*70 + "\n")

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print("✓ Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        print("   Please install Python 3.8+ from https://www.python.org/downloads/")
        return False
    print(f"   ✅ Python {sys.version_info.major}.{sys.version_info.minor} detected\n")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("✓ Installing dependencies...")
    print("   This may take a few minutes...\n")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--upgrade'])
        print("\n   ✅ All dependencies installed successfully\n")
        return True
    except subprocess.CalledProcessError:
        print("\n   ❌ Error installing dependencies")
        print("   Please run manually: pip install -r requirements.txt")
        return False

def setup_api_key():
    """Guide user through API key setup"""
    print("✓ Setting up API key...\n")
    
    if os.path.exists('.env'):
        response = input("   .env file already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("   Keeping existing .env file\n")
            return True
    
    print("\n   📋 API Key Options:")
    print("   1. Groq (Recommended - FREE & FAST)")
    print("   2. OpenAI (Paid)")
    print("   3. Skip for now\n")
    
    choice = input("   Select option (1-3): ")
    
    if choice == '1':
        print("\n   🔑 Setting up Groq API:")
        print("   1. Go to https://console.groq.com/")
        print("   2. Create a free account")
        print("   3. Generate an API key")
        print("   4. Copy the key (starts with 'gsk_')\n")
        
        api_key = input("   Paste your Groq API key: ").strip()
        
        if not api_key.startswith('gsk_'):
            print("   ⚠️  Warning: Groq keys usually start with 'gsk_'")
            response = input("   Continue anyway? (y/n): ")
            if response.lower() != 'y':
                return False
        
        with open('.env', 'w') as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        
        print("   ✅ API key saved to .env\n")
        return True
        
    elif choice == '2':
        print("\n   🔑 Setting up OpenAI API:")
        print("   1. Go to https://platform.openai.com/api-keys")
        print("   2. Create an API key")
        print("   3. Copy the key (starts with 'sk-')\n")
        
        api_key = input("   Paste your OpenAI API key: ").strip()
        
        if not api_key.startswith('sk-'):
            print("   ⚠️  Warning: OpenAI keys usually start with 'sk-'")
            response = input("   Continue anyway? (y/n): ")
            if response.lower() != 'y':
                return False
        
        with open('.env', 'w') as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        
        print("   ✅ API key saved to .env\n")
        return True
        
    else:
        print("\n   ⚠️  Skipping API key setup")
        print("   You'll need to create .env file manually before running the app\n")
        return True

def create_directories():
    """Create necessary directories"""
    print("✓ Creating directories...")
    
    dirs = ['uploads', 'reports', 'templates', 'static/css']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
    
    print("   ✅ All directories created\n")
    return True

def final_instructions():
    """Print final instructions"""
    print("="*70)
    print("✅ SETUP COMPLETE!")
    print("="*70)
    print("\n📋 Next Steps:\n")
    print("1. Make sure you have a resume (PDF/DOCX/TXT)")
    print("2. Prepare a job description file")
    print("3. Run the application:\n")
    print("   python app.py\n")
    print("4. Open your browser to: http://localhost:5000\n")
    print("="*70)
    print("\n💡 Tips:")
    print("   - Use Chrome or Edge for best speech recognition")
    print("   - Find a quiet room with good lighting")
    print("   - Test your microphone before starting")
    print("   - Keep answers 30-90 seconds long")
    print("\nGood luck with your interview practice! 🎯\n")

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("⚠️  Warning: Some dependencies may not be installed")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Setup API key
    if not setup_api_key():
        print("⚠️  Warning: API key not configured")
        print("You'll need to create a .env file manually")
    
    # Create directories
    create_directories()
    
    # Print final instructions
    final_instructions()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)
