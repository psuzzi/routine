# File: init-app/utils/project_initializer.py

import yaml
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from .generation_utils import GenerationUtils

class ProjectInitializer:
    def __init__(self, base_dir, config_file_path, description):
        self.base_dir = Path(base_dir).resolve()
        self.config_file_path = config_file_path
        self.description = description
        print(f'init\n Base Dir: {base_dir}\n Config File Path: {config_file_path}')

    def resolve_path(self, path):
        """Resolve path relative to the config script's location."""
        return (self.base_dir / path).resolve()

    def setup_argparser(self):
        parser = argparse.ArgumentParser(description=self.description)
        parser.add_argument('--config', default=self.config_file_path, help='Path to configuration file')
        parser.add_argument('--remove', action='store_true', help='Remove empty directories and files in the project structure.')
        parser.add_argument('--remove-all', action='store_true', help='Remove all specified directories and their contents.')
        return parser.parse_args()

    def run(self):
        args = self.setup_argparser()

        # Load YAML configuration
        config_path = self.resolve_path(args.config)
        print(f'config_path: {config_path}')
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Resolve paths in config
        config['init']['basedir'] = self.resolve_path(config['init']['basedir'])
        config['init']['templates'] = self.resolve_path(config['init']['templates'])
        config['init']['structure'] = self.resolve_path(config['init']['structure'])

        print(f'basedir: {config['init']['basedir']}')
        print(f'templates: {config['init']['templates']}')
        print(f'structure: {config['init']['structure']}')

        # Setup Jinja2 environment
        env = Environment(loader=FileSystemLoader(config['init']['templates']))
        env.filters['toFolder'] = lambda package: package.replace('.', '/')
        env.filters['toTitleCase'] = lambda s: s.replace('_', ' ').title()

         # Load and render structure from template
        with open(config['init']['structure'], 'r') as f:
            structure_template = f.read()
        structure = yaml.safe_load(GenerationUtils.render_template(structure_template, config, env))

        if args.remove or args.remove_all:
            GenerationUtils.remove_structure(structure, config['init']['basedir'], remove_all=args.remove_all)
            print(f"{self.description} structure removal complete.")
        else:
            GenerationUtils.create_structure(structure, config['init']['basedir'], config['init']['templates'], config, env)
            print(f"{self.description} structure created successfully!")