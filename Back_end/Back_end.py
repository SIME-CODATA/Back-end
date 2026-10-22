import reflex as rx

from Back_end.access.modules.auth.model import UserSession
from Back_end.access.modules.users.model import User
from Back_end.access.modules.audit.model import AuditLog

from Back_end.access_api.metas.models.meta import Meta
from Back_end.access_api.metas.models.meta_orcamento import MetaOrcamento
from Back_end.access_api.metas.models.tag import Tag
from Back_end.access_api.metas.models.meta_tag import MetaTag
from Back_end.access_api.metas.models.meta_equipe import MetaEquipe
from Back_end.access_api.metas.models.iniciativa import Iniciativa

from Back_end.access.pages.admin import admin_page
from Back_end.access.pages.logout import logout_page
from Back_end.access.states.auth_state import AuthState

from Back_end.interface.pages.login import login_page
from Back_end.interface.pages.forbidden import forbidden_page
from Back_end.interface.pages.users.users_page import users_page
from Back_end.interface.pages.users.profile import profile_page

from Back_end.interface.pages.meta.meta_detail import meta_detail_page
from Back_end.interface.pages.meta.meta_list import meta_list_page
from Back_end.interface.pages.meta.meta_print import meta_print_page

from Back_end.interface.state.meta.meta_list_state import MetaListState
from Back_end.interface.state.meta.meta_detail_state import MetaDetailState
from Back_end.interface.state.meta.meta_print_state import MetaPrintState
from Back_end.interface.state.users.user_management_state import UserManagementState
from Back_end.interface.state.users.profile_state import ProfileState

import Back_end.site_cms  # noqa: F401

from Back_end.site_cms.pages.site_page import site_cms_page

from Back_end.site_cms.modules.home.page import site_cms_home_page
from Back_end.site_cms.modules.home.state import HomeCmsState
from Back_end.site_cms.modules.home.editors import (
    mayor_letter_page,
    news_cms_page,
    axes_cms_page,
)

from Back_end.site_cms.modules.about.page import about_cms_page
from Back_end.site_cms.modules.history.page import history_cms_page
from Back_end.site_cms.modules.regionalization.page import regionalization_cms_page
from Back_end.site_cms.modules.transparency.page import transparency_cms_page

from Back_end.site_cms.modules.metas.list_page import metas_cms_page
from Back_end.site_cms.modules.metas.detail_page import meta_cms_detail_page
from Back_end.site_cms.modules.metas.state import MetaCmsState
from Back_end.site_cms.modules.metas.overview_page import meta_overview_cms_page
from Back_end.site_cms.modules.metas.overview_state import MetaOverviewCmsState

from Back_end.site_cms.state.section_editor_state import SectionEditorState

from Back_end.api import api


# ============================================================
# APP
# ============================================================

app = rx.App(
    api_transformer=api,
)


# ============================================================
# LOGIN
# ============================================================

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


# ============================================================
# PAINEL
# ============================================================

app.add_page(
    admin_page,
    route="/admin",
    title="Admin | Programa de Metas",
    on_load=AuthState.require_dashboard_access,
)


# ============================================================
# SITE / CMS
# ============================================================

app.add_page(
    site_cms_page,
    route="/admin/site",
    title="Site | Programa de Metas",
    on_load=AuthState.require_site_access,
)

# Página Inicial
app.add_page(
    site_cms_home_page,
    route="/admin/site/home",
    title="Página Inicial | Programa de Metas",
    on_load=HomeCmsState.load_page,
)

app.add_page(
    mayor_letter_page,
    route="/admin/site/home/carta-prefeito",
    title="Carta do prefeito | Programa de Metas",
    on_load=SectionEditorState.load_mayor_letter,
)

app.add_page(
    news_cms_page,
    route="/admin/site/home/noticias",
    title="Notícias | Programa de Metas",
    on_load=SectionEditorState.load_news,
)

app.add_page(
    axes_cms_page,
    route="/admin/site/home/eixos",
    title="Eixos | Programa de Metas",
    on_load=SectionEditorState.load_axes,
)

# Sobre
app.add_page(
    about_cms_page,
    route="/admin/site/sobre",
    title="Sobre o PdM | Programa de Metas",
    on_load=SectionEditorState.load_about_page,
)

# Histórico
app.add_page(
    history_cms_page,
    route="/admin/site/historico",
    title="Histórico | Programa de Metas",
    on_load=SectionEditorState.load_history,
)

# Regionalização
app.add_page(
    regionalization_cms_page,
    route="/admin/site/regionalizacao",
    title="Regionalização | Programa de Metas",
    on_load=SectionEditorState.load_regionalization,
)

# Transparência e Monitoramento
app.add_page(
    transparency_cms_page,
    route="/admin/site/transparencia",
    title="Transparência e Monitoramento | Programa de Metas",
    on_load=SectionEditorState.load_transparency,
)

# Metas do Site
app.add_page(
    metas_cms_page,
    route="/admin/site/metas",
    title="Metas do Site | Programa de Metas",
    on_load=MetaCmsState.load_metas,
)

app.add_page(
    meta_overview_cms_page,
    route="/admin/site/metas/visao-geral",
    title="Visão Geral das Metas | Programa de Metas",
    on_load=MetaOverviewCmsState.load_page,
)

app.add_page(
    meta_cms_detail_page,
    route="/admin/site/metas/[codigo]",
    title="Editar Meta do Site | Programa de Metas",
    on_load=MetaCmsState.load_meta,
)


# ============================================================
# METAS
# ============================================================

app.add_page(
    meta_list_page,
    route="/admin/metas",
    title="Metas | Programa de Metas",
    on_load=[
        AuthState.require_metas_access,
        MetaListState.load_metas,
    ],
)

app.add_page(
    meta_detail_page,
    route="/admin/metas/[codigo]",
    title="Ficha da Meta | Programa de Metas",
    on_load=[
        AuthState.require_metas_access,
        MetaDetailState.load_meta,
    ],
)

app.add_page(
    meta_print_page,
    route="/imprimir/metas/[codigo]",
    title="Ficha da Meta",
    on_load=[
        AuthState.require_metas_access,
        MetaPrintState.load_meta,
    ],
)


# ============================================================
# USUÁRIOS
# ============================================================

app.add_page(
    users_page,
    route="/admin/usuarios",
    title="Usuários | Programa de Metas",
    on_load=[
        AuthState.require_users_access,
        UserManagementState.load_users,
    ],
)


# ============================================================
# PERFIL
# ============================================================

app.add_page(
    profile_page,
    route="/admin/perfil",
    title="Perfil | Programa de Metas",
    on_load=ProfileState.load_profile,
)


# ============================================================
# ACESSO NEGADO
# ============================================================

app.add_page(
    forbidden_page,
    route="/403",
    title="Acesso não autorizado | Programa de Metas",
    on_load=AuthState.require_auth,
)


# ============================================================
# LOGOUT
# ============================================================

app.add_page(
    logout_page,
    route="/logout",
    title="Saindo | Programa de Metas",
    on_load=AuthState.logout,
)
