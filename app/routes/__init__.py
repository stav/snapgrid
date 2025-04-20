from starlette.requests import Request

from .index import index_route
from .findsnap import findsnap_route


def router(rt):

    # The index route displays the form that submits to the findsnap route
    @rt("/")
    def _():
        return index_route()

    # The findsnap route receives the form data and returns the screenshot
    @rt("/findsnap")
    async def _(request: Request):
        return await findsnap_route(request)
