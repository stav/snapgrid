from starlette.requests import Request

from .index import index_route
from .fetch import fetch_route


def router(rt):

    @rt("/")
    def _():
        return index_route()

    @rt("/fetch")
    async def _(request: Request):
        return await fetch_route(request)
