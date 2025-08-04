#!/usr/bin/env python3
"""
Production server script for Timesheet Management System
Clean URL version - runs on port 80 (requires admin privileges)
"""

import os
import sys
import socket
from main import app

def get_local_ip():
    """Get the local IP address for network access"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

if __name__ == '__main__':
    # Clean URL configuration
    HOST = '0.0.0.0'
    PORT = 80  # Standard HTTP port - no need for :8080
    DEBUG = False
    LOCAL_IP = get_local_ip()
    
    print("=" * 70)
    print("🏢 TIMESHEET MANAGEMENT SYSTEM - CLEAN URL SERVER")
    print("=" * 70)
    print(f"📍 Server: {HOST}:{PORT}")
    print(f"🔧 Debug Mode: {DEBUG}")
    print(f"🌐 Network Access: Enabled")
    print(f"🔒 Security: Production Mode")
    print("=" * 70)
    print("📱 Clean Access URLs for Users:")
    print(f"   - Local: http://localhost")
    print(f"   - Network: http://{LOCAL_IP}")
    print("   - Custom Domain: http://timesheet.local (if configured)")
    print("=" * 70)
    print("👥 Multi-User Setup:")
    print("   1. Users can register at: http://[DOMAIN]/register")
    print("   2. Admin can manage users at: http://[DOMAIN]/admin")
    print("   3. Users login at: http://[DOMAIN]/login")
    print("=" * 70)
    print("⚠️  NOTE: This requires administrator privileges!")
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
            use_reloader=False
        )
    except PermissionError:
        print("❌ ERROR: Port 80 requires administrator privileges!")
        print("💡 Solutions:")
        print("   1. Run as Administrator")
        print("   2. Use port 8080 instead (edit PORT = 8080)")
        print("   3. Configure port forwarding")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Production server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1) 