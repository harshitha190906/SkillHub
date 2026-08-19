import sys
import os

# Add project root directory to Python path for PythonAnywhere WSGI
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

from app import app as application
