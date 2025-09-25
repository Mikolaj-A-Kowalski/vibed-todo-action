# TODO Comment Checker - Test Files

This directory contains test files to demonstrate the TODO checker functionality.

## Test Cases

The following files contain various TODO patterns for testing:

1. `sample_code.py` - Python file with TODO comments
2. `sample_code.js` - JavaScript file with TODO comments
3. `sample_code.md` - Markdown file with TODO comments

## Running Tests

To run the unit tests:

```bash
cd tests
python -m unittest test_todo_checker.py -v
```

## Manual Testing

1. Create a branch with changes to any of the sample files
2. Add TODO comments in various formats
3. Create a pull request
4. The GitHub Action should automatically detect and comment on the TODOs
