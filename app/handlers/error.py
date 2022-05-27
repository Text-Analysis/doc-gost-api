from typing import Callable

from fastapi import Request, Response, HTTPException
from fastapi.routing import APIRoute

from app.errors.errors import UnprocessableDataException, ResourceNotFoundException


class RouteErrorHandle(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except ResourceNotFoundException as ex:
                raise HTTPException(status_code=404, detail=str(ex))
            except UnprocessableDataException as ex:
                raise HTTPException(status_code=422, detail=str(ex))
            except Exception as ex:
                raise HTTPException(status_code=500, detail=str(ex))

        return custom_route_handler
