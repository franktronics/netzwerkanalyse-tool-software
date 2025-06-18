import json
import os
from ..ports import FileManagerPort

class FileManagerAdapter(FileManagerPort):
    def __init__(self):
        self.json_cache: dict[str, dict] = {}

    def load_json_file(self, file_path: str) -> dict | None:
        if file_path in self.json_cache:
            return self.json_cache[file_path]

        abs_path = os.path.abspath(file_path)
        try:
            with open(abs_path, 'r') as f:
                data = json.load(f)
                self.json_cache[file_path] = data
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return None
        except Exception as e:
            print(f"Error loading JSON file {file_path}: {e}")
            return None