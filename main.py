from fasthtml.common import fast_app, serve

app, rt = fast_app()
serve()


@rt
def index():
    return "Hello, World!"
