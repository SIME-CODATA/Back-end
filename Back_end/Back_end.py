import reflex as rx

from Back_end.access.modules.auth.model import UserSession
from Back_end.access.modules.users.model import User
from Back_end.metas.models.meta import Meta
from Back_end.access.pages.admin import admin_page
from Back_end.access.pages.login import login_page
from Back_end.access.pages.logout import logout_page
from Back_end.access.states.auth_state import AuthState
from Back_end.api import api


app = rx.App(
    api_transformer=api,
)

app.add_page(
    login_page,
    route="/",
    title="Programa de Metas",
)

app.add_page(
    login_page,
    route="/login",
    title="Login | Programa de Metas",
)

app.add_page(
    admin_page,
    route="/admin",
    title="Admin | Programa de Metas",
    on_load=AuthState.require_auth,
)

app.add_page(
    logout_page,
    route="/logout",
    title="Saindo | Programa de Metas",
    on_load=AuthState.logout,
)