"""
ISULOG client
"""
from __future__ import annotations

import json
import time
import urllib.parse
import sys

import requests
import threading
from queue import Queue

class IsuLogger:
    def __init__(self, endpoint, appID):
        self.endpoint = endpoint
        self.appID = appID
        self.queue = Queue()
        self.logs = []
        self.thread = threading.Thread(target=self._send_bulk)
        self.thread.start()

    def send(self, tag, data):
        self.queue.put(
            {
                "tag": tag,
                "time": time.strftime("%Y-%m-%dT%H:%M:%S+09:00"),
                "data": data,
            }
        )

    def _send_bulk(self):
        while True:
            while not self.queue.empty():
                self.logs.append(self.queue.get())
            if self.logs:
                try:
                    self._request("/send_bulk", self.logs)
                except Exception as e:
                    print(f"Catch bulk error {e}", file=sys.stderr)
                else:
                    self.logs = []
            time.sleep(2)

    def _request(self, path, data):
        url = urllib.parse.urljoin(self.endpoint, path)
        body = json.dumps(data)
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.appID,
        }

        res = requests.post(url, data=body, headers=headers)
        res.raise_for_status()
