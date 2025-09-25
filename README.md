# TODO Comment Checker GitHub Action

A GitHub Action that automatically searches git diffs for `TODO:` comments and creates pull request comments to highlight them.

## Features

- 🔍 Scans git diffs for TODO comments in pull requests
- 💬 Creates PR comments for each TODO found
- 🎯 Supports custom TODO patterns
- 📍 Shows exact file and line number for each TODO
- 🔧 Configurable comment formatting

## Usage

### Basic Usage

Add the following workflow to your repository in `.github/workflows/todo-checker.yml`:

```yaml
name: TODO Checker

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  check-todos:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Check for TODOs
        uses: ./
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Advanced Usage

```yaml
name: TODO Checker

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  check-todos:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Check for TODOs
        uses: ./
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          todo-pattern: 'TODO:|FIXME:|HACK:'
          comment-prefix: '⚠️ **Action Required**'
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `github-token` | GitHub token for API access | Yes | N/A |
| `todo-pattern` | Pattern to search for TODO comments | No | `TODO:` |
| `comment-prefix` | Prefix for PR comments | No | `💡 **TODO Found**` |

## Outputs

| Output | Description |
|--------|-------------|
| `todos-found` | Number of TODO comments found |
| `comments-created` | Number of PR comments created |

## Example Output

When a TODO is found, the action will create a comment like this:

> 💡 **TODO Found**
>
> A new TODO comment was found in this pull request:
>
> **File:** `src/main.py`  
> **Line:** 42  
> **Content:**
> ```
> # TODO: Add proper error handling here
> ```
>
> **TODO:** Add proper error handling here
>
> Please make sure to address this TODO before merging or create a follow-up issue to track it.

## Development

### Local Testing

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   python -m pytest tests/
   ```

### Building the Docker Image

```bash
docker build -t todo-checker .
```

### Project Structure

```
.
├── action.yml              # Action metadata
├── Dockerfile              # Container definition
├── requirements.txt        # Python dependencies
├── entrypoint.py          # Main entry point
├── src/
│   ├── todo_checker.py    # Core TODO detection logic
│   └── github_client.py   # GitHub API interactions
├── tests/
│   └── test_todo_checker.py # Unit tests
└── README.md              # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. **"Not running on a pull request event"**: Make sure your workflow is triggered by `pull_request` events.

2. **Permission errors**: Ensure the `github-token` has the necessary permissions to read repository content and create PR comments.

3. **No TODOs found**: Check that your `todo-pattern` matches the format of your TODO comments.

### Debugging

Enable debug logging by setting the `ACTIONS_STEP_DEBUG` secret to `true` in your repository settings.
