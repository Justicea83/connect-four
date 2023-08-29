"""
Mock WebsocketCommunicator to make the scope accept a user
"""

from channels.testing import WebsocketCommunicator
from urllib.parse import unquote, urlparse
from asgiref.testing import ApplicationCommunicator


class MockWebsocketCommunicator(WebsocketCommunicator):
    def __init__(self, application, path, user):
        if not isinstance(path, str):
            raise TypeError("Expected str, got {}".format(type(path)))
        parsed = urlparse(path)
        self.scope = {
            "type": "websocket",
            "path": unquote(parsed.path),
            "query_string": parsed.query.encode("utf-8"),
            "headers": [],
            "subprotocols": [],
            "user": user,
        }
        ApplicationCommunicator.__init__(self, application=application, scope=self.scope)
