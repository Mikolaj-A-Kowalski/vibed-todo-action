#!/usr/bin/env python3
"""
Entrypoint script for the TODO Comment Checker GitHub Action.
"""

import os
import sys
from src.todo_checker import TodoChecker
from src.github_client import GitHubClient


def main():
    """Main entrypoint for the GitHub Action."""
    try:
        # Get inputs from environment variables
        github_token = os.environ.get('INPUT_GITHUB-TOKEN')
        todo_pattern = os.environ.get('INPUT_TODO-PATTERN', 'TODO:')
        comment_prefix = os.environ.get('INPUT_COMMENT-PREFIX', '💡 **TODO Found**')
        
        # Get GitHub context
        github_repository = os.environ.get('GITHUB_REPOSITORY')
        github_event_path = os.environ.get('GITHUB_EVENT_PATH')
        github_workspace = os.environ.get('GITHUB_WORKSPACE')
        
        if not github_token:
            print("Error: github-token input is required")
            sys.exit(1)
            
        if not github_repository:
            print("Error: GITHUB_REPOSITORY environment variable not found")
            sys.exit(1)
            
        if not github_workspace:
            print("Error: GITHUB_WORKSPACE environment variable not found")
            sys.exit(1)
        
        print(f"Repository: {github_repository}")
        print(f"Workspace: {github_workspace}")
        print(f"TODO Pattern: {todo_pattern}")
        
        # Initialize clients
        github_client = GitHubClient(github_token, github_repository)
        todo_checker = TodoChecker(todo_pattern, comment_prefix)
        
        # Get PR number from event
        pr_number = github_client.get_pr_number_from_event(github_event_path)
        if not pr_number:
            print("Not running on a pull request event, skipping...")
            return
            
        print(f"Processing PR #{pr_number}")
        
        # Get git diff
        git_diff = todo_checker.get_git_diff(github_workspace)
        
        # Find TODOs in diff
        todos = todo_checker.find_todos_in_diff(git_diff)
        
        print(f"Found {len(todos)} TODO comments")
        
        # Create PR comments
        comments_created = 0
        for todo in todos:
            try:
                github_client.create_pr_comment(pr_number, todo)
                comments_created += 1
                print(f"Created comment for TODO at {todo['file']}:{todo['line']}")
            except Exception as e:
                print(f"Failed to create comment for {todo['file']}:{todo['line']}: {e}")
        
        # Set outputs
        print(f"::set-output name=todos-found::{len(todos)}")
        print(f"::set-output name=comments-created::{comments_created}")
        
        print(f"Successfully processed {comments_created} TODO comments")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
