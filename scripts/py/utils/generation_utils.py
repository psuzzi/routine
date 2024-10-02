# File: init-app/utils/generation_utils.py

import yaml
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template, TemplateError
from pprint import pprint

class GenerationUtils:

    @staticmethod
    def render_template(template_str, data, env):
#         """Render a Jinja2 template string with given data."""
#         template = env.from_string(template_str)
#         return template.render(data)
        """Render a Jinja2 template string with given data and handle errors."""
        try:
            template = env.from_string(template_str)
            return template.render(data)
        except TemplateError as e:
            # Log the error and relevant details
            print("Error rendering template:")
            print(f"Template: {template_str}")
            print("Data: ")
            pprint(data)
            print(f"Error: {str(e)}")
            raise  # Re-raise the error after logging

    @staticmethod
    def create_structure(structure, base_path, template_dir, data, env):
        """Recursively create the project structure using provided structure."""
        for item, content in structure.items():
            path = Path(base_path) / item
            if isinstance(content, dict):
                # If content is a dict, it's a directory with nested structure
                path.mkdir(parents=True, exist_ok=True)
                GenerationUtils.create_structure(content, path, template_dir, data, env)
            elif content is None:
                # If content is None, it's an empty directory
                path.mkdir(parents=True, exist_ok=True)
            else:
                # If content is a string, it's a file with a template
                template_path = Path(template_dir) / content
                if template_path.exists():
                    with open(template_path, 'r') as f:
                        template_content = f.read()
                    rendered_content = GenerationUtils.render_template(template_content, data, env)
                    path.write_text(rendered_content)
                else:
                    print(f"Warning: Template {content} not found. Creating an empty file.")
                    path.touch()

    @staticmethod
    def remove_structure(structure, base_path, remove_all=False):
        """Recursively remove the project structure."""
        base_path = Path(base_path)
        for item, content in structure.items():
            path = base_path / item
            if not path.exists():
                continue

            if path.is_file():
                path.unlink()
                print(f"Removed file: {path}")
            elif path.is_dir():
                if remove_all:
                    # Remove all contents, including the manually created ones
                    shutil.rmtree(path)
                    print(f"Removed directory and all contents: {path}")
                else:
                    # Remove only the empty directories and files created by the script
                    if isinstance(content, dict):
                        GenerationUtils.remove_structure(content, path, remove_all)

                    if GenerationUtils.is_dir_empty_or_contains_only_empty_dirs(path):
                        shutil.rmtree(path)
                        print(f"Removed empty directory: {path}")
                    else:
                        print(f"Skipped non-empty directory: {path}")

    @staticmethod
    def is_dir_empty_or_contains_only_empty_dirs(path):
        """Check if a directory is empty or contains only empty directories."""
        if not path.is_dir():
            return False
        for item in path.iterdir():
            if item.is_file():
                return False
            if item.is_dir() and not GenerationUtils.is_dir_empty_or_contains_only_empty_dirs(item):
                return False
        return True