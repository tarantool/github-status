import http
import logging
from typing import Optional

import requests
import retry

import settings


class BadRequestException(Exception):
    pass


class GithubClient:

    def __init__(self, api_url: str):
        self.__api_url = api_url

    @retry.retry(exceptions=BadRequestException, delay=settings.Config().retry_request_delay)
    def _get_request(self, url: str, retry_: bool = True) -> Optional[requests.Response]:
        response = requests.get(url)
        logging.info(f"Sent request: {response.url}")
        logging.debug(f"Response status code: {response.status_code} \njson: {response.json()}")
        if response.status_code != http.HTTPStatus.OK:
            logging.error(f"Incorrect status code for request: {response.url} \nResponse json: {response.json()}")
            if retry_:
                raise BadRequestException
        return response

    def get_summary(self, retry_: bool = True) -> Optional[requests.Response]:
        url = f"{self.__api_url}/summary.json"
        return self._get_request(url, retry_)

    def get_status(self, retry_: bool = True) -> requests.Response:
        url = f"{self.__api_url}/status.json"
        return self._get_request(url, retry_)

    def get_unresolved_incidents(self, retry_: bool = True) -> requests.Response:
        url = f"{self.__api_url}/incidents/unresolved.json"
        return self._get_request(url, retry_)
