#!/usr/bin/env python3
"""
UAT Server script for Timesheet Management System
Access via: http://uat-timesheet.local:8080
"""

import os
import sys
from main import app

if __name__ == '__main__':
    # UAT configuration
    HOST = '0.0.0.0'
    PORT = 8080
    DEBUG = True
    
    print("=" * 60)
    print("🌐 UAT TIMESHEET SYSTEM")
    print("=" * 60)
    print(f"📍 Server: {HOST}:{PORT}")
    print(f"🔧 Debug Mode: {DEBUG}")
    print(f"🌐 Network Access: Enabled")
    print("=" * 60)
    print("📱 Access URLs:")
    print("   - UAT Domain: http://uat-timesheet.local:8080")
    print("   - Local: http://localhost:8080")
    print("   - Network: http://YOUR_IP:8080")
    print("=" * 60)
    print("🛑 Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        # Set UAT environment
        os.environ['FLASK_ENV'] = 'uat'
        os.environ['FLASK_DEBUG'] = 'true'
        
        app.run(
            host=HOST,
            port=PORT,
            debug=DEBUG,
            threaded=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n🛑 UAT server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1) 