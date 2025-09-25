"""
Unit tests for the TODO Comment Checker GitHub Action.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from todo_checker import TodoChecker
from github_client import GitHubClient


class TestTodoChecker(unittest.TestCase):
    """Test cases for TodoChecker class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = TodoChecker("TODO:", "💡 **TODO Found**")
    
    def test_find_todos_in_diff(self):
        """Test finding TODOs in git diff."""
        sample_diff = """diff --git a/src/main.py b/src/main.py
index 1234567..abcdefg 100644
--- a/src/main.py
+++ b/src/main.py
@@ -10,6 +10,8 @@ def main():
     print("Hello World")
+    # TODO: Add error handling here
+    # FIXME: This needs refactoring
     return 0
 
+# TODO: Implement logging functionality
 def helper():
     pass"""
        
        todos = self.checker.find_todos_in_diff(sample_diff)
        
        self.assertEqual(len(todos), 2)
        self.assertEqual(todos[0]['file'], 'src/main.py')
        self.assertIn('TODO:', todos[0]['content'])
        self.assertEqual(todos[1]['todo_text'], 'Implement logging functionality')
    
    def test_format_comment_body(self):
        """Test comment body formatting."""
        todo = {
            'file': 'src/test.py',
            'line': 42,
            'content': '    # TODO: Fix this bug',
            'todo_text': 'Fix this bug',
            'pattern': 'TODO:'
        }
        
        body = self.checker.format_comment_body(todo)
        
        self.assertIn('💡 **TODO Found**', body)
        self.assertIn('src/test.py', body)
        self.assertIn('42', body)
        self.assertIn('Fix this bug', body)


class TestGitHubClient(unittest.TestCase):
    """Test cases for GitHubClient class."""
    
    @patch('github.Github')
    def setUp(self, mock_github):
        """Set up test fixtures."""
        self.mock_repo = MagicMock()
        mock_github.return_value.get_repo.return_value = self.mock_repo
        self.client = GitHubClient("fake_token", "owner/repo")
    
    def test_get_pr_number_from_event(self):
        """Test extracting PR number from event file."""
        # Test with pull request event
        event_data = {
            "pull_request": {
                "number": 123
            }
        }
        
        with patch('builtins.open', unittest.mock.mock_open()):
            with patch('json.load', return_value=event_data):
                pr_number = self.client.get_pr_number_from_event('/fake/path')
                self.assertEqual(pr_number, 123)
    
    @patch('builtins.open', unittest.mock.mock_open(read_data='invalid json'))
    def test_get_pr_number_from_invalid_event(self):
        """Test handling invalid event file."""
        pr_number = self.client.get_pr_number_from_event('/fake/path')
        self.assertIsNone(pr_number)


if __name__ == '__main__':
    unittest.main()
