# AsciiDoc to Markdown Converter (Bash Script)

This bash script converts AsciiDoc files to Markdown format using Asciidoctor. 
It recursively searches for `.adoc` files in a specified directory and its subdirectories, converts them to Markdown, and saves the output in a parallel directory structure.

## Prerequisites

- Asciidoc
- Pandoc
- Latex engine

## Usage

1. Open `adoc_to_md.py` and modify `ADOC_BASE_DIR` and `OUTPUT_DIR` if needed.
2. Run the script as follow to generate docbook, markdown, and pdf:
   ```bash
   python3 adoc.py --docbook --md --pdf
   ```

The script will convert all `.adoc` files in `ADOC_BASE_DIR` and its subdirectories, saving Markdown files in `OUTPUT_DIR` while maintaining the original directory structure.

## Troubleshooting

If you encounter issues using asciidoctor:

1. Verify Asciidoctor installation:
   ```
   asciidoctor --version
   ```
2. Check script paths are correct for your project structure.
3. Ensure you have read permissions for the input directory and write permissions for the output directory.

### Asciidoctor Installation Issues on macOS

If you encounter permission errors installing asciidoctor on macOS, check your ruby environment and reinstall asciidoctor:

First, set up a local Ruby environment using rbenv, if you don't have one:
  ```bash
  # Install and set up rbenv
  brew install rbenv
  rbenv init
  # Install Ruby and set it as global
  rbenv install 3.2.2
  rbenv global 3.2.2
  # Restart shell and check ruby
  which ruby
  ruby -v
  ```
Then, when the environment is set, gem-install and verify asciidoctor
  ```bash
  # Install asciidoctor
  gem install asciidoctor
  # Check Asciidoctor
  which asciidoctor
  asciidoctor -v
  ```

### Installing TeX

To run the script, you need to install a full version of tex. 
As I develop on macOS, I installed mactex, as follows:

```bash
brew install --cask mactex
sudo tlmgr update --self
sudo tlmgr update --all
```

In case you run in issues when running tex, and you have basictex, you might want to uninstall it
```bash
brew uninstall --cask basictex
sudo rm -rf /usr/local/texlive
```

## Notes

- This script uses Asciidoctor for high-quality conversion of AsciiDoc files to DocBook XML.
- The script uses 
- The conversion process preserves the input files' directory structure.
- Adjust paths in the script as needed for your project structure.