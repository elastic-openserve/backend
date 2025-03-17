from dotenv import load_dotenv
import os
import json
from typing import Dict, Any

def load_json_data(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return None
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def save_json_data(path: str, data: Dict[str, Any]):
    # Create the directory if it doesn't exist
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

def load_file_content(path: str) -> str:
    if not os.path.exists(path):
        return None
    with open(path, 'r') as file:
        content = file.read()
    return content
