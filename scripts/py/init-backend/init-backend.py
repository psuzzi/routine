import yaml
import json
import shutil
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template, TemplateError
from pprint import pprint

# Config constants
CONFIG_FILE_PATH = 'init-backend-config.yaml'

def resolve_path(path):
    """Resolve path relative to the script's location."""
    return Path(__file__).parent.resolve() / path

def render_template(template_str, data, env):
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
#     """Render a Jinja2 template string with given data."""
#     template = env.from_string(template_str)
#     return template.render(data)


def create_structure(structure, base_path, template_dir, data, env):
    """Recursively create the project structure using provided structure."""
    for item, content in structure.items():
        path = Path(base_path) / item
        if isinstance(content, dict):
            # If content is a dict, it's a directory with nested structure
            path.mkdir(parents=True, exist_ok=True)
            create_structure(content, path, template_dir, data, env)
        elif content is None:
            # If content is None, it's an empty directory
            path.mkdir(parents=True, exist_ok=True)
        else:
            # If content is a string, it's a file with a template
            template_path = Path(template_dir) / content
            if template_path.exists():
                with open(template_path, 'r') as f:
                    template_content = f.read()
                rendered_content = render_template(template_content, data, env)
                path.write_text(rendered_content)
            else:
                print(f"Warning: Template {content} not found. Creating an empty file.")
                path.touch()

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
                    remove_structure(content, path, remove_all)

                if is_dir_empty_or_contains_only_empty_dirs(path):
                    shutil.rmtree(path)
                    print(f"Removed empty directory: {path}")
                else:
                    print(f"Skipped non-empty directory: {path}")

def is_dir_empty_or_contains_only_empty_dirs(path):
    """Check if a directory is empty or contains only empty directories."""
    if not path.is_dir():
        return False
    for item in path.iterdir():
        if item.is_file():
            return False
        if item.is_dir() and not is_dir_empty_or_contains_only_empty_dirs(item):
            return False
    return True

def main():
    """Main function to handle command-line arguments and manage the project structure."""
    parser = argparse.ArgumentParser(description="Manage project structure.")
    parser.add_argument('--config', default=CONFIG_FILE_PATH, help='Path to configuration file')
    parser.add_argument('--remove', action='store_true', help='Remove empty directories and files in the project structure.')
    parser.add_argument('--remove-all', action='store_true', help='Remove all specified directories and their contents.')
    args = parser.parse_args()

    # Load YAML configuration
    config_path = resolve_path(args.config)
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Resolve paths in config
    config['init']['basedir'] = resolve_path(config['init']['basedir'])
    config['init']['templates'] = resolve_path(config['init']['templates'])
    config['init']['structure'] = resolve_path(config['init']['structure'])
    
    # Setup Jinja2 environment and filters
    env = Environment(loader=FileSystemLoader(config['init']['templates']))
    env.filters['toFolder'] = lambda package: package.replace('.', '/')
    env.filters['toTitleCase'] = lambda s: s.replace('_', ' ').title()

    # Load and render structure from template
    structure_path = Path(__file__).parent / config['init']['structure']
    with open(structure_path, 'r') as f:
        structure_template = f.read()
    structure = yaml.safe_load(render_template(structure_template, config, env))

    if args.remove or args.remove_all:
        remove_structure(structure, config['init']['basedir'], remove_all=args.remove_all)
        print("Project structure removal complete.")
    else:
        create_structure(structure, config['init']['basedir'], config['init']['templates'], config, env)
        print("Project structure created successfully!")

if __name__ == "__main__":
    main()