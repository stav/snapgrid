from starlette.requests import Request

from .index import index_route
from .snap import snap_route
from .markdown import markdown_route


def router(rt):

    # The index route displays the form that submits to the snap route
    @rt("/")
    def _():
        return index_route()

    # The snap route receives the form data and returns the screenshot
    @rt("/snap")
    async def _(request: Request):
        return await snap_route(request)
        
    # The markdown route serves markdown content for a given filename
    @rt("/markdown/{filename:path}/")
    async def _(request: Request):
        print(f"request: {request.method}")
        print(f"request.path_params: {request.path_params}")
        return await markdown_route(request)
