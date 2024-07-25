#!/usr/bin/env python3
"""
Unit tests for client.py
"""
import unittest
from client import GithubOrgClient
from parameterized import parameterized
from unittest.mock import Mock, patch


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for GithubOrgClient class.
    """
    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test the org method of GithubOrgClient to ensure
        it calls get_json with the correct URL.
        """
        # Arrange
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_response = {
            "repos_url": "https://api.github.com/orgs/{org}/repos"
        }
        mock_get_json.return_value = mock_response

        client = GithubOrgClient(org_name)

        # Act
        result = client.org

        # Assert
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, mock_response)

    @patch('client.get_json')
    def test_public_repos_url(self, mock_org):
        """
        Test the _public_repos_url property to ensure it
        returns the correct URL based on the org method.
        """
        # Arrange
        org_name = "google"
        expected_repos_url = "https://api.github.com/orgs/google/repos"
        client = GithubOrgClient(org_name)

        # Mock the return value of the org property
        mock_org.return_value = {"repos_url": expected_repos_url}

        # Act
        repos_url = client._public_repos_url

        # Assert
        self.assertEqual(repos_url, expected_repos_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test the public_repos method of GithubOrgClient to
        ensure it returns the correct list of repos.
        """
        # Mocked data
        mock_payload = [
            {"name": "repo1", "license": {"key": "MIT"}},
            {"name": "repo2", "license": {"key": "Apache"}},
            {"name": "repo3", "license": {"key": "MIT"}}
        ]
        mock_get_json.return_value = mock_payload

        # Mock the _public_repos_url property
        with patch.object(
            GithubOrgClient, '_public_repos_url',
            new='https://api.github.com/orgs/google/repos'
        ):
            client = GithubOrgClient("google")

            # Act
            result = client.public_repos(license="MIT")

            # Assert
            expected_repos = ["repo1", "repo3"]
            self.assertEqual(result, expected_repos)

            # Check that get_json was called once with the expected URL
            mock_get_json.assert_called_once_with(
                'https://api.github.com/orgs/google/repos'
            )


if __name__ == "__main__":
    unittest.main()
