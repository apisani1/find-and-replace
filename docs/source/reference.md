# Reference

This document provides detailed information about the find-and-replace CLI tool's components and functions.

## Command Line Interface

### Syntax

```
find-and-replace FILE_PATTERN DIRECTORY FIND_PATTERN REPLACE_TEXT [OPTIONS]
```

### Arguments

#### Positional Arguments

**`FILE_PATTERN`**
: Glob pattern for matching file names
: **Type**: `str`
: **Examples**: `*.py`, `*.txt`, `config.*`, `package.json`
: **Description**: Supports standard glob wildcards (`*`, `?`, `[...]`)

**`DIRECTORY`**
: Directory to search in
: **Type**: `str`  
: **Examples**: `.`, `/path/to/project`, `~/documents`
: **Description**: Can be absolute or relative path. Tilde (`~`) expansion is supported.

**`FIND_PATTERN`**
: Regular expression pattern to search for
: **Type**: `str`
: **Examples**: `old_function`, `hello.*world`, `"version":\s*"[^"]*"`
: **Description**: Full Python regex syntax supported. Remember to escape special characters in shell.

**`REPLACE_TEXT`**
: Replacement text (can include regex groups)
: **Type**: `str`
: **Examples**: `new_function`, `hi universe`, `"version": "2.0.0"`
: **Description**: Supports backreferences (`\1`, `\2`, etc.) for captured groups.

#### Optional Arguments

**`-r, --recursive`**
: Search subdirectories recursively
: **Type**: `flag`
: **Default**: `False`
: **Description**: When enabled, searches through all subdirectories.

**`-n, --no-confirm`**
: Skip confirmation prompts
: **Type**: `flag`
: **Default**: `False`
: **Description**: Useful for automation scripts. Applies changes without user interaction.

**`--dry-run`**
: Show what would be changed without making actual changes
: **Type**: `flag`
: **Default**: `False`
: **Description**: Safe way to test patterns before applying them.

**`-h, --help`**
: Show help message and exit
: **Type**: `flag`

## Regular Expression Examples

### Basic Patterns

- `hello`: Matches literal text "hello"
- `hello.*world`: Matches "hello" followed by anything, then "world"
- `\d+`: Matches one or more digits
- `\w+`: Matches one or more word characters

### Advanced Patterns

- `"version":\s*"[^"]*"`: Matches JSON version fields
- `import\s+(\w+)`: Captures module names in import statements
- `function\s+(\w+)\s*\(`: Captures function names

### Replacement Examples

- `new_function`: Simple text replacement
- `\1_new`: Prepend "new_" to captured group 1
- `"version": "2.0.0"`: Replace with specific version

## Error Handling

The tool handles various error conditions gracefully:

- **File not found**: Skips missing files with warning
- **Permission denied**: Reports permission errors and continues
- **Unicode decode errors**: Skips binary files with informative message
- **Invalid regex**: Validates patterns before processing
- **Keyboard interrupt**: Clean exit on Ctrl+C

## Performance Considerations

- Files are processed sequentially
- Entire file content is loaded into memory
- Regex compilation is done once per pattern
- Large files (>100MB) may cause memory issues

## Best Practices

1. **Test with `--dry-run`** before making actual changes
2. **Use version control** to track changes
3. **Escape shell metacharacters** in patterns
4. **Start with simple patterns** and build complexity gradually
5. **Use `--no-confirm`** only for tested, automated scripts