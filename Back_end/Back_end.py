import reflex as rx

from Back_end.access.modules.auth.model import UserSession
from Back_end.access.modules.users.model import User
from Back_end.access_api.metas.models.meta import Meta
from Back_end.access_api.metas.models.meta_orcamento import MetaOrcamento
from Back_end.access_api.metas.models.tag import Tag
from Back_end.access_api.metas.models.meta_tag import MetaTag
from Back_end.access_api.metas.models.meta_equipe import MetaEquipe
from Back_end.access_api.metas.models.iniciativa import Iniciativa
from Back_end.access.pages.admin import admin_page
from Back_end.interface.pages.login import login_page
from Back_end.interface.pages.meta.meta_detail import meta_detail_page
from Back_end.interface.pages.meta.meta_list import meta_list_page
from Back_end.interface.state.meta.meta_list_state import MetaListState
from Back_end.interface.state.meta.meta_detail_state import MetaDetailState
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
    meta_list_page,
    route="/admin/metas",
    title="Metas | Programa de Metas",
    on_load=[
        AuthState.require_auth,
        MetaListState.load_metas,
    ],
)

app.add_page(
    meta_detail_page,
    route="/admin/metas/[codigo]",
    title="Ficha da Meta | Programa de Metas",
    on_load=[
        AuthState.require_auth,
        MetaDetailState.load_meta,
    ],
)

app.add_page(
    logout_page,
    route="/logout",
    title="Saindo | Programa de Metas",
    on_load=AuthState.logout,
)