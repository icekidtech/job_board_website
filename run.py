#!/usr/bin/env python3

import os
from app import create_app

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Get environment variables
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"Starting Job Board application...")
    print(f"Visit: http://{host}:{port}")
    
    # Run the application
    app.run(host=host, port=port, debug=debug)