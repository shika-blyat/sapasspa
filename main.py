from server import Handler, path, serve


class MyHandler(Handler):
    @path("/abc")
    def hello(self):
        with open("static/hello.html") as hello:
            return hello.read()

    @path("/")
    def foo(self):
        return "Try to change the url to `localhost:8888/abc`"

    @path("404")
    def bar(self):
        with open("static/404.html") as hello:
            return hello.read()


def main():
    serve(MyHandler)


main()
