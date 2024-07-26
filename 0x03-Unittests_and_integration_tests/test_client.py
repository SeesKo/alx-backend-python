#!/usr/bin/env python3
"""
Unit tests for client.py
"""
import unittest
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
from unittest.mock import Mock, patch


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestGithubOrgClient(unittest.TestCase):
    """
    Tests for GithubOrgClient class.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up the patcher for requests.get and configure the mock.
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Mock responses for the different URLs
        cls.mock_get.side_effect = lambda url: Mock(
            **{'json.return_value': cls._get_mock_response(url)}
        )

    @classmethod
    def _get_mock_response(cls, url):
        """
        Return the mock response based on the URL.
        """
        if 'orgs' in url and 'repos' not in url:
            return cls.org_payload
        elif 'repos' in url:
            return cls.repos_payload
        else:
            return {}

    @classmethod
    def tearDownClass(cls):
        """
        Stop the patcher.
        """
        cls.get_patcher.stop()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Unit test for GithubOrgClient.public_repos method"""
        # Define the payload to be returned by get_json
        mock_payload = [
            {"name": "repo1", "license": {"key": "MIT"}},
            {"name": "repo2", "license": {"key": "Apache-2.0"}},
            {"name": "repo3", "license": {"key": "MIT"}}
        ]
        mock_get_json.return_value = mock_payload

        # Define the expected URL
        expected_url = 'https://api.github.com/orgs/google/repos'

        with patch.object(
            GithubOrgClient, '_public_repos_url',
            new=expected_url
        ):
            client = GithubOrgClient("google")

            # Act
            result = client.public_repos("Apache-2.0")

            # Define the expected result
            expected_repos = ["repo2"]

            # Assert the result matches the expected repos
            self.assertEqual(result, expected_repos)

            # Assert that get_json was called once with the expected URL
            mock_get_json.assert_called_once_with(expected_url)

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
    def test_public_repos_url(self, mock_get_json):
        """
        Test the _public_repos_url property to ensure it
        returns the correct URL based on the org method.
        """
        # Arrange
        org_name = "google"
        expected_repos_url = "https://api.github.com/orgs/google/repos"
        client = GithubOrgClient(org_name)

        # Mock the return value of the org property
        mock_get_json.return_value = {"repos_url": expected_repos_url}

        # Act
        repos_url = client._public_repos_url

        # Assert
        self.assertEqual(repos_url, expected_repos_url)

    @patch('client.get_json')
    def test_public_repos_with_license(self, mock_get_json):
        """Integration test: public repos filtered by license"""
        # Mocked data for repos
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
            result = client.public_repos(license="Apache")

            # Assert
            expected_repos = ["repo2"]
            self.assertEqual(result, expected_repos)

            # Check that get_json was called once with the expected URL
            mock_get_json.assert_called_once_with(
                'https://api.github.com/orgs/google/repos'
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
        ({"license": {}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test the has_license static method of GithubOrgClient.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
