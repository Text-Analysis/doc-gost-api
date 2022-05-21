from typing import Callable

from fastapi import Request, Response, HTTPException
from fastapi.routing import APIRoute

from app.errors import ValidException, FoundException


class RouteErrorHandle(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except FoundException as ex:
                raise HTTPException(status_code=404, detail=str(ex))
            except ValidException as ex:
                raise HTTPException(status_code=422, detail=str(ex))
            except Exception as ex:
                raise HTTPException(status_code=500, detail=str(ex))

        return custom_route_handler
