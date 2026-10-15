import reflex as rx

from Back_end.access.modules.auth.model import (UserSession,)
from Back_end.access.modules.users.model import (User,)
from Back_end.access_api.metas.models.meta import (Meta,)
from Back_end.access_api.metas.models.meta_orcamento import (MetaOrcamento,)
from Back_end.access_api.metas.models.tag import (Tag,)
from Back_end.access_api.metas.models.meta_tag import (MetaTag,)
from Back_end.access_api.metas.models.meta_equipe import (MetaEquipe,)
from Back_end.access_api.metas.models.iniciativa import (Iniciativa,)
from Back_end.access.pages.admin import (admin_page,)
from Back_end.access.pages.logout import (logout_page,)
from Back_end.access.states.auth_state import (AuthState,)
from Back_end.interface.pages.login import (login_page,)
from Back_end.interface.pages.forbidden import (forbidden_page,)
from Back_end.interface.pages.users.users_page import (users_page,)
from Back_end.interface.pages.meta.meta_detail import (meta_detail_page,)
from Back_end.interface.pages.meta.meta_list import (meta_list_page,)
from Back_end.interface.pages.meta.meta_print import (meta_print_page,)
from Back_end.interface.state.meta.meta_list_state import (MetaListState,)
from Back_end.interface.state.meta.meta_detail_state import (MetaDetailState,)
from Back_end.interface.state.meta.meta_print_state import (MetaPrintState,)
from Back_end.interface.pages.users.profile import (profile_page,)
from Back_end.interface.state.users.user_management_state import (UserManagementState,)
from Back_end.api import (api,)


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
    on_load=(
        AuthState.require_dashboard_access
    ),
)

# ============================================================
# METAS
# ============================================================

app.add_page(
    meta_list_page,
    route="/admin/metas",
    title="Metas | Programa de Metas",
    on_load=[AuthState.require_metas_access,MetaListState.load_metas,],
)


app.add_page(
    meta_detail_page,
    route="/admin/metas/[codigo]",
    title="Ficha da Meta | Programa de Metas",
    on_load=[AuthState.require_metas_access,MetaDetailState.load_meta,],
)

app.add_page(
    meta_print_page,
    route="/imprimir/metas/[codigo]",
    title="Ficha da Meta",
    on_load=[AuthState.require_metas_access,MetaPrintState.load_meta,],
)

# ============================================================
# USUÁRIOS
# ============================================================

app.add_page(
    users_page,
    route="/admin/usuarios",
    title="Usuários | Programa de Metas",
    on_load=[AuthState.require_users_access,UserManagementState.load_users,],
)

# ============================================================
# PERFIL
# ============================================================

app.add_page(
    profile_page,

    route="/admin/perfil",

    title="Perfil | Programa de Metas",

    on_load=AuthState.require_auth,
)

# ============================================================
# ACESSO NEGADO
# ============================================================

app.add_page(
    forbidden_page,
    route="/403",
    title="Acesso não autorizado | Programa de Metas",
    on_load=(AuthState.require_auth),
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