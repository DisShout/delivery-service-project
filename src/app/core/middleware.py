import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        session_id = request.cookies.get("session_id")

        if not session_id:
            session_id = str(uuid.uuid4())
            response: Response = await call_next(request)
            response.set_cookie(key="session_id", value=session_id)
            request.state.session_id = session_id
            return response

        request.state.session_id = session_id
        response: Response = await call_next(request)
        return response
