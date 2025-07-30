#!/usr/bin/env python3
"""
Railway Deployment Script for Timesheet Management System
This script helps you deploy your Flask app to Railway
"""

import os
import subprocess
import sys

def check_git():
    """Check if Git is installed and initialized"""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git is installed")
            return True
        else:
            print("❌ Git is not installed")
            return False
    except FileNotFoundError:
        print("❌ Git is not installed")
        return False

def check_railway_cli():
    """Check if Railway CLI is installed"""
    try:
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Railway CLI is installed")
            return True
        else:
            print("❌ Railway CLI is not installed")
            return False
    except FileNotFoundError:
        print("❌ Railway CLI is not installed")
        return False

def install_railway_cli():
    """Install Railway CLI"""
    print("📥 Installing Railway CLI...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'railway'], check=True)
        print("✅ Railway CLI installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Railway CLI")
        return False

def initialize_git():
    """Initialize Git repository if not already done"""
    if not os.path.exists('.git'):
        print("📁 Initializing Git repository...")
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
        print("✅ Git repository initialized")
    else:
        print("✅ Git repository already exists")

def create_railway_project():
    """Create Railway project"""
    print("🚀 Creating Railway project...")
    try:
        subprocess.run(['railway', 'login'], check=True)
        subprocess.run(['railway', 'init'], check=True)
        print("✅ Railway project created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create Railway project: {e}")
        return False

def deploy_to_railway():
    """Deploy to Railway"""
    print("🚀 Deploying to Railway...")
    try:
        subprocess.run(['railway', 'up'], check=True)
        print("✅ Deployment successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 Railway Deployment Setup")
    print("=" * 60)
    
    # Check prerequisites
    if not check_git():
        print("Please install Git first: https://git-scm.com/")
        return
    
    if not check_railway_cli():
        if not install_railway_cli():
            print("Please install Railway CLI manually: npm install -g @railway/cli")
            return
    
    # Initialize Git
    initialize_git()
    
    # Create Railway project
    if not create_railway_project():
        return
    
    # Deploy
    if deploy_to_railway():
        print("\n🎉 Your app is now deployed to Railway!")
        print("📱 Check your Railway dashboard for the URL")
        print("🔗 You can also run: railway status")
    else:
        print("\n❌ Deployment failed. Check the error messages above.")

if __name__ == '__main__':
    main() 