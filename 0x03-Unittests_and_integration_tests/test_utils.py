#!/usr/bin/env python3
"""
Unit tests for utils.py
"""
import unittest
from parameterized import parameterized
from unittest.mock import Mock, patch
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Unit tests for access_nested_map function
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map with valid inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError for invalid inputs."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(cm.exception.args[0], path[-1])


class TestGetJson(unittest.TestCase):
    """
    Unit tests for get_json function
    """

    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        """Test get_json returns correct JSON response."""
        mock_response = Mock()
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response

        url = "http://example.com"
        result = get_json(url)
        self.assertEqual(result, {"key": "value"})
        mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """
    Unit tests for memoize decorator
    """
    def test_memoize(self):
        """
        Test memoize decorator to ensure method is called only once
        """

        class TestClass:
            def a_method(self):
                """
                Method that will be mocked
                """
                return 42

            @memoize
            def a_property(self):
                """
                Property that is memoized
                """
                return self.a_method()

        obj = TestClass()

        # Patch the a_method to control its calls and results
        with patch.object(
            TestClass, 'a_method', return_value=42
        ) as mock_method:
            # Call the memoized property twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Assert the results are as expected
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert a_method was called only once
            mock_method.assert_called_once()


class TestIntegration(unittest.TestCase):
    """
    Integration tests for utils functions
    """

    @patch('utils.requests.get')
    def test_get_json_and_access_nested_map(self, mock_get):
        """Test get_json and access_nested_map integration."""
        mock_response = Mock()
        mock_response.json.return_value = {"a": {"b": {"c": 1}}}
        mock_get.return_value = mock_response

        url = "http://example.com"
        result = get_json(url)
        value = access_nested_map(result, ["a", "b", "c"])
        self.assertEqual(value, 1)


if __name__ == "__main__":
    unittest.main()
