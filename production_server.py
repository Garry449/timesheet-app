#!/usr/bin/env python3
"""
Production server script for Timesheet Management System
Optimized for multi-user access in local network
"""

import os
import sys
import socket
from main import app

def get_local_ip():
    """Get the local IP address for network access"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

if __name__ == '__main__':
    # Production configuration for multi-user access
    HOST = '0.0.0.0'  # Accept connections from any IP
    PORT = 8080
    DEBUG = False  # Disable debug mode for production
    LOCAL_IP = get_local_ip()
    
    print("=" * 70)
    print("🏢 TIMESHEET MANAGEMENT SYSTEM - PRODUCTION SERVER")
    print("=" * 70)
    print(f"📍 Server: {HOST}:{PORT}")
    print(f"🔧 Debug Mode: {DEBUG}")
    print(f"🌐 Network Access: Enabled")
    print(f"🔒 Security: Production Mode")
    print("=" * 70)
    print("📱 Access URLs for Users:")
    print(f"   - Local: http://localhost:{PORT}")
    print(f"   - Network: http://{LOCAL_IP}:{PORT}")
    print("=" * 70)
    print("👥 Multi-User Setup:")
    print("   1. Users can register at: http://[IP]:8080/register")
    print("   2. Admin can manage users at: http://[IP]:8080/admin")
    print("   3. Users login at: http://[IP]:8080/login")
    print("=" * 70)
    print("🛑 Press Ctrl+C to stop")
    print("=" * 70)
    
    try:
        # Set production environment
        os.environ['FLASK_ENV'] = 'production'
        os.environ['FLASK_DEBUG'] = 'false'
        
        app.run(
            host=HOST,
            port=PORT,
            debug=DEBUG,
            threaded=True,
            use_reloader=False  # Disable auto-reload for production
        )
    except KeyboardInterrupt:
        print("\n🛑 Production server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1) 