"""Middleware для создания и передачи пользовательской сессии."""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.sessions import create_session, session_exists


class SessionMiddleware(BaseHTTPMiddleware):
    """Обеспечивает наличие пользовательской сессии для HTTP-запросов.

    Извлекает идентификатор сессии из cookie ``session_id``.
    Если cookie отсутствует или сессия не существует, создаёт новую.

    Идентификатор сессии сохраняется в ``request.state.session_id``
    для использования обработчиками запроса. Для новой сессии
    идентификатор также устанавливается в cookie ответа.
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        session_id = request.cookies.get("session_id")
        is_new_session = False

        if session_id is None or not await session_exists(session_id):
            session_id = await create_session()
            is_new_session = True

        request.state.session_id = session_id
        response = await call_next(request)
        if is_new_session:
            response.set_cookie("session_id", session_id)
        return response
