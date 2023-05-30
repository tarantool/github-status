import http
import json

import requests_mock

from settings import Config
from watcher.githubclient import GithubClient, BadRequestException


class TestClient:

    def test_get_status(self):
        with requests_mock.Mocker() as mock:
            config = Config()

            expected = json.loads(
                '{"page":{"id":"kctbh9vrtdwd","name":"GitHub","url":"https://www.githubstatus.xscom","time_zone"'
                ':"Etc/UTC","updated_at":"2023-05-29T07:49:52.960Z"},"status":{"indicator":"none","description'
                '":"All Systems Operational"}}')

            mock.get(
                url=f"{config.github_api_url}/status.json",
                json=expected
            )

            response = GithubClient(api_url=config.github_api_url).get_status()
            data = response.json()
            assert data["status"]["indicator"].lower() == "none"
            assert data["page"]["name"].lower() == "github"

    def test_get_status_incorrect_status_code(self):
        with requests_mock.Mocker() as mock:
            config = Config()

            mock.get(
                url=f"{config.github_api_url}/status.json",
                json=json.loads('{}'),
                status_code=http.HTTPStatus.BAD_REQUEST
            )
            try:
                GithubClient(api_url=config.github_api_url).get_status(retry_=False)
            except BadRequestException:
                return

    def test_get_unresolved_incidents(self):
        with requests_mock.Mocker() as mock:
            config = Config()

            expected = json.loads(
                '{"page":{"id":"kctbh9vrtdwd","name":"GitHub","url":"https://www.githubstatus.com",'
                '"time_zone":"Etc/UTC","updated_at":"2023-05-30T08:03:09.076Z"},"incidents":[]}')

            mock.get(
                url=f"{config.github_api_url}/incidents/unresolved.json",
                json=expected
            )

            response = GithubClient(api_url=config.github_api_url).get_unresolved_incidents()
            data = response.json()
            assert data["incidents"] == []
            assert data["page"]["name"].lower() == "github"

    def test_get_unresolved_incidents_incorrect_status(self):
        with requests_mock.Mocker() as mock:
            config = Config()

            mock.get(
                url=f"{config.github_api_url}/incidents/unresolved.json",
                json=json.loads('{}'),
                status_code=http.HTTPStatus.BAD_REQUEST
            )
            try:
                GithubClient(api_url=config.github_api_url).get_unresolved_incidents(retry_=False)
            except BadRequestException:
                return
