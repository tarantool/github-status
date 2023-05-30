import http
import json

import requests_mock

from settings import Config
from watcher.vkteams_bot import VKTeamsBot, BadRequestException


class TestVKTeamsBot:

    def test_valid_request(self):
        with requests_mock.Mocker() as mock:
            config = Config()
            mock.get(
                url=f"{config.bot_api_url}/messages/sendText",
                json=json.loads('{"msgId": "12345678", "ok": true}')
            )

            bot = VKTeamsBot(token="test_token", api_url=config.bot_api_url, chat_id="test_chat")
            response = bot.send_message(message="test_message")
            assert response.status_code == http.HTTPStatus.OK
            assert response.json()["ok"] is True
            assert response.json()["msgId"] == "12345678"

    def test_incorrect_status_code(self):
        with requests_mock.Mocker() as mock:
            config = Config()
            mock.get(
                url=f"{config.bot_api_url}/messages/sendText",
                json=json.loads('{}'),
                status_code=http.HTTPStatus.BAD_REQUEST
            )
            try:
                bot = VKTeamsBot(token="test_token", api_url=config.bot_api_url, chat_id="test_chat")
                bot.send_message(message="test_message", retry_=False)
            except BadRequestException:
                return

    def test_invalid_token(self):
        with requests_mock.Mocker() as mock:
            config = Config()
            mock.get(
                url=f"{config.bot_api_url}/messages/sendText",
                json=json.loads('{"description": "Invalid token", "ok": false}')
            )

            bot = VKTeamsBot(token="test_token", api_url=config.bot_api_url, chat_id="test_chat")
            response = bot.send_message(message="test_message", retry_=False)
            assert response.json()["ok"] is False
            assert response.json()["description"].lower() == "invalid token"
