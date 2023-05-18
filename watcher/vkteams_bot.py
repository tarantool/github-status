import http
import logging

import requests
import retry
from bot import bot as teamsbot

import settings


class BadRequestException(Exception):
    pass


class VKTeamsBot:

    def __init__(self, token: str, api_url: str, chat_id: str):
        self.bot = teamsbot.Bot(token=token, api_url_base=api_url)
        self.chat_id = chat_id

    @retry.retry(exceptions=BadRequestException, delay=settings.Config().retry_request_delay)
    def send_message(
            self,
            message: str,
            chat_id: str = None,
            parse_mode: str = "HTML",
            retry_: bool = True) -> requests.Response:
        if chat_id is None:
            chat_id = self.chat_id

        response = self.bot.send_text(chat_id=chat_id, text=message, parse_mode=parse_mode)
        logging.info(f"Sent request {response.url}")
        logging.debug(f"Response status code: {response.status_code} \njson: {response.json()}")
        if response.status_code != http.HTTPStatus.OK or response.json()["ok"] is False:
            logging.error(f"Incorrect status code for request: {response.url} \nResponse json: {response.json()}")
            if retry_:
                raise BadRequestException
        return response
