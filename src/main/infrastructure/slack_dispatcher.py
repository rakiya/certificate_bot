import requests


class SlackDispatcher:
    def __init__(self, slack_url: str) -> None:
        self.__slack_url = slack_url

    def send_good(self, title: str, message: str):
        body = {
            "attachments": [
                {"mrkdwn_in": ["title", "text"], "color": "good", "title": title, "text": message}
            ]
        }
        requests.post(self.__slack_url, json=body)

    def send_danger(self, title: str, message: str):
        body = {
            "attachments": [
                {"mrkdwn_in": ["title", "text"], "color": "danger", "title": title, "text": message}
            ]
        }
        requests.post(self.__slack_url, json=body)
