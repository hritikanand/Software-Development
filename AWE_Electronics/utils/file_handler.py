import json

def read_json(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
