"""
TodoChecker module for finding TODO comments in git diffs.
"""

import subprocess
import re
from typing import List, Dict, Any


class TodoChecker:
    """Class for finding TODO comments in git diffs."""
    
    def __init__(self, todo_pattern: str = "TODO:", comment_prefix: str = "💡 **TODO Found**"):
        """
        Initialize TodoChecker.
        
        Args:
            todo_pattern: Pattern to search for (default: "TODO:")
            comment_prefix: Prefix for PR comments
        """
        self.todo_pattern = todo_pattern
        self.comment_prefix = comment_prefix
        
    def get_git_diff(self, workspace_path: str) -> str:
        """
        Get git diff for the current changes.
        
        Args:
            workspace_path: Path to the git repository
            
        Returns:
            Git diff as string
        """
        try:
            # Get diff between base and head
            result = subprocess.run(
                ["git", "diff", "origin/master...HEAD"],
                cwd=workspace_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            # Fallback to staged changes if the above fails
            try:
                result = subprocess.run(
                    ["git", "diff", "--cached"],
                    cwd=workspace_path,
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.stdout
            except subprocess.CalledProcessError:
                # Final fallback to unstaged changes
                result = subprocess.run(
                    ["git", "diff"],
                    cwd=workspace_path,
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.stdout
    
    def find_todos_in_diff(self, git_diff: str) -> List[Dict[str, Any]]:
        """
        Find TODO comments in git diff.
        
        Args:
            git_diff: Git diff content
            
        Returns:
            List of TODO items with file, line, and content information
        """
        todos = []
        current_file = None
        line_number = 0
        
        lines = git_diff.split('\n')
        
        for i, line in enumerate(lines):
            # Track current file being processed
            if line.startswith('+++'):
                # Extract filename from +++ b/filename
                current_file = line[6:] if line.startswith('+++ b/') else line[4:]
                line_number = 0
                continue
                
            # Track line numbers (simplified approach)
            if line.startswith('@@'):
                # Parse hunk header to get line number
                # Format: @@ -old_start,old_count +new_start,new_count @@
                match = re.search(r'\+(\d+)', line)
                if match:
                    line_number = int(match.group(1)) - 1
                continue
            
            # Only look at added lines
            if line.startswith('+') and not line.startswith('+++'):
                line_number += 1
                # Check if line contains TODO pattern
                if self.todo_pattern.lower() in line.lower():
                    # Extract the TODO content
                    todo_content = line[1:].strip()  # Remove the '+' prefix
                    
                    # Find the position of the TODO pattern (case insensitive)
                    todo_match = re.search(re.escape(self.todo_pattern), todo_content, re.IGNORECASE)
                    if todo_match:
                        # Extract everything after the TODO pattern
                        todo_text = todo_content[todo_match.end():].strip()
                        
                        todos.append({
                            'file': current_file,
                            'line': line_number,
                            'content': todo_content,
                            'todo_text': todo_text,
                            'pattern': self.todo_pattern
                        })
            elif not line.startswith('-'):
                # Count non-removed lines
                line_number += 1
                
        return todos
    
    def format_comment_body(self, todo: Dict[str, Any]) -> str:
        """
        Format the comment body for a TODO item.
        
        Args:
            todo: TODO item dictionary
            
        Returns:
            Formatted comment body
        """
        return f"""{self.comment_prefix}

A new TODO comment was found in this pull request:

**File:** `{todo['file']}`
**Line:** {todo['line']}
**Content:** 
```
{todo['content']}
```

{f"**TODO:** {todo['todo_text']}" if todo['todo_text'] else ""}

Please make sure to address this TODO before merging or create a follow-up issue to track it."""
