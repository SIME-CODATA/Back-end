import unicodedata

import reflex as rx


def normalize_text(value: str) -> str:
    """Normaliza o texto para permitir buscas sem acentos."""

    normalized = unicodedata.normalize(
        "NFKD",
        value.casefold().strip(),
    )

    return "".join(
        character
        for character in normalized
        if not unicodedata.combining(character)
    )


class SidebarState(rx.State):
    """Controla a navegação lateral do painel administrativo."""

    expanded: bool = True
    site_open: bool = True
    filter_text: str = ""

    @rx.var
    def active_path(self) -> str:
        """Retorna o caminho atual, sem a barra final."""

        return self.router.url.path.rstrip("/") or "/"

    @rx.var
    def overview_active(self) -> bool:
        return self.active_path == "/admin"

    @rx.var
    def metas_active(self) -> bool:
        return (
            self.active_path == "/metas"
            or self.active_path.startswith("/metas/")
        )

    @rx.var
    def visible_items(self) -> dict[str, bool]:
        """Define quais itens aparecem durante a pesquisa do menu."""

        query = normalize_text(self.filter_text)

        main_items = {
            "overview": "Visão Geral",
            "metas": "Metas",
            "images": "Banco de imagem",
            "users": "Usuários",
        }

        site_items = {
            "site_home": "Página inicial",
            "site_news": "Notícias",
            "site_about": "Sobre",
            "site_history": "Histórico",
            "site_participation": "Participação Social",
            "site_metas": "Metas",
            "site_regionalization": "Regionalização",
            "site_transparency": "Transparência e Monitoramento",
        }

        visible = {
            key: not query or query in normalize_text(label)
            for key, label in main_items.items()
        }

        # Ao pesquisar "Site", exibimos todo o submenu.
        site_matches = not query or query in normalize_text("Site")

        for key, label in site_items.items():
            visible[key] = (
                site_matches
                or query in normalize_text(label)
            )

        visible["site"] = (
            site_matches
            or any(visible[key] for key in site_items)
        )

        return visible

    @rx.var
    def has_visible_items(self) -> bool:
        """Indica se a pesquisa encontrou algum item."""

        return any(self.visible_items.values())

    @rx.var
    def show_site_children(self) -> bool:
        """Exibe os submenus ao expandir Site ou pesquisar neles."""

        return (
            self.expanded
            and (
                self.site_open
                or bool(self.filter_text.strip())
            )
        )

    @rx.event
    def toggle_sidebar(self):
        """Expande ou recolhe a sidebar."""

        self.expanded = not self.expanded

        if not self.expanded:
            # Evita deixar um filtro invisível ativo
            # quando a sidebar estiver recolhida.
            self.filter_text = ""

    @rx.event
    def toggle_site(self):
        """Expande ou recolhe o grupo Site."""

        if not self.expanded:
            self.expanded = True
            self.site_open = True
            return

        self.site_open = not self.site_open

    @rx.event
    def update_filter(self, value: str):
        """Atualiza a pesquisa dos itens de navegação."""

        self.filter_text = value