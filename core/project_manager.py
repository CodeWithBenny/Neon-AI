import os
import json
from pathlib import Path
from typing import Dict, List


class ProjectManager:
    def __init__(self, project_root: str = None):
        self.project_root = project_root or os.getcwd()
        self.file_tree = {}
        self.open_files = {}

    def load_project(self, path: str = None):
        """Load a project directory structure"""
        self.project_root = path or self.project_root
        self.file_tree = self._build_file_tree(self.project_root)
        return self.file_tree

    def _build_file_tree(self, path: str) -> Dict:
        """Recursively build a file tree structure"""
        tree = {"name": os.path.basename(path), "path": path}
        if os.path.isdir(path):
            tree["type"] = "directory"
            tree["children"] = [
                self._build_file_tree(os.path.join(path, name))
                for name in os.listdir(path)
                if not name.startswith('.')
            ]
        else:
            tree["type"] = "file"
        return tree

    def open_file(self, file_path: str) -> str:
        """Open and cache a file"""
        with open(file_path, 'r') as f:
            content = f.read()
        self.open_files[file_path] = content
        return content

    def save_file(self, file_path: str, content: str):
        """Save file content"""
        with open(file_path, 'w') as f:
            f.write(content)
        self.open_files[file_path] = content