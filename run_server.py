#!/usr/bin/env python3
"""
Production server script for Timesheet Management System
Run this script to start the Flask application for network access
"""

import os
import sys
from main import app

if __name__ == '__main__':
    # Configuration
    HOST = '0.0.0.0'  # Allow external connections
    PORT = int(os.environ.get('PORT', 8080))  # Use environment variable or default to 8080
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("=" * 60)
    print("🚀 Timesheet Management System")
    print("=" * 60)
    print(f"📍 Server: {HOST}:{PORT}")
    print(f"🔧 Debug Mode: {DEBUG}")
    print(f"🌐 Network Access: Enabled")
    print("=" * 60)
    print("📱 Access from other devices on your network:")
    print("   - Find your computer's IP address")
    print("   - Use: http://YOUR_IP:8080")
    print("=" * 60)
    
    try:
        app.run(
            host=HOST,
            port=PORT,
            debug=DEBUG,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1) 