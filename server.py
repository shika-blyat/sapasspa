from http_parser import HttpParser, build_http_answer
from socketserver import BaseRequestHandler, ThreadingMixIn, TCPServer
from threading import Thread
import socketserver

HELP = """
help: display this help
exit | quit: shutdown the server
            """


def path(path):
    def inner_decorator(fn):
        def wrapper(self):
            self.paths = {path: fn}
            return fn

        wrapper.__dict__[path] = fn
        return wrapper

    return inner_decorator


class Handler(BaseRequestHandler):
    def handle(self):
        raw_request = self.request.recv(1024)
        request = HttpParser(raw_request).build_request()
        page = self.get_page(request.path)
        self.request.sendall(page)

    def get_page(self, path):
        methods = [
            getattr(self, method_name)
            for method_name in dir(self)
            if callable(getattr(self, method_name)) and not method_name.startswith("__")
        ]
        err_page = None
        for i in methods:
            try:
                return build_http_answer("200 OK", i.__dict__[path](self))
            except KeyError:
                try:
                    err_page = i.__dict__["404"](self)
                except KeyError:
                    pass
                pass
        if err_page:
            return build_http_answer("404 Not Found", err_page)
        with open("static/404.html") as err_page:
            return build_http_answer("404 Not Found", err_page.read())


class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    pass


def serve(handler, url="localhost", port=8888):
    server = ThreadedTCPServer((url, port), handler)
    server_thread = Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    while True:
        print(">>> ", end="")
        command = input()
        if command in ("quit", "exit"):
            break
        elif command in ("help"):
            print(HELP)
        elif command.strip() != "":
            print(f"Unknown command `{command}`")
    server.shutdown()
