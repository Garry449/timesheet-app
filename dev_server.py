#!/usr/bin/env python3
"""
Development server script for Timesheet Management System
This is for development only - never use in production!
"""

import os
import sys
from main import app

if __name__ == '__main__':
    # Development configuration
    HOST = '0.0.0.0'
    PORT = 8080
    DEBUG = True
    
    print("=" * 60)
    print("🔧 DEVELOPMENT SERVER")
    print("=" * 60)
    print(f"📍 Server: {HOST}:{PORT}")
    print(f"🔧 Debug Mode: {DEBUG}")
    print(f"🌐 Network Access: Enabled")
    print(f"⚠️  WARNING: This is for development only!")
    print("=" * 60)
    print("📱 Access URLs:")
    print("   - Local: http://localhost:8080")
    print("   - Network: http://YOUR_IP:8080")
    print("=" * 60)
    print("🛑 Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        # Set development environment
        os.environ['FLASK_ENV'] = 'development'
        os.environ['FLASK_DEBUG'] = 'true'
        
        app.run(
            host=HOST,
            port=PORT,
            debug=DEBUG,
            threaded=True,
            use_reloader=True  # Auto-reload on file changes
        )
    except KeyboardInterrupt:
        print("\n🛑 Development server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1) 