#!/usr/bin/env python3
"""
Dedalus Tooling Dashboard - Production Startup Script
"""

import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == '__main__':
    print("🚀 Starting Dedalus Tooling Dashboard...")
    print("📊 Loading data and starting server...")
    
    try:
        from unified_dashboard import app
        
        # Production configuration
        port = int(os.environ.get('PORT', 8050))
        host = os.environ.get('HOST', '0.0.0.0')
        debug = os.environ.get('DEBUG', 'False').lower() == 'true'
        
        print(f"✅ Dedalus Dashboard starting at http://{host}:{port}")
        print("🔄 Press Ctrl+C to stop")
        
        app.run_server(
            host=host,
            port=port,
            debug=debug,
            dev_tools_hot_reload=False,
            dev_tools_ui=False
        )
        
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        sys.exit(1)
