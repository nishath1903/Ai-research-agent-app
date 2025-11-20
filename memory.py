import json
import os
from typing import List, Dict, Any

# Define the paths relative to the project root
MEMORY_FILE = os.path.join("data", "memory.json")
OUTPUT_FILE = os.path.join("data", "output.json")

def load_memory() -> List[Dict[str, Any]]:
    """Loads the research history from memory.json."""
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Warning: Could not load or decode memory.json. Starting with empty history.")
        return []

def save_memory(history: List[Dict[str, Any]]):
    """Saves the current research history to memory.json."""
    try:
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        with open(MEMORY_FILE, 'w') as f:
            json.dump(history, f, indent=4)
    except IOError as e:
        print(f"Error saving memory.json: {e}")

def save_output(data: Dict[str, Any]):
    """Saves the final consolidated output to output.json."""
    try:
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving output.json: {e}")