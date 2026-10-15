import unicodedata
import reflex as rx

# ============================================================
# TEXTO
# ============================================================
def normalize_text(value: str,) -> str:
    """Normaliza texto para pesquisas sem acentos."""
    normalized = unicodedata.normalize("NFKD", value.casefold().strip(),)
    return "".join(character for character in normalized if not unicodedata.combining(character))


# ============================================================
# STATE
# ============================================================
class SidebarState(rx.State):
    """Controla a navegação lateral administrativa."""
    expanded: bool = True
    site_open: bool = True
    filter_text: str = ""

    # ========================================================
    # ROTA ATUAL
    # ========================================================
    @rx.var
    def active_path(self,) -> str:
        """Retorna o caminho atual sem barra final."""
        return (self.router.url.path.rstrip("/") or "/")

    # ========================================================
    # ROTAS ATIVAS
    # ========================================================
    @rx.var
    def overview_active(self,) -> bool:
        """Indica se estamos no painel geral."""
        return ( self.active_path == "/admin")

    @rx.var
    def metas_active(self,) -> bool:
        """Indica se estamos em alguma página de metas."""
        return (self.active_path == "/admin/metas" or self.active_path.startswith("/admin/metas/"))

    @rx.var
    def users_active(self,) -> bool:
        """Indica se estamos na administração de usuários."""
        return (self.active_path == "/admin/usuarios" or self.active_path.startswith("/admin/usuarios/"))

    # ========================================================
    # PESQUISA DO MENU
    # ========================================================
    @rx.var
    def visible_items(self,) -> dict[str, bool]:
        """
        Define quais itens aparecem durante
        a pesquisa da Sidebar.

        A permissão do usuário é tratada
        separadamente no componente.
        """
        query = normalize_text(self.filter_text)

        main_items = {
            "overview": "Visão Geral",
            "metas": "Metas",
            "images": "Banco de imagens",
            "users": "Usuários",
        }

        site_items = {
            "site_home": "Página inicial",
            "site_news": "Notícias",
            "site_about": "Sobre o PdM",
            "site_history": "Histórico",
            "site_participation": (
                "Participação Social"
            ),
            "site_metas": "Metas",
            "site_regionalization": (
                "Regionalização"
            ),
            "site_transparency": (
                "Transparência e Monitoramento"
            ),
        }
        visible = {key: (not query or query in normalize_text(label)) for key, label in main_items.items()}

        # ----------------------------------------------------
        # SITE
        # ----------------------------------------------------
        site_matches = (not query or query in normalize_text("Site"))
        for (key, label,) in site_items.items():
            visible[key] = (site_matches or query in normalize_text(label))

        visible["site"] = (site_matches or any(visible[key] for key in site_items ))
        return visible

    # ========================================================
    # RESULTADO DA PESQUISA
    # ========================================================
    @rx.var
    def has_visible_items(self,) -> bool:
        """Indica se a pesquisa encontrou algo."""
        return any(self.visible_items.values())

    # ========================================================
    # SUBMENU SITE
    # ========================================================
    @rx.var
    def show_site_children(self,) -> bool:
        """Exibe os itens internos do módulo Site."""
        return (self.expanded and (self.site_open or bool(self.filter_text.strip())))

    # ========================================================
    # EVENTOS
    # ========================================================
    @rx.event
    def toggle_sidebar(self,):
        """Expande ou recolhe a Sidebar."""
        self.expanded = (not self.expanded)
        if not self.expanded:
            # Evita manter um filtro invisível
            # enquanto a Sidebar estiver fechada.
            self.filter_text = ""

    # --------------------------------------------------------
    @rx.event
    def toggle_site(self,):
        """Expande ou recolhe o módulo Site."""
        if not self.expanded:
            self.expanded = True
            self.site_open = True
            return

        self.site_open = (not self.site_open)

    # --------------------------------------------------------
    @rx.event
    def update_filter(self,value: str,):
        """Atualiza a pesquisa da Sidebar."""
        self.filter_text = value