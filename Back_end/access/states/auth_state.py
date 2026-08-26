import reflex as rx

from Back_end.access.modules.auth.service import ( create_session, validate_session, revoke_session,)
from Back_end.access.modules.users.service import authenticate_user

SESSION_MAX_AGE = 8 * 60 * 60


class AuthState(rx.State):
    """Controla autenticação e sessão do usuário."""

    error_message: str = ""

    session_token: str = rx.Cookie(
        "",
        name="pdm_session",
        path="/",
        max_age=SESSION_MAX_AGE,
        same_site="strict",
        secure=False,
    )

    _authenticated_user_id: int | None = None

    @rx.event
    def login(self, form_data: dict[str, str]):
        """Autentica o usuário e cria uma sessão válida."""

        self.error_message = ""

        email = form_data.get("email", "")
        password = form_data.get("password", "")

        user = authenticate_user(
            email=email,
            password=password,
        )

        if user is None or user.id is None:
            self.error_message = "E-mail ou senha inválidos."
            return

        token = create_session(user.id)

        self.session_token = token
        self._authenticated_user_id = user.id

        return rx.redirect("/admin")

    @rx.event
    def require_auth(self):
        """Valida a sessão antes de permitir acesso a páginas protegidas."""

        user_id = validate_session(self.session_token)

        if user_id is None:
            self.session_token = ""
            self._authenticated_user_id = None

            return rx.redirect("/login")

        self._authenticated_user_id = user_id

    @rx.event
    def logout(self):
        """Encerra a sessão atual do usuário."""

        if self.session_token:
            revoke_session(self.session_token)

        self.session_token = ""
        self._authenticated_user_id = None

        yield rx.remove_cookie("pdm_session")
        yield rx.redirect("/login")