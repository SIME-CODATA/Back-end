import reflex as rx

from Back_end.access.core.permissions import Permission
from Back_end.access.states.auth_state import AuthState
from Back_end.site_cms.schemas.home.constants import HOME_SECTION_EDITOR_META
from Back_end.site_cms.services.content_service import list_home_sections


SectionRow = dict[str, str]


def _truncate(value: object, limit: int = 180) -> str:
    text = " ".join(str(value or "").split())

    if len(text) <= limit:
        return text

    return text[: limit - 1].rstrip() + "…"


def _content_summary(section_key: str, content: dict) -> str:
    """Cria um resumo curto e amigável para o card da seção."""

    if section_key == "about_pdm":
        message = content.get("mayor_message") or {}
        title = message.get("title") or "Carta do prefeito"
        author = message.get("author") or ""
        paragraphs = message.get("paragraphs") or []
        suffix = f" • {author}" if author else ""
        return _truncate(
            f"{title}{suffix}. {len(paragraphs)} parágrafo(s) cadastrado(s)."
        )

    if section_key == "news":
        total = len(content.get("items") or [])
        return f"{total} notícia(s) cadastrada(s) para exibição na Página Inicial."

    if section_key == "axes":
        total = len(content.get("items") or [])
        return f"{total} eixo(s) configurado(s), com textos, cores e recursos visuais."

    if section_key == "transparency":
        title = content.get("title") or "Transparência"
        total = len(content.get("cards") or [])
        return f"{title}. {total} recurso(s) ou card(s) configurado(s)."

    if section_key == "history":
        title = content.get("title") or "Histórico"
        total = len(content.get("cards") or [])
        return f"{title}. {total} conjunto(s) histórico(s) cadastrado(s)."

    if section_key == "regionalization":
        title = content.get("title") or "Regionalização"
        body = content.get("body") or content.get("subtitle") or ""
        return _truncate(f"{title}. {body}".strip(". "))

    return "Conteúdo administrável da Página Inicial."


class HomeCmsState(AuthState):
    """Estado da administração da Página Inicial."""

    sections: list[SectionRow] = []

    loading: bool = False
    error_message: str = ""

    section_count: int = 0
    draft_count: int = 0
    published_count: int = 0

    @staticmethod
    def _serialize_section(section) -> SectionRow:
        draft_content = dict(section.draft_content or {})
        published_content = dict(section.published_content or {})
        section_key = str(section.key or "")

        has_draft = draft_content != published_content

        if has_draft:
            status_label = "Rascunho"
        elif str(section.status or "").lower() == "published":
            status_label = "Publicado"
        else:
            status_label = str(section.status or "Publicado").capitalize()

        meta = HOME_SECTION_EDITOR_META.get(section_key, {})

        return {
            "id": str(section.id or ""),
            "key": section_key,
            "name": str(meta.get("name") or section.name or ""),
            "description": str(meta.get("description") or ""),
            "icon": str(meta.get("icon") or "file_text"),
            "editor_href": str(meta.get("route") or "/admin/site/home"),
            "section_type": str(section.section_type or ""),
            "position": str(section.position or 0),
            "position_label": f"{int(section.position or 0) // 10:02d}",
            "status_label": status_label,
            "has_draft": "true" if has_draft else "false",
            "enabled": "true" if bool(section.enabled) else "false",
            "summary": _content_summary(
                section_key,
                published_content,
            ),
            "source_label": (
                "Conteúdo inicial importado"
                if str(section.source_type or "") == "legacy_api"
                else "Conteúdo do CMS"
            ),
        }

    def _reload_sections(self) -> None:
        items = list_home_sections()

        self.sections = [
            self._serialize_section(section)
            for section in items
        ]

        self.section_count = len(self.sections)
        self.draft_count = sum(
            1
            for item in self.sections
            if item["has_draft"] == "true"
        )
        self.published_count = sum(
            1
            for item in self.sections
            if item["status_label"] == "Publicado"
        )

    @rx.event
    def load_page(self):
        """Valida o acesso e carrega as seções reais do banco."""

        redirect = self._require_permission(
            Permission.SITE_VIEW
        )

        if redirect is not None:
            return redirect

        self.loading = True
        self.error_message = ""

        try:
            self._reload_sections()

        except Exception as error:
            print(
                "Erro ao carregar CMS da Página Inicial: "
                f"{error}"
            )

            self.sections = []
            self.section_count = 0
            self.draft_count = 0
            self.published_count = 0
            self.error_message = (
                "Não foi possível carregar o conteúdo da Página Inicial."
            )

        finally:
            self.loading = False
