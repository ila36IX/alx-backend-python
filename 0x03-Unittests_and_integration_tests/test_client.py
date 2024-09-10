#!/usr/bin/env python3
"""
Test suite for the GithubOrgClient class.

This module contains unit tests and integration tests for the GithubOrgClient
class, which interacts with the GitHub API to retrieve information about
organizations and their repositories.
"""

import unittest
from typing import Dict
from unittest.mock import (
    MagicMock,
    Mock,
    PropertyMock,
    patch,
)
from parameterized import parameterized, parameterized_class
from requests import HTTPError

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class.

    This test suite covers various methods of the GithubOrgClient class,
    including org(), _public_repos_url, public_repos(), and has_license().
    """

    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org: str, expected_response: Dict,
                 mocked_function: MagicMock) -> None:
        """
        Test the org method of GithubOrgClient.

        This test ensures that the org method correctly calls the GitHub API
        and returns the expected organization data.

        Args:
            org (str): The name of the organization to test.
            expected_response (Dict): The expected response from the API.
            mocked_function (MagicMock): A mock object for the get_json function.
        """
        mocked_function.return_value = MagicMock(return_value=expected_response)
        goclient = GithubOrgClient(org)
        self.assertEqual(goclient.org(), expected_response)
        mocked_function.assert_called_once_with(
            f"https://api.github.com/orgs/{org}"
        )

    def test_public_repos_url(self) -> None:
        """
        Test the _public_repos_url property of GithubOrgClient.

        This test verifies that the _public_repos_url property correctly
        extracts the repos_url from the organization data.
        """
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
        ) as mock_org:
            mock_org.return_value = {
                'repos_url': "https://api.github.com/users/google/repos",
            }
            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                "https://api.github.com/users/google/repos",
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """
        Test the public_repos method of GithubOrgClient.

        This test ensures that the public_repos method correctly retrieves
        and processes the list of public repositories for an organization.

        Args:
            mock_get_json (MagicMock): A mock object for the get_json function.
        """
        test_payload = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-19T00:31:37Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "has_issues": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    "id": 8566972,
                    "name": "kratu",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/kratu",
                    "created_at": "2013-03-04T22:52:33Z",
                    "updated_at": "2019-11-15T22:22:16Z",
                    "has_issues": True,
                    "forks": 32,
                    "default_branch": "master",
                },
            ]
        }
        mock_get_json.return_value = test_payload["repos"]
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload["repos_url"]
            self.assertEqual(
                GithubOrgClient("google").public_repos(),
                [
                    "episodes.dart",
                    "kratu",
                ],
            )
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({'license': {'key': "bsd-3-clause"}}, "bsd-3-clause", True),
        ({'license': {'key': "bsl-1.0"}}, "bsd-3-clause", False),
    ])
    def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
        """
        Test the has_license method of GithubOrgClient.

        This test verifies that the has_license method correctly determines
        whether a repository has a specific license.

        Args:
            repo (Dict): A dictionary representing a repository.
            key (str): The license key to check for.
            expected (bool): The expected result of the has_license check.
        """
        gh_org_client = GithubOrgClient("google")
        client_has_licence = gh_org_client.has_license(repo, key)
        self.assertEqual(client_has_licence, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for the GithubOrgClient class.

    This test suite performs integration tests on the GithubOrgClient class,
    simulating API responses and testing the class's behavior in a more
    realistic scenario.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the test environment for the integration tests.

        This method creates a mock for the requests.get function to simulate
        API responses without making actual network calls.
        """
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """
        Test the public_repos method in an integration scenario.

        This test verifies that the public_repos method returns the expected
        list of repositories when called on a GithubOrgClient instance.
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """
        Test the public_repos method with a license filter in an integration scenario.

        This test checks that the public_repos method correctly filters repositories
        by license when the license parameter is provided.
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Clean up the test environment after running the integration tests.

        This method stops the patcher used to mock the requests.get function.
        """
        cls.get_patcher.stop()
