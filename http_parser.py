from abc import ABC
from itertools import zip_longest
from pprint import pformat
from datetime import datetime


class HttpRequest(ABC):
    pass


class GetRequest(HttpRequest):
    def __init__(self, headers, path, http_ver):
        self.headers = headers
        self.path = path
        self.http_ver = http_ver

    def __str__(self):
        return "GET request:\npath: {}\nheaders:\n{}".format(
            self.path, pformat(self.headers)
        )


class HttpParser:
    def __init__(self, request):
        self.request = request

    def build_request(self):
        """
        Create a request object (for example a GetRequest object) from the request
        given when the HttpParser was initialized
        """
        request_lines = self.request.decode().strip().split("\n")
        [request_type, path, http_ver] = request_lines[0].split()
        headers = HttpParser.build_header_from_list(request_lines[1:])
        if request_type == "GET":
            return GetRequest(headers, path, http_ver)

    @classmethod
    def build_header_from_list(cls, header_l):
        """
        Convert a list of string representing header into a dictionnaries
        """
        header_dict = dict([tuple(map(str.strip, i.split(":", 1))) for i in header_l])
        return header_dict


def build_http_answer(code, val):
    return bytes(
        """HTTP/1.1 {}
Date: {}
Content-Length: {}
Content-Type: text/html; utf-8

{}""".format(
            code, datetime.now(), len(val), val
        ),
        encoding="utf-8",
    )
