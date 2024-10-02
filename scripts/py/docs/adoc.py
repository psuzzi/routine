import os
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
import re
from rich import print

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

def resolve(string_path):
    return Path(SCRIPT_DIR, string_path).resolve()

ADOC_BASE_DIR = resolve('../../../docs/adoc')
OUTPUT_DIR = resolve("../../../docs/gen")

# Conversion tools
ASCIIDOC_TO_DOCBOOK = {
    'asciidoc': lambda input_file, output_file: (
        f"asciidoc -b docbook "
        f"-o {output_file} {input_file}"
    ),
    'asciidoctor': lambda input_file, output_file: (
        f"asciidoctor -b docbook "
        f"--trace "
        f"-o {output_file} {input_file}"
    )
}


DOCBOOK_TO_MARKDOWN = {
    'pandoc': lambda input_file, output_file: (
        f"pandoc -f docbook "
        f"-t markdown "
        f"-o {output_file} {input_file}"
    )
}

# main: Georgia, SF Pro, Palatino, Roboto, Libre Baskerville
# mono: Menlo, Fira Code, Consolas, Source Code Pro, Inconsolata
MAIN_FONT = "SF Pro"
MONO_FONT = "Fira Code"
HEADER_00_TEX_PATH = resolve('header-00.tex')
HEADER_01_TEX_PATH = resolve('header-01.tex')
HEADER_02_TEX_PATH = resolve('header-02.tex')
HEADER_03_TEX_PATH = resolve('header-03.tex')
LUA_FILTER_PATH = resolve('docbook_links.lua')

DOCBOOK_TO_PDF = {
    'pandoc': lambda input_file, output_file: (
        f"pandoc -f docbook "
        f"--pdf-engine=xelatex "
        f"-H '{HEADER_01_TEX_PATH}' "
        f"--lua-filter='{LUA_FILTER_PATH}' "
        f"-V documentclass=article "
        f"-V papersize=a4 "
        f"-V mainfont='{MAIN_FONT}' "
        f"-V monofont='{MONO_FONT}' "
        f"-V fontsize=11pt "  # Adjust this value to change the main font size
        f"-V geometry:margin=0.5in "
        f"--highlight-style=tango "
        f"-V colorlinks=true "
        f"-V linkcolor=blue "
#         f"--listings " #use listings for code blocks
#         f"--number-sections " # set section numbers
#         f"--toc " # add toc
        f"-o {output_file} {input_file}"
    )
}

def run_command(command):
    print(f" [blue]Executing[/blue]: {command}")  # Debug print
    result = subprocess.run(command, shell=True, capture_output=False, text=True)
    if result.returncode != 0:
        print(f"[red]Error executing command: {command}[/red]")
        print(f"Error message: {result.stderr}")
        sys.exit(1)
    return result.stdout

def add_creation_date(content):
    """Add creation date"""
    creation_date = datetime.now().strftime("%Y-%m-%d")
    return re.sub(r'(<info>)', f'\\1\n    <date>{creation_date}</date>', content)

def convert_tabs_to_spaces(content):
    """Convert tabs to double spaces"""
    return re.sub(r'(<programlisting[^>]*>.*?</programlisting>)',
#                   lambda m: re.sub(r'\t', '  ', m.group(1)),
                  lambda m: re.sub(r'    ', '  ', m.group(1)),
                  content, flags=re.DOTALL)

def postprocess_docbook(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    content = add_creation_date(content)
    content = convert_tabs_to_spaces(content)

    with open(file_path, 'w') as f:
        f.write(content)

def postprocess_markdown(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    # Remove curly brackets and IDs from headers
    content = re.sub(r'^(#+\s.*?)\s+{#.*?}$', r'\1', content, flags=re.MULTILINE)

    # Convert "-   " to "- " for unordered list items
    content = re.sub(r'(?m)^-   ', '- ', content)

    # Convert "1.  " to "1. " for ordered list items (and similar for other numbers)
    content = re.sub(r'(?m)^(\d+)\.  ', r'\1. ', content)

    # Aggressively remove empty lines between list items (both ordered and unordered)
    content = re.sub(r'(\n(?:- |\d+\. ).*?)(\n+)(?=(?:- |\d+\. ))', r'\1\n', content, flags=re.DOTALL)

    # Ensure single newline after each header
    content = re.sub(r'^(#+\s.*?)(\n+)', r'\1\n', content, flags=re.MULTILINE)

    # Remove any remaining {#id} tags
    content = re.sub(r'\s*{#.*?}', '', content)

    # Ensure proper spacing around code blocks
    content = re.sub(r'```(\w+)\n', r'\n```\1\n', content)
    content = re.sub(r'\n```\n', r'\n\n```\n\n', content)

    # Remove extra newlines, but keep one empty line before and after lists
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Ensure single newline between paragraphs and lists (both ordered and unordered)
    content = re.sub(r'(\S)\n\n+((?:- |\d+\. ))', r'\1\n\n\2', content)

    # Final pass to remove any remaining empty lines between list items (both ordered and unordered)
    content = re.sub(r'((?:- |\d+\. ).*?\n)\n+((?:- |\d+\. ))', r'\1\2', content, flags=re.DOTALL)

    # Transform note sections (including those with lists)
    def note_replacement(match):
        note_content = match.group(1).strip()
        # Remove any leading newlines and extra spaces before list items
        note_content = re.sub(r'^\s*-\s*', '- ', note_content, flags=re.MULTILINE)
        return f"**Note:**\n{note_content}"

    content = re.sub(r':::: note\n::: title\n:::\n(.*?)::::',
                     note_replacement,
                     content, flags=re.DOTALL)

    with open(file_path, 'w') as file:
        file.write(content)

def convert_asciidoc(input_path, out_dir, output_formats):
    """Convert AsciiDoc to DocBook XML and other formats as requested"""

    docbook_file = out_dir / f"{input_path.stem}.xml"
    run_command(ASCIIDOC_TO_DOCBOOK['asciidoctor'](input_path, docbook_file))

    # Check if the docbook file was generated
    if not os.path.exists(docbook_file):
        print(f"Error: DocBook file not generated: {docbook_file}")
        sys.exit(1)

    # Postprocess DocBook
    postprocess_docbook(docbook_file)

    # Convert to other formats if requested
    if 'md' in output_formats:
        md_file = out_dir / f"{input_path.stem}.md"
        run_command(DOCBOOK_TO_MARKDOWN['pandoc'](docbook_file, md_file))
        postprocess_markdown(md_file)
    if 'pdf' in output_formats:
        pdf_file = out_dir / f"{input_path.stem}.pdf"
        run_command(DOCBOOK_TO_PDF['pandoc'](docbook_file, pdf_file))
    # Remove docbook if unwanted
    if 'docbook' not in output_formats:
            os.remove(docbook_file)


def main():
    parser = argparse.ArgumentParser(description="Convert AsciiDoc to DocBook, Markdown, and PDF")
    parser.add_argument("--docbook", action="store_true", help="Output DocBook")
    parser.add_argument("--md", action="store_true", help="Output Markdown")
    parser.add_argument("--pdf", action="store_true", help="Output PDF")
    args = parser.parse_args()

    output_formats = []
    if args.docbook:
        output_formats.append('docbook')
    if args.md:
        output_formats.append('md')
    if args.pdf:
        output_formats.append('pdf')

    for root, dir, files in os.walk(ADOC_BASE_DIR):
        for file in files:
            if file.endswith('.adoc'):
                input_path = os.path.join(root, file)

                rel_path = os.path.relpath(root, ADOC_BASE_DIR)
                output_dir = os.path.join(OUTPUT_DIR, rel_path)
                os.makedirs(output_dir, exist_ok=True)

                print(f"\n[blue]Converting[/blue] {input_path} into {output_dir}")
                convert_asciidoc(Path(input_path), Path(output_dir), output_formats)

if __name__ == "__main__":
    main()

