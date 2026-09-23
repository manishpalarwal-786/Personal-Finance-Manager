"""
main.py
-------
Entry point of the Personal Finance Manager application.
Run this file to start the program:

    python main.py
"""

import sys
import os

# Allow importing modules from the src/ folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from menu import run

if __name__ == "__main__":
    run()
