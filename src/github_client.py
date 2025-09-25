"""
GitHub client for interacting with GitHub API.
"""

import json
import os
from typing import Dict, Any, Optional
from github import Github


class GitHubClient:
    """Client for GitHub API interactions."""
    
    def __init__(self, token: str, repository: str):
        """
        Initialize GitHub client.
        
        Args:
            token: GitHub API token
            repository: Repository name in format "owner/repo"
        """
        self.github = Github(token)
        self.repository = self.github.get_repo(repository)
        self.repo_name = repository
        
    def get_pr_number_from_event(self, event_path: str) -> Optional[int]:
        """
        Get pull request number from GitHub event.
        
        Args:
            event_path: Path to GitHub event JSON file
            
        Returns:
            PR number if available, None otherwise
        """
        try:
            if not event_path or not os.path.exists(event_path):
                return None
                
            with open(event_path, 'r') as f:
                event_data = json.load(f)
                
            # Check if this is a pull request event
            if 'pull_request' in event_data:
                return event_data['pull_request']['number']
                
            # Check if this is a push event that might be related to a PR
            if event_data.get('ref', '').startswith('refs/pull/'):
                # Extract PR number from ref like refs/pull/123/merge
                import re
                match = re.search(r'refs/pull/(\d+)/', event_data['ref'])
                if match:
                    return int(match.group(1))
                    
            return None
            
        except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
            print(f"Failed to parse event file: {e}")
            return None
    
    def create_pr_comment(self, pr_number: int, todo: Dict[str, Any]) -> None:
        """
        Create a comment on a pull request for a TODO item.
        
        Args:
            pr_number: Pull request number
            todo: TODO item dictionary
        """
        try:
            pr = self.repository.get_pull(pr_number)
            
            # Format comment body
            comment_body = self._format_comment_body(todo)
            
            # Try to create a review comment on the specific line
            try:
                # Get the commit SHA for the PR head
                commit = pr.head.sha
                
                # Create a review comment on the specific line
                pr.create_review_comment(
                    body=comment_body,
                    commit_id=commit,
                    path=todo['file'],
                    line=todo['line']
                )
                print(f"Created review comment on line {todo['line']} of {todo['file']}")
                
            except Exception as review_error:
                print(f"Failed to create review comment, falling back to issue comment: {review_error}")
                
                # Fallback: create a regular issue comment
                pr.create_issue_comment(comment_body)
                print(f"Created issue comment for TODO in {todo['file']}")
                
        except Exception as e:
            print(f"Failed to create PR comment: {e}")
            raise
    
    def _format_comment_body(self, todo: Dict[str, Any]) -> str:
        """
        Format the comment body for a TODO item.
        
        Args:
            todo: TODO item dictionary
            
        Returns:
            Formatted comment body
        """
        return f"""💡 **TODO Found**

A new TODO comment was found in this pull request:

**File:** `{todo['file']}`
**Line:** {todo['line']}
**Content:** 
```
{todo['content']}
```

{f"**TODO:** {todo['todo_text']}" if todo['todo_text'] else ""}

Please make sure to address this TODO before merging or create a follow-up issue to track it."""
    
    def get_pr_files(self, pr_number: int) -> list:
        """
        Get list of changed files in a pull request.
        
        Args:
            pr_number: Pull request number
            
        Returns:
            List of changed files
        """
        try:
            pr = self.repository.get_pull(pr_number)
            return list(pr.get_files())
        except Exception as e:
            print(f"Failed to get PR files: {e}")
            return []
