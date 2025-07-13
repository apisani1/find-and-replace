# Find and Replace

A command-line tool for finding and replacing text in files using regular expressions. This tool provides an intuitive interface for bulk text operations across your project files.

## Features

- **Regular Expression Support**: Use regex patterns for complex search and replace operations
- **Glob Pattern Matching**: Find files using glob expressions like `*.py`, `config.*`, etc.
- **Recursive Search**: Search through directory trees with the `-r/--recursive` flag
- **Interactive Confirmation**: Review matches before making changes (unless using `--no-confirm`)
- **Dry Run Mode**: Preview what would be changed without making actual modifications
- **Error Handling**: Graceful handling of permission errors, encoding issues, and invalid regex patterns
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Quick Start

### Installation

Install from PyPI:

```bash
pip install find-replace-cli
```

### Basic Usage

Replace all instances of "old_function" with "new_function" in Python files:

```bash
find-and-replace "*.py" /path/to/project "old_function" "new_function"
```

### Common Examples

**Replace text in all files recursively:**
```bash
find-and-replace "*.txt" . "hello.*world" "hi universe" -r
```

**Update version strings in configuration files:**
```bash
find-and-replace "config.json" ~/projects "\"version\":\s*\"[^\"]*\"" "\"version\": \"2.0.0\"" -r
```

**Dry run to preview changes:**
```bash
find-and-replace "*.py" . "old_pattern" "new_pattern" --dry-run
```

**No confirmation prompts (automation-friendly):**
```bash
find-and-replace "*.md" . "old_text" "new_text" -r -n
```

## Use Cases

- **Code Refactoring**: Rename functions, variables, or classes across your codebase
- **Configuration Updates**: Update configuration values across multiple files
- **Documentation Maintenance**: Update links, references, or terminology in documentation
- **Migration Tasks**: Update import statements, API calls, or deprecated syntax
- **Bulk Text Processing**: Any scenario requiring consistent text changes across multiple files

## Safety Features

- **Interactive Confirmation**: By default, the tool shows you what will be changed and asks for confirmation
- **Dry Run Mode**: Test your patterns without making any changes
- **Detailed Output**: See exactly what files were processed and how many matches were found
- **Error Recovery**: Continues processing other files even if one file encounters an error

## Command Line Arguments

```
find-and-replace FILE_PATTERN DIRECTORY FIND_PATTERN REPLACE_TEXT [OPTIONS]
```

**Positional Arguments:**
- `FILE_PATTERN`: Glob pattern for file names (e.g., `*.py`, `config.*`)
- `DIRECTORY`: Directory to search in
- `FIND_PATTERN`: Regular expression pattern to find
- `REPLACE_TEXT`: Text to replace matches with (supports regex groups like `\1`, `\2`)

**Options:**
- `-r, --recursive`: Search subdirectories recursively
- `-n, --no-confirm`: Skip confirmation prompts
- `--dry-run`: Show what would be changed without making changes
- `-h, --help`: Show help message

## Getting Help

- **Documentation**: Read the full documentation at [find-and-replace.readthedocs.io](https://find-and-replace.readthedocs.io/)
- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/apisani1/find-and-replace/issues)
- **Source Code**: View the source code on [GitHub](https://github.com/apisani1/find-and-replace)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/apisani1/find-and-replace/blob/main/LICENSE) file for details.