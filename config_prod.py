import os

# Get environment variables
SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
basedir = os.path.abspath(os.path.dirname(__file__))

# Production configuration
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Database configuration
# For production, use environment variable or fall back to PostgreSQL
if os.environ.get('DATABASE_URL'):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # Handle PostgreSQL URL format for SQLAlchemy 1.4+
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
else:
    # Development fallback
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/fyyur'

SQLALCHEMY_TRACK_MODIFICATIONS = False
