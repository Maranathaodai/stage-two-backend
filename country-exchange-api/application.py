# WSGI wrapper for Elastic Beanstalk (if using Python platform)
# Note: This is a workaround. Better to use Docker platform for FastAPI.

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import your FastAPI app
from main import app

# For Elastic Beanstalk Python platform (WSGI)
# This won't work well with async FastAPI. Use Docker platform instead.
application = app

