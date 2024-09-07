# Init App Dynamic Project Structure Generator

This Python script generates a project structure based on a YAML configuration file and a templated structure definition. 
It uses Jinja2 for templating, allowing for dynamic creation of both the directory structure and file contents.

## Features

- Dynamic configuration using YAML
- Templating for both structure definition and file contents
- Custom filters for operations like `toFolder()` and `toTitleCase()`
- Options to create or remove the project structure

## Setup
1. Ensure you have Python 3.6+ installed.
2. Set up a virtual environment as explained in [../README.md](../README.md)

## Configuration

1. Create an [init-app-config.yaml](init-app-config.yaml) file with your project configuration:
   ```yaml
   init:
      # base directory of the project
      basedir: ../../../target
      # directory where the templates are stored
      templates: ./templates
      # file representing the project structure
      structure: ./init-app-structure-template.yaml
   
   # application details
   app:
      title: Routine App
      name: routine
      group: dev.algo
      package: dev.algo.routine
   ```

2. Create a [init-app-structure-template.yaml](init-app-structure-template.yaml) file defining your project structure using Jinja2 syntax:
   ```yaml
   backend:
    src/main/java/{{ app.package | toFolder }}: null
    src/main/resources: null
    src/test/java/{{ app.package | toFolder }}: null
    pom.xml: backend_pom.xml
    README.md: backend_readme.md
   frontend:
    src: null
    public: null
    package.json: frontend_package.json
    README.md: frontend_readme.md
   ...
   ```

3. Create template files in the `templates` directory. These can use Jinja2 syntax, e.g., `pom.xml`:
   ```xml
   <project>
    <groupId>{{ app.group }}</groupId>
    <artifactId>{{ app.name }}-app</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>{{ app.name }}-app</name>
    <description>{{ app.title }} Backend</description>
   </project>
   ```

## Usage

1. To create the project structure:
   ```
   python3 init-app.py
   ```

2. To remove empty directories and files:
   ```
   python3 init-app.py --remove
   ```

3. To remove all specified directories and their contents:
   ```
   python3 init-app.py --remove-all
   ```

4. To use a different configuration file:
   ```
   python3 init-app.py --config path/to/config.yaml
   ```

## Templating Mechanism

- The script uses Jinja2 for templating.
- Custom filters `toFolder` and `toTitleCase` are available in templates.
- The entire configuration object is passed to templates, accessible via keys like `{{ application.name }}`.

## Extending the Script

- Add more custom filters in the Python script.
- Modify the `create_structure` function to handle more complex file generation logic.
- Extend the configuration schema to include more project-specific settings.

Remember to keep your virtual environment activated when running the script. To deactivate the virtual environment, simply run `deactivate`.