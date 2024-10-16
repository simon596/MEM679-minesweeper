import os, sys
# Get the absolute path to the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the '/src' directory
src_dir = os.path.join(current_dir, '..', 'src')
# Add '/src' to Python's module search path
sys.path.append(src_dir)