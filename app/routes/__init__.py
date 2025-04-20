from starlette.requests import Request

from .index import index_route
from .fetch import fetch_route


def router(rt):

    # The index route displays the form that submits to the fetch route
    @rt("/")
    def _():
        return index_route()

    # The fetch route receives the form data and returns the screenshot
    @rt("/fetch")
    async def _(request: Request):
        return await fetch_route(request)
