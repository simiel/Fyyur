import sys
import os

# Add the parent directory to the Python path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel expects the app to be exposed as 'app'
# This is the WSGI application object
if __name__ == "__main__":
    app.run(debug=False)
