import json
from enum import Enum
from typing import Optional

from flask import Request

"""
Standardizing class for webhook data from GitLab or GitHub
"""


class RequestData:
    class Sender(Enum):
        GITLAB = 1
        GITHUB = 2
        NOT_IDENTIFIED = 0


    sender: Sender = Sender.NOT_IDENTIFIED
    event: str | None = None
    repository: str | None = None
    ref: str | None = None

    def loadData(self, request: Request) -> Optional['RequestData']:
        for key, value in request.headers:
            if "x-gitlab-event" in key.lower():
                self.sender = self.Sender.GITLAB
                self.event = value.lower().strip(" hook")
                break
            if "x-github-event" in key.lower():
                self.sender = self.Sender.GITHUB
                self.event = value.lower()
                break

        if self.sender is self.Sender.NOT_IDENTIFIED:
            return None

        data = request.json

        self.ref = data.get('ref', None)

        if self.sender is self.Sender.GITHUB:
            self.repository = data['repository']['full_name']
        elif self.sender is self.Sender.GITLAB:
            self.repository = data['project']['path_with_namespace']

        return self