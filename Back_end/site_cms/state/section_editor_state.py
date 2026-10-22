from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

import reflex as rx

from Back_end.access.core.guards import can_access
from Back_end.access.core.permissions import Permission
from Back_end.access.states.auth_state import AuthState
from Back_end.site_cms.config.sections import (
    SECTION_EDITOR_META,
)
from Back_end.site_cms.services.editor_service import (
    get_cms_section,
    list_section_versions,
)
from Back_end.site_cms.services.editorial_service import (
    publish_section,
    restore_version_to_draft,
    save_section_draft,
)


VersionRow = dict[str, str]
NewsRow = dict[str, str]
AxisRow = dict[str, str]
TransparencyRow = dict[str, str]
HistoryRow = dict[str, str]
HistoryDocumentRow = dict[str, str]
AboutHowRow = dict[str, str]


def _format_datetime(
    value: datetime | None,
) -> str:
    if value is None:
        return "Sem registro"

    try:
        return value.strftime(
            "%d/%m/%Y %H:%M"
        )
    except Exception:
        return str(value)


def _media_url(
    value: dict[str, Any] | None,
) -> str:
    if not value:
        return ""

    return str(
        value.get("legacy_source")
        or value.get("url")
        or ""
    )


def _media_reference(
    url: str,
) -> dict[str, Any] | None:
    normalized = str(url or "").strip()

    if not normalized:
        return None

    return {
        "media_id": None,
        "legacy_source": normalized,
    }


def _split_lines(
    value: str,
) -> list[str]:
    return [
        line.strip()
        for line in str(value or "").splitlines()
        if line.strip()
    ]


def _split_paragraphs(
    value: str,
) -> list[str]:
    raw = str(value or "").replace(
        "\r\n",
        "\n",
    )

    blocks = [
        block.strip()
        for block in raw.split("\n\n")
        if block.strip()
    ]

    if blocks:
        return blocks

    return _split_lines(raw)


def _join_paragraphs(
    values: list[Any],
) -> str:
    return "\n\n".join(
        str(value or "").strip()
        for value in values or []
        if str(value or "").strip()
    )





def _history_years_from_legacy_id(
    legacy_id: str,
) -> tuple[str, str]:
    """
    O endpoint público de histórico traz ids como pdm-2008-2011.
    Usamos isso somente para pré-preencher os anos quando o JSON ainda
    não possui os novos campos editáveis.
    """

    parts = str(
        legacy_id or ""
    ).strip().split("-")

    if (
        len(parts) >= 3
        and parts[-2].isdigit()
        and parts[-1].isdigit()
    ):
        return parts[-2], parts[-1]

    return "", ""


class SectionEditorState(AuthState):
    """Editor editorial compartilhado pelos módulos do Site."""

    # ========================================================
    # ESTADO GERAL
    # ========================================================

    section_id: int | None = None
    section_key: str = ""

    section_name: str = ""
    section_description: str = ""

    status_label: str = ""
    source_label: str = ""
    updated_label: str = ""
    enabled_label: str = ""

    loading: bool = False
    saving: bool = False
    publishing: bool = False

    error_message: str = ""
    success_message: str = ""

    has_draft: bool = False
    preview_open: bool = False

    publication_note: str = ""

    versions: list[VersionRow] = []

    # ========================================================
    # CARTA DO PREFEITO / ABOUT_PDM
    # ========================================================

    about_title: str = ""
    about_subtitle: str = ""
    about_body: str = ""

    about_image_url: str = ""
    about_pdf_url: str = ""

    letter_title: str = ""
    letter_author: str = ""
    letter_paragraphs_text: str = ""

    # ========================================================
    # NOTÍCIAS
    # ========================================================

    news_items: list[NewsRow] = []

    # ========================================================
    # EIXOS
    # ========================================================

    axes_items: list[AxisRow] = []

    # ========================================================
    # TRANSPARÊNCIA
    # ========================================================

    transparency_title: str = ""
    transparency_subtitle: str = ""
    transparency_cards: list[TransparencyRow] = []

    # ========================================================
    # HISTÓRICO
    # ========================================================

    history_title: str = ""
    history_instruction: str = ""
    history_body: str = ""

    # Cada card contém os dados do PDM e a apresentação do card.
    history_cards: list[HistoryRow] = []

    # Documentos ficam em uma lista própria para permitir formulários
    # individuais no Reflex sem depender de textarea ou JSON manual.
    history_documents: list[HistoryDocumentRow] = []

    # ========================================================
    # REGIONALIZAÇÃO
    # ========================================================

    regionalization_title: str = ""
    regionalization_subtitle: str = ""
    regionalization_instruction: str = ""
    regionalization_body: str = ""
    regionalization_document_url: str = ""
    regionalization_dashboard_url: str = ""


    # ========================================================
    # SOBRE O PDM
    # ========================================================

    site_about_eyebrow: str = ""
    site_about_title: str = ""
    site_about_subtitle: str = ""

    site_about_pdf_url: str = ""
    site_about_pdf2_url: str = ""

    site_about_what: str = ""
    site_about_why: str = ""
    site_about_for_whom: str = ""

    site_about_objective_transparency: str = ""
    site_about_objective_systemic_view: str = ""
    site_about_objective_optimization: str = ""
    site_about_objective_execution: str = ""

    site_about_how_text: str = ""
    site_about_how_cards: list[AboutHowRow] = []

    site_about_indicators_text: str = ""
    site_about_indicators_subtitle: str = ""
    site_about_indicators_section_call: str = ""
    site_about_indicators_section_content: str = ""

    site_about_participation_text: str = ""
    site_about_hearings_content: str = ""
    site_about_hearings_video_url: str = ""
    site_about_feedback_content: str = ""

    # ========================================================
    # SETTERS EXPLÍCITOS
    # ========================================================
    #
    # O Reflex 0.9.8 usado neste projeto não expôs automaticamente
    # os handlers set_<campo> esperados pelos componentes.
    # Mantemos os setters explícitos para evitar falha de compilação.
    # ========================================================

    @rx.event
    def set_about_title(self, value: str):
        self.about_title = value

    @rx.event
    def set_about_subtitle(self, value: str):
        self.about_subtitle = value

    @rx.event
    def set_about_body(self, value: str):
        self.about_body = value

    @rx.event
    def set_about_image_url(self, value: str):
        self.about_image_url = value

    @rx.event
    def set_about_pdf_url(self, value: str):
        self.about_pdf_url = value

    @rx.event
    def set_letter_title(self, value: str):
        self.letter_title = value

    @rx.event
    def set_letter_author(self, value: str):
        self.letter_author = value

    @rx.event
    def set_letter_paragraphs_text(self, value: str):
        self.letter_paragraphs_text = value

    @rx.event
    def set_transparency_title(self, value: str):
        self.transparency_title = value

    @rx.event
    def set_transparency_subtitle(self, value: str):
        self.transparency_subtitle = value

    @rx.event
    def set_history_title(self, value: str):
        self.history_title = value

    @rx.event
    def set_history_instruction(self, value: str):
        self.history_instruction = value

    @rx.event
    def set_history_body(self, value: str):
        self.history_body = value

    @rx.event
    def set_regionalization_title(self, value: str):
        self.regionalization_title = value

    @rx.event
    def set_regionalization_subtitle(self, value: str):
        self.regionalization_subtitle = value

    @rx.event
    def set_regionalization_instruction(self, value: str):
        self.regionalization_instruction = value

    @rx.event
    def set_regionalization_body(self, value: str):
        self.regionalization_body = value

    @rx.event
    def set_regionalization_document_url(self, value: str):
        self.regionalization_document_url = value

    @rx.event
    def set_regionalization_dashboard_url(self, value: str):
        self.regionalization_dashboard_url = value


    @rx.event
    def set_site_about_eyebrow(self, value: str):
        self.site_about_eyebrow = value

    @rx.event
    def set_site_about_title(self, value: str):
        self.site_about_title = value

    @rx.event
    def set_site_about_subtitle(self, value: str):
        self.site_about_subtitle = value

    @rx.event
    def set_site_about_pdf_url(self, value: str):
        self.site_about_pdf_url = value

    @rx.event
    def set_site_about_pdf2_url(self, value: str):
        self.site_about_pdf2_url = value

    @rx.event
    def set_site_about_what(self, value: str):
        self.site_about_what = value

    @rx.event
    def set_site_about_why(self, value: str):
        self.site_about_why = value

    @rx.event
    def set_site_about_for_whom(self, value: str):
        self.site_about_for_whom = value

    @rx.event
    def set_site_about_objective_transparency(self, value: str):
        self.site_about_objective_transparency = value

    @rx.event
    def set_site_about_objective_systemic_view(self, value: str):
        self.site_about_objective_systemic_view = value

    @rx.event
    def set_site_about_objective_optimization(self, value: str):
        self.site_about_objective_optimization = value

    @rx.event
    def set_site_about_objective_execution(self, value: str):
        self.site_about_objective_execution = value

    @rx.event
    def set_site_about_how_text(self, value: str):
        self.site_about_how_text = value

    @rx.event
    def set_site_about_indicators_text(self, value: str):
        self.site_about_indicators_text = value

    @rx.event
    def set_site_about_indicators_subtitle(self, value: str):
        self.site_about_indicators_subtitle = value

    @rx.event
    def set_site_about_indicators_section_call(self, value: str):
        self.site_about_indicators_section_call = value

    @rx.event
    def set_site_about_indicators_section_content(self, value: str):
        self.site_about_indicators_section_content = value

    @rx.event
    def set_site_about_participation_text(self, value: str):
        self.site_about_participation_text = value

    @rx.event
    def set_site_about_hearings_content(self, value: str):
        self.site_about_hearings_content = value

    @rx.event
    def set_site_about_hearings_video_url(self, value: str):
        self.site_about_hearings_video_url = value

    @rx.event
    def set_site_about_feedback_content(self, value: str):
        self.site_about_feedback_content = value

    @rx.event
    def set_publication_note(self, value: str):
        self.publication_note = value

    @rx.var
    def news_count(self) -> int:
        return len(self.news_items)

    # ========================================================
    # PERMISSÕES
    # ========================================================

    @rx.var
    def can_edit_content(self) -> bool:
        return can_access(
            self.current_user_role,
            Permission.SITE_EDIT,
        )

    @rx.var
    def can_publish_content(self) -> bool:
        return can_access(
            self.current_user_role,
            Permission.SITE_PUBLISH,
        )

    # ========================================================
    # MENSAGENS / PREVIEW
    # ========================================================

    @rx.event
    def clear_messages(self):
        self.error_message = ""
        self.success_message = ""

    @rx.event
    def open_preview(self):
        self.preview_open = True

    @rx.event
    def close_preview(self):
        self.preview_open = False

    # ========================================================
    # HELPERS DE AUTORIZAÇÃO
    # ========================================================

    def _require_edit_permission(self) -> bool:
        if not can_access(
            self.current_user_role,
            Permission.SITE_EDIT,
        ):
            self.error_message = (
                "Seu perfil não possui permissão para editar "
                "conteúdo do site."
            )
            return False

        return True

    def _require_publish_permission(self) -> bool:
        if not can_access(
            self.current_user_role,
            Permission.SITE_PUBLISH,
        ):
            self.error_message = (
                "Seu perfil não possui permissão para publicar "
                "conteúdo do site."
            )
            return False

        return True

    # ========================================================
    # SERIALIZAÇÃO DOS DADOS PARA OS CAMPOS
    # ========================================================

    def _load_about(
        self,
        content: dict[str, Any],
    ) -> None:
        heading = content.get("heading") or {}
        media = content.get("media") or {}
        documents = content.get("documents") or {}
        message = content.get("mayor_message") or {}

        self.about_title = str(
            heading.get("title") or ""
        )
        self.about_subtitle = str(
            heading.get("subtitle") or ""
        )
        self.about_body = str(
            content.get("body") or ""
        )

        self.about_image_url = _media_url(
            media.get("image")
        )
        self.about_pdf_url = _media_url(
            documents.get("about_pdf")
        )

        self.letter_title = str(
            message.get("title") or ""
        )
        self.letter_author = str(
            message.get("author") or ""
        )
        self.letter_paragraphs_text = (
            _join_paragraphs(
                message.get("paragraphs") or []
            )
        )


    def _load_site_about(
        self,
        content: dict[str, Any],
    ) -> None:
        banner = content.get("banner") or {}
        documents = banner.get("documents") or []
        summary = banner.get("summary") or {}
        objectives = content.get("objectives") or {}
        how = content.get("how_it_was_made") or {}
        indicators = content.get("indicators") or {}
        participation = content.get("participation") or {}

        self.site_about_eyebrow = str(
            banner.get("eyebrow") or ""
        )
        self.site_about_title = str(
            banner.get("title") or ""
        )
        self.site_about_subtitle = str(
            banner.get("subtitle") or ""
        )

        self.site_about_pdf_url = (
            _media_url(documents[0])
            if len(documents) > 0
            else ""
        )
        self.site_about_pdf2_url = (
            _media_url(documents[1])
            if len(documents) > 1
            else ""
        )

        self.site_about_what = str(
            summary.get("what") or ""
        )
        self.site_about_why = str(
            summary.get("why") or ""
        )
        self.site_about_for_whom = str(
            summary.get("for_whom") or ""
        )

        self.site_about_objective_transparency = str(
            objectives.get("transparency") or ""
        )
        self.site_about_objective_systemic_view = str(
            objectives.get("systemic_view") or ""
        )
        self.site_about_objective_optimization = str(
            objectives.get("optimization") or ""
        )
        self.site_about_objective_execution = str(
            objectives.get("execution") or ""
        )

        self.site_about_how_text = str(
            how.get("text") or ""
        )
        self.site_about_how_cards = [
            {
                "number": str(
                    card.get("number") or ""
                ),
                "title": str(
                    card.get("title") or ""
                ),
                "content": str(
                    card.get("content") or ""
                ),
                "detail": str(
                    card.get("detail") or ""
                ),
            }
            for card in how.get("cards") or []
        ]

        self.site_about_indicators_text = str(
            indicators.get("text") or ""
        )
        self.site_about_indicators_subtitle = str(
            indicators.get("subtitle") or ""
        )
        self.site_about_indicators_section_call = str(
            indicators.get("section_call") or ""
        )
        self.site_about_indicators_section_content = str(
            indicators.get("section_content") or ""
        )

        self.site_about_participation_text = str(
            participation.get("text") or ""
        )
        self.site_about_hearings_content = str(
            participation.get("hearings_content") or ""
        )
        self.site_about_hearings_video_url = _media_url(
            participation.get("hearings_video")
        )
        self.site_about_feedback_content = str(
            participation.get("feedback_content") or ""
        )

    def _load_news(
        self,
        content: dict[str, Any],
    ) -> None:
        self.news_items = [
            {
                "title": str(
                    item.get("title") or ""
                ),
                "url": str(
                    item.get("url") or ""
                ),
                "date": str(
                    item.get("date") or ""
                ),
                "priority": str(
                    item.get("priority") or 0
                ),
            }
            for item in content.get("items") or []
        ]

    def _load_axes(
        self,
        content: dict[str, Any],
    ) -> None:
        items: list[AxisRow] = []

        for item in content.get("items") or []:
            theme = item.get("theme") or {}
            media = item.get("media") or {}

            items.append({
                "legacy_id": str(
                    item.get("legacy_id") or ""
                ),
                "name": str(
                    item.get("name") or ""
                ),
                "title": str(
                    item.get("title") or ""
                ),
                "primary_color": str(
                    theme.get("primary_color")
                    or ""
                ),
                "image_url": _media_url(
                    media.get("image")
                ),
                "card_image_url": _media_url(
                    media.get("card_image")
                ),
                "highlights_text": "\n".join(
                    str(value or "")
                    for value in (
                        item.get("highlights") or []
                    )
                ),
                "paragraphs_text": (
                    _join_paragraphs(
                        item.get("paragraphs") or []
                    )
                ),
            })

        self.axes_items = items

    def _load_transparency(
        self,
        content: dict[str, Any],
    ) -> None:
        self.transparency_title = str(
            content.get("title") or ""
        )
        self.transparency_subtitle = str(
            content.get("subtitle") or ""
        )

        self.transparency_cards = [
            {
                "title": str(
                    item.get("title") or ""
                ),
                "text": str(
                    item.get("text") or ""
                ),
                "order": str(
                    item.get("order") or 0
                ),
                "button_label": str(
                    (item.get("button") or {}).get(
                        "label"
                    )
                    or ""
                ),
                "button_url": str(
                    (item.get("button") or {}).get(
                        "url"
                    )
                    or ""
                ),
            }
            for item in content.get("cards") or []
        ]

    def _load_history(
        self,
        content: dict[str, Any],
    ) -> None:
        # Os campos gerais continuam preservados internamente para não
        # perder conteúdo legado, mas não aparecem mais no formulário.
        self.history_title = str(
            content.get("title") or ""
        )
        self.history_instruction = str(
            content.get("instruction") or ""
        )
        self.history_body = str(
            content.get("body") or ""
        )

        cards: list[HistoryRow] = []
        documents: list[HistoryDocumentRow] = []

        for card_index, item in enumerate(
            content.get("cards") or []
        ):
            media = item.get("media") or {}
            theme = item.get("theme") or {}

            # Compatibilidade com todas as versões que já tivemos:
            # id novo, legacy_id antigo ou editor_key do hotfix anterior.
            card_id = str(
                item.get("id")
                or item.get("legacy_id")
                or item.get("editor_key")
                or f"pdm-card-{card_index + 1}"
            )

            editor_key = str(
                item.get("editor_key")
                or card_id
                or f"history-card-{card_index + 1}"
            )

            cards.append({
                "editor_key": editor_key,
                "card_id": card_id,
                "order": str(
                    item.get("order")
                    or (card_index + 1)
                ),
                "image_url": _media_url(
                    media.get("image")
                ),
                "primary_color": str(
                    theme.get("primary_color")
                    or item.get("cor_principal")
                    or "#1281AA"
                ),
                "button_color": str(
                    theme.get("button_color")
                    or item.get("cor_botao")
                    or "#292561"
                ),
            })

            for document_index, document in enumerate(
                item.get("documents")
                or item.get("documentos")
                or []
            ):
                document_key = str(
                    document.get("editor_key")
                    or (
                        f"{editor_key}-document-"
                        f"{document_index + 1}"
                    )
                )

                documents.append({
                    "editor_key": document_key,
                    "card_key": editor_key,
                    "type": str(
                        document.get("type")
                        or document.get("tipo")
                        or "pdm"
                    ),
                    "name": str(
                        document.get("name")
                        or document.get("nome")
                        or ""
                    ),
                    "url": str(
                        document.get("url")
                        or _media_url(
                            document.get("file")
                        )
                        or ""
                    ),
                })

        def _order_value(
            row: dict[str, str],
        ) -> int:
            try:
                return int(
                    str(
                        row.get("order") or "0"
                    ).strip()
                    or "0"
                )
            except ValueError:
                return 0

        self.history_cards = sorted(
            cards,
            key=_order_value,
        )
        self.history_documents = documents

    def _load_regionalization(
        self,
        content: dict[str, Any],
    ) -> None:
        self.regionalization_title = str(
            content.get("title") or ""
        )
        self.regionalization_subtitle = str(
            content.get("subtitle") or ""
        )
        self.regionalization_instruction = str(
            content.get("instruction") or ""
        )
        self.regionalization_body = str(
            content.get("body") or ""
        )
        self.regionalization_document_url = (
            _media_url(
                content.get("document")
            )
        )
        self.regionalization_dashboard_url = str(
            content.get("dashboard_url") or ""
        )

    # ========================================================
    # CONTEÚDO MONTADO A PARTIR DOS CAMPOS
    # ========================================================

    def _build_about_content(
        self,
    ) -> dict[str, Any]:
        return {
            "heading": {
                "title": self.about_title.strip(),
                "subtitle": self.about_subtitle.strip(),
            },
            "body": self.about_body.strip(),
            "media": {
                "image": _media_reference(
                    self.about_image_url
                ),
            },
            "documents": {
                "about_pdf": _media_reference(
                    self.about_pdf_url
                ),
            },
            "mayor_message": {
                "title": self.letter_title.strip(),
                "author": self.letter_author.strip(),
                "paragraphs": _split_paragraphs(
                    self.letter_paragraphs_text
                ),
            },
        }


    def _build_site_about_content(
        self,
    ) -> dict[str, Any]:
        documents = [
            value
            for value in [
                _media_reference(
                    self.site_about_pdf_url
                ),
                _media_reference(
                    self.site_about_pdf2_url
                ),
            ]
            if value is not None
        ]

        return {
            "banner": {
                "eyebrow": self.site_about_eyebrow.strip(),
                "title": self.site_about_title.strip(),
                "subtitle": self.site_about_subtitle.strip(),
                "documents": documents,
                "summary": {
                    "what": self.site_about_what.strip(),
                    "why": self.site_about_why.strip(),
                    "for_whom": self.site_about_for_whom.strip(),
                },
            },
            "objectives": {
                "transparency": (
                    self.site_about_objective_transparency.strip()
                ),
                "systemic_view": (
                    self.site_about_objective_systemic_view.strip()
                ),
                "optimization": (
                    self.site_about_objective_optimization.strip()
                ),
                "execution": (
                    self.site_about_objective_execution.strip()
                ),
            },
            "how_it_was_made": {
                "text": self.site_about_how_text.strip(),
                "cards": [
                    {
                        "number": str(
                            row.get("number") or ""
                        ).strip(),
                        "title": str(
                            row.get("title") or ""
                        ).strip(),
                        "content": str(
                            row.get("content") or ""
                        ).strip(),
                        "detail": str(
                            row.get("detail") or ""
                        ).strip(),
                    }
                    for row in self.site_about_how_cards
                ],
            },
            "indicators": {
                "text": self.site_about_indicators_text.strip(),
                "subtitle": (
                    self.site_about_indicators_subtitle.strip()
                ),
                "section_call": (
                    self.site_about_indicators_section_call.strip()
                ),
                "section_content": (
                    self.site_about_indicators_section_content.strip()
                ),
            },
            "participation": {
                "text": self.site_about_participation_text.strip(),
                "hearings_content": (
                    self.site_about_hearings_content.strip()
                ),
                "hearings_video": _media_reference(
                    self.site_about_hearings_video_url
                ),
                "feedback_content": (
                    self.site_about_feedback_content.strip()
                ),
            },
        }

    def _build_news_content(
        self,
    ) -> dict[str, Any]:
        items = []

        for row in self.news_items:
            try:
                priority = int(
                    str(
                        row.get("priority") or "0"
                    ).strip()
                    or "0"
                )
            except ValueError:
                priority = 0

            items.append({
                "title": str(
                    row.get("title") or ""
                ).strip(),
                "url": str(
                    row.get("url") or ""
                ).strip(),
                "date": str(
                    row.get("date") or ""
                ).strip(),
                "priority": priority,
            })

        return {
            "items": items,
        }

    def _build_axes_content(
        self,
    ) -> dict[str, Any]:
        items = []

        for row in self.axes_items:
            legacy_id: int | str | None

            raw_id = str(
                row.get("legacy_id") or ""
            ).strip()

            try:
                legacy_id = int(raw_id)
            except ValueError:
                legacy_id = raw_id or None

            items.append({
                "legacy_id": legacy_id,
                "name": str(
                    row.get("name") or ""
                ).strip(),
                "title": str(
                    row.get("title") or ""
                ).strip(),
                "theme": {
                    "primary_color": str(
                        row.get(
                            "primary_color"
                        )
                        or ""
                    ).strip(),
                },
                "media": {
                    "image": _media_reference(
                        str(
                            row.get("image_url")
                            or ""
                        )
                    ),
                    "card_image": _media_reference(
                        str(
                            row.get(
                                "card_image_url"
                            )
                            or ""
                        )
                    ),
                },
                "highlights": _split_lines(
                    str(
                        row.get(
                            "highlights_text"
                        )
                        or ""
                    )
                ),
                "paragraphs": _split_paragraphs(
                    str(
                        row.get(
                            "paragraphs_text"
                        )
                        or ""
                    )
                ),
            })

        return {
            "items": items,
        }

    def _build_transparency_content(
        self,
    ) -> dict[str, Any]:
        cards = []

        for row in self.transparency_cards:
            try:
                order = int(
                    str(
                        row.get("order") or "0"
                    ).strip()
                    or "0"
                )
            except ValueError:
                order = 0

            cards.append({
                "title": str(
                    row.get("title") or ""
                ).strip(),
                "text": str(
                    row.get("text") or ""
                ).strip(),
                "order": order,
                "button": {
                    "label": str(
                        row.get(
                            "button_label"
                        )
                        or ""
                    ).strip(),
                    "url": (
                        str(
                            row.get(
                                "button_url"
                            )
                            or ""
                        ).strip()
                        or None
                    ),
                },
            })

        return {
            "title": (
                self.transparency_title.strip()
            ),
            "subtitle": (
                self.transparency_subtitle.strip()
                or None
            ),
            "cards": cards,
        }

    def _build_history_content(
        self,
    ) -> dict[str, Any]:
        def _int_value(
            value: object,
            fallback: int = 0,
        ) -> int:
            try:
                return int(
                    str(
                        value or ""
                    ).strip()
                    or fallback
                )
            except ValueError:
                return fallback

        ordered_cards = sorted(
            [
                dict(row)
                for row in self.history_cards
            ],
            key=lambda row: _int_value(
                row.get("order"),
                0,
            ),
        )

        cards: list[dict[str, Any]] = []

        for card_position, row in enumerate(
            ordered_cards
        ):
            card_key = str(
                row.get("editor_key") or ""
            ).strip()

            documents = [
                dict(document)
                for document in self.history_documents
                if str(
                    document.get("card_key") or ""
                )
                == card_key
            ]

            cards.append({
                "id": str(
                    row.get("card_id") or ""
                ).strip(),
                "order": _int_value(
                    row.get("order"),
                    card_position + 1,
                ),
                "media": {
                    "image": _media_reference(
                        str(
                            row.get("image_url")
                            or ""
                        )
                    ),
                },
                "theme": {
                    "primary_color": str(
                        row.get("primary_color")
                        or "#1281AA"
                    ).strip(),
                    "button_color": str(
                        row.get("button_color")
                        or "#292561"
                    ).strip(),
                },
                "documents": [
                    {
                        "type": str(
                            document.get("type")
                            or "pdm"
                        ).strip(),
                        "name": str(
                            document.get("name")
                            or ""
                        ).strip(),
                        "file": _media_reference(
                            str(
                                document.get("url")
                                or ""
                            )
                        ),
                    }
                    for document in documents
                ],
            })

        # Mantemos os textos gerais existentes no JSON para não apagá-los,
        # embora eles não façam mais parte do formulário desta página.
        return {
            "title": self.history_title.strip(),
            "instruction": (
                self.history_instruction.strip()
            ),
            "body": self.history_body.strip(),
            "cards": cards,
        }

    def _build_regionalization_content(
        self,
    ) -> dict[str, Any]:
        return {
            "title": (
                self.regionalization_title.strip()
            ),
            "subtitle": (
                self.regionalization_subtitle.strip()
            ),
            "instruction": (
                self.regionalization_instruction.strip()
            ),
            "body": (
                self.regionalization_body.strip()
            ),
            "document": _media_reference(
                self.regionalization_document_url
            ),
            "dashboard_url": (
                self.regionalization_dashboard_url.strip()
            ),
        }

    def _build_current_content(
        self,
    ) -> dict[str, Any]:
        if self.section_key == "about_pdm":
            return self._build_about_content()

        if self.section_key == "about":
            return self._build_site_about_content()

        if self.section_key == "news":
            return self._build_news_content()

        if self.section_key == "axes":
            return self._build_axes_content()

        if self.section_key == "transparency":
            return self._build_transparency_content()

        if self.section_key == "history":
            return self._build_history_content()

        if self.section_key == "regionalization":
            return (
                self._build_regionalization_content()
            )

        raise ValueError(
            "Módulo do CMS não reconhecido."
        )

    # ========================================================
    # CARREGAMENTO
    # ========================================================

    def _refresh_versions(self) -> None:
        if self.section_id is None:
            self.versions = []
            return

        history = list_section_versions(
            self.section_id
        )

        self.versions = [
            {
                "number": str(
                    version.version_number
                ),
                "note": str(
                    version.note or ""
                ),
                "published_at": (
                    _format_datetime(
                        version.published_at
                    )
                ),
            }
            for version in history
        ]

    def _apply_section_content(
        self,
        section_key: str,
        content: dict[str, Any],
    ) -> None:
        if section_key == "about_pdm":
            self._load_about(content)
            return

        if section_key == "about":
            self._load_site_about(content)
            return

        if section_key == "news":
            self._load_news(content)
            return

        if section_key == "axes":
            self._load_axes(content)
            return

        if section_key == "transparency":
            self._load_transparency(content)
            return

        if section_key == "history":
            self._load_history(content)
            return

        if section_key == "regionalization":
            self._load_regionalization(content)
            return

    def _load_section(
        self,
        page_key: str,
        section_key: str,
    ):
        redirect = self._require_permission(
            Permission.SITE_VIEW
        )

        if redirect is not None:
            return redirect

        self.loading = True
        self.error_message = ""
        self.success_message = ""
        self.preview_open = False
        self.publication_note = ""

        try:
            section = get_cms_section(
                page_key=page_key,
                section_key=section_key,
            )

            if (
                section is None
                or section.id is None
            ):
                self.error_message = (
                    "A seção solicitada não foi encontrada."
                )
                return

            self.section_id = int(
                section.id
            )
            self.section_key = section_key

            meta = (
                SECTION_EDITOR_META.get(
                    section_key,
                    {},
                )
            )

            self.section_name = str(
                meta.get("name")
                or section.name
                or ""
            )
            self.section_description = str(
                meta.get("description")
                or ""
            )

            draft = dict(
                section.draft_content or {}
            )
            published = dict(
                section.published_content or {}
            )

            self.has_draft = (
                draft != published
            )
            self.status_label = (
                "Rascunho"
                if self.has_draft
                else "Publicado"
            )
            self.source_label = (
                "Conteúdo inicial importado"
                if (
                    str(
                        section.source_type
                        or ""
                    )
                    == "legacy_api"
                )
                else "Conteúdo do CMS"
            )
            self.updated_label = (
                _format_datetime(
                    section.updated_at
                )
            )
            self.enabled_label = (
                "Visível no site"
                if section.enabled
                else "Oculta"
            )

            content = (
                draft
                if self.has_draft
                else published
            )

            self._apply_section_content(
                section_key,
                deepcopy(content),
            )
            self._refresh_versions()

        except Exception as error:
            print(
                "Erro ao carregar editor do CMS: "
                f"{error}"
            )
            self.error_message = (
                "Não foi possível carregar "
                "este módulo do CMS."
            )

        finally:
            self.loading = False

    @rx.event
    def load_mayor_letter(self):
        return self._load_section(
            "home",
            "about_pdm",
        )

    @rx.event
    def load_news(self):
        return self._load_section(
            "home",
            "news",
        )

    @rx.event
    def load_axes(self):
        return self._load_section(
            "home",
            "axes",
        )

    @rx.event
    def load_transparency(self):
        return self._load_section(
            "transparency",
            "transparency",
        )

    @rx.event
    def load_history(self):
        return self._load_section(
            "history",
            "history",
        )

    @rx.event
    def load_regionalization(self):
        return self._load_section(
            "regionalization",
            "regionalization",
        )


    @rx.event
    def load_about_page(self):
        return self._load_section(
            "about",
            "about",
        )

    # ========================================================
    # AÇÕES EDITORIAIS
    # ========================================================

    @rx.event
    def save_draft(self):
        if not self._require_edit_permission():
            return

        if self.section_id is None:
            self.error_message = (
                "Nenhuma seção foi carregada."
            )
            return

        self.saving = True
        self.error_message = ""
        self.success_message = ""

        try:
            content = (
                self._build_current_content()
            )

            section = save_section_draft(
                section_id=self.section_id,
                content=content,
                actor_user_id=(
                    self.current_user_id
                    or 0
                ),
            )

            self.has_draft = (
                section.draft_content
                != section.published_content
            )
            self.status_label = (
                "Rascunho"
                if self.has_draft
                else "Publicado"
            )
            self.source_label = (
                "Conteúdo do CMS"
            )
            self.updated_label = (
                _format_datetime(
                    section.updated_at
                )
            )

            self._audit(
                action="SITE_CONTENT_UPDATED",
                entity_type="cms_section",
                entity_id=self.section_id,
                description=(
                    f"Rascunho salvo: "
                    f"{self.section_name}."
                ),
            )

            self.success_message = (
                "Rascunho salvo com sucesso."
            )

        except Exception as error:
            print(
                "Erro ao salvar rascunho CMS: "
                f"{error}"
            )
            self.error_message = (
                "Não foi possível salvar "
                "o rascunho."
            )

        finally:
            self.saving = False

    @rx.event
    def publish(self):
        if not self._require_publish_permission():
            return

        if self.section_id is None:
            self.error_message = (
                "Nenhuma seção foi carregada."
            )
            return

        self.publishing = True
        self.error_message = ""
        self.success_message = ""

        try:
            # Primeiro garante que os campos atuais
            # estejam gravados como rascunho.
            content = (
                self._build_current_content()
            )

            save_section_draft(
                section_id=self.section_id,
                content=content,
                actor_user_id=(
                    self.current_user_id
                    or 0
                ),
            )

            section, version = publish_section(
                section_id=self.section_id,
                actor_user_id=(
                    self.current_user_id
                    or 0
                ),
                note=self.publication_note,
            )

            self.has_draft = False
            self.status_label = (
                "Publicado"
            )
            self.source_label = (
                "Conteúdo do CMS"
            )
            self.updated_label = (
                _format_datetime(
                    section.updated_at
                )
            )
            self.publication_note = ""

            self._refresh_versions()

            self._audit(
                action="SITE_CONTENT_PUBLISHED",
                entity_type="cms_section",
                entity_id=self.section_id,
                description=(
                    f"{self.section_name} "
                    f"publicada na versão "
                    f"{version.version_number}."
                ),
            )

            self.success_message = (
                "Conteúdo publicado com sucesso."
            )

        except Exception as error:
            print(
                "Erro ao publicar conteúdo CMS: "
                f"{error}"
            )
            self.error_message = (
                "Não foi possível publicar "
                "o conteúdo."
            )

        finally:
            self.publishing = False

    @rx.event
    def restore_version(
        self,
        version_number: str,
    ):
        if not self._require_edit_permission():
            return

        if self.section_id is None:
            self.error_message = (
                "Nenhuma seção foi carregada."
            )
            return

        try:
            number = int(
                str(
                    version_number
                ).strip()
            )

            section = (
                restore_version_to_draft(
                    section_id=self.section_id,
                    version_number=number,
                    actor_user_id=(
                        self.current_user_id
                        or 0
                    ),
                )
            )

            self._apply_section_content(
                self.section_key,
                dict(
                    section.draft_content
                    or {}
                ),
            )

            self.has_draft = (
                section.draft_content
                != section.published_content
            )
            self.status_label = (
                "Rascunho"
                if self.has_draft
                else "Publicado"
            )
            self.updated_label = (
                _format_datetime(
                    section.updated_at
                )
            )

            self._audit(
                action="SITE_CONTENT_VERSION_RESTORED",
                entity_type="cms_section",
                entity_id=self.section_id,
                description=(
                    f"Versão {number} restaurada "
                    f"como rascunho em "
                    f"{self.section_name}."
                ),
            )

            self.success_message = (
                f"Versão {number} restaurada "
                "como rascunho."
            )
            self.error_message = ""

        except Exception as error:
            print(
                "Erro ao restaurar versão CMS: "
                f"{error}"
            )
            self.error_message = (
                "Não foi possível restaurar "
                "a versão selecionada."
            )


    # ========================================================
    # LISTAS: SOBRE / COMO FOI FEITO
    # ========================================================

    def _update_site_about_how_field(
        self,
        index: int,
        field: str,
        value: str,
    ) -> None:
        items = [
            dict(item)
            for item in self.site_about_how_cards
        ]

        if 0 <= index < len(items):
            items[index][field] = value
            self.site_about_how_cards = items

    @rx.event
    def update_site_about_how_number(
        self,
        index: int,
        value: str,
    ):
        self._update_site_about_how_field(
            index,
            "number",
            value,
        )

    @rx.event
    def update_site_about_how_title(
        self,
        index: int,
        value: str,
    ):
        self._update_site_about_how_field(
            index,
            "title",
            value,
        )

    @rx.event
    def update_site_about_how_content(
        self,
        index: int,
        value: str,
    ):
        self._update_site_about_how_field(
            index,
            "content",
            value,
        )

    @rx.event
    def update_site_about_how_detail(
        self,
        index: int,
        value: str,
    ):
        self._update_site_about_how_field(
            index,
            "detail",
            value,
        )

    @rx.event
    def add_site_about_how_card(self):
        self.site_about_how_cards = [
            *self.site_about_how_cards,
            {
                "number": "",
                "title": "",
                "content": "",
                "detail": "",
            },
        ]

    @rx.event
    def remove_site_about_how_card(
        self,
        index: int,
    ):
        self.site_about_how_cards = [
            dict(item)
            for position, item
            in enumerate(
                self.site_about_how_cards
            )
            if position != index
        ]

    # ========================================================
    # LISTAS: NOTÍCIAS
    # ========================================================

    @rx.event
    def update_news_title(
        self,
        index: int,
        value: str,
    ):
        items = [
            dict(item)
            for item in self.news_items
        ]

        if 0 <= index < len(items):
            items[index]["title"] = value
            self.news_items = items

    @rx.event
    def update_news_url(
        self,
        index: int,
        value: str,
    ):
        items = [
            dict(item)
            for item in self.news_items
        ]

        if 0 <= index < len(items):
            items[index]["url"] = value
            self.news_items = items

    @rx.event
    def update_news_date(
        self,
        index: int,
        value: str,
    ):
        items = [
            dict(item)
            for item in self.news_items
        ]

        if 0 <= index < len(items):
            items[index]["date"] = value
            self.news_items = items

    @rx.event
    def update_news_priority(
        self,
        index: int,
        value: str,
    ):
        items = [
            dict(item)
            for item in self.news_items
        ]

        if 0 <= index < len(items):
            items[index]["priority"] = value
            self.news_items = items

    @rx.event
    def add_news_item(self):
        self.news_items = [
            *self.news_items,
            {
                "title": "",
                "url": "",
                "date": "",
                "priority": "0",
            },
        ]

    @rx.event
    def remove_news_item(
        self,
        index: int,
    ):
        self.news_items = [
            dict(item)
            for position, item
            in enumerate(
                self.news_items
            )
            if position != index
        ]

    # ========================================================
    # LISTAS: EIXOS
    # ========================================================

    def _update_axis_field(
        self,
        index: int,
        field: str,
        value: str,
    ) -> None:
        items = [
            dict(item)
            for item in self.axes_items
        ]

        if 0 <= index < len(items):
            items[index][field] = value
            self.axes_items = items

    @rx.event
    def update_axis_name(
        self,
        index: int,
        value: str,
    ):
        self._update_axis_field(
            index,
            "name",
            value,
        )

    @rx.event
    def update_axis_title(
        self,
        index: int,
        value: str,
    ):
        self._update_axis_field(
            index,
            "title",
            value,
        )

    @rx.event
    def update_axis_color(
        self,
        index: int,
        value: str,
    ):
        self._update_axis_field(
            index,
            "primary_color",
            value,
        )

    @rx.event
    def update_axis_highlights(
        self,
        index: int,
        value: str,
    ):
        self._update_axis_field(
            index,
            "highlights_text",
            value,
        )

    @rx.event
    def update_axis_paragraphs(
        self,
        index: int,
        value: str,
    ):
        self._update_axis_field(
            index,
            "paragraphs_text",
            value,
        )

    @rx.event
    def update_axis_image_url(
        self,
        index: int,
        value: str,
    ):
        self._update_axis_field(
            index,
            "image_url",
            value,
        )

    @rx.event
    def update_axis_card_image_url(
        self,
        index: int,
        value: str,
    ):
        self._update_axis_field(
            index,
            "card_image_url",
            value,
        )

    # ========================================================
    # LISTAS: TRANSPARÊNCIA
    # ========================================================

    def _update_transparency_field(
        self,
        index: int,
        field: str,
        value: str,
    ) -> None:
        items = [
            dict(item)
            for item
            in self.transparency_cards
        ]

        if 0 <= index < len(items):
            items[index][field] = value
            self.transparency_cards = items

    @rx.event
    def update_transparency_card_title(
        self,
        index: int,
        value: str,
    ):
        self._update_transparency_field(
            index,
            "title",
            value,
        )

    @rx.event
    def update_transparency_card_text(
        self,
        index: int,
        value: str,
    ):
        self._update_transparency_field(
            index,
            "text",
            value,
        )

    @rx.event
    def update_transparency_card_order(
        self,
        index: int,
        value: str,
    ):
        self._update_transparency_field(
            index,
            "order",
            value,
        )

    @rx.event
    def update_transparency_button_label(
        self,
        index: int,
        value: str,
    ):
        self._update_transparency_field(
            index,
            "button_label",
            value,
        )

    @rx.event
    def update_transparency_button_url(
        self,
        index: int,
        value: str,
    ):
        self._update_transparency_field(
            index,
            "button_url",
            value,
        )

    @rx.event
    def add_transparency_card(self):
        self.transparency_cards = [
            *self.transparency_cards,
            {
                "title": "",
                "text": "",
                "order": str(
                    len(
                        self.transparency_cards
                    )
                    + 1
                ),
                "button_label": "",
                "button_url": "",
            },
        ]

    @rx.event
    def remove_transparency_card(
        self,
        index: int,
    ):
        self.transparency_cards = [
            dict(item)
            for position, item
            in enumerate(
                self.transparency_cards
            )
            if position != index
        ]

    # ========================================================
    # LISTAS: HISTÓRICO
    # ========================================================

    def _update_history_card_field(
        self,
        index: int,
        field: str,
        value: str,
    ) -> None:
        items = [
            dict(item)
            for item in self.history_cards
        ]

        if 0 <= index < len(items):
            items[index][field] = value
            self.history_cards = items

    @rx.event
    def update_history_card_field(
        self,
        index: int,
        field: str,
        value: str,
    ):
        self._update_history_card_field(
            index,
            field,
            value,
        )

    @rx.event
    def add_history_card(self):
        sequence = (
            len(self.history_cards)
            + 1
        )

        existing_keys = {
            str(
                item.get("editor_key") or ""
            )
            for item in self.history_cards
        }

        editor_key = (
            f"history-card-new-{sequence}"
        )

        while editor_key in existing_keys:
            sequence += 1
            editor_key = (
                f"history-card-new-{sequence}"
            )

        self.history_cards = [
            *self.history_cards,
            {
                "editor_key": editor_key,
                "card_id": "",
                "order": str(
                    len(self.history_cards)
                    + 1
                ),
                "image_url": "",
                "primary_color": "#1281AA",
                "button_color": "#292561",
            },
        ]

    @rx.event
    def remove_history_card(
        self,
        index: int,
    ):
        if not (
            0 <= index < len(self.history_cards)
        ):
            return

        card_key = str(
            self.history_cards[index].get(
                "editor_key"
            )
            or ""
        )

        self.history_cards = [
            dict(item)
            for position, item
            in enumerate(
                self.history_cards
            )
            if position != index
        ]

        self.history_documents = [
            dict(document)
            for document in self.history_documents
            if str(
                document.get("card_key") or ""
            )
            != card_key
        ]

    def _update_history_document_field(
        self,
        index: int,
        field: str,
        value: str,
    ) -> None:
        documents = [
            dict(item)
            for item in self.history_documents
        ]

        if 0 <= index < len(documents):
            documents[index][field] = value
            self.history_documents = documents

    @rx.event
    def update_history_document_field(
        self,
        index: int,
        field: str,
        value: str,
    ):
        self._update_history_document_field(
            index,
            field,
            value,
        )

    @rx.event
    def add_history_document(
        self,
        card_key: str,
    ):
        normalized_card_key = str(
            card_key or ""
        ).strip()

        if not normalized_card_key:
            return

        sequence = (
            len(self.history_documents)
            + 1
        )

        self.history_documents = [
            *self.history_documents,
            {
                "editor_key": (
                    f"{normalized_card_key}-"
                    f"document-new-{sequence}"
                ),
                "card_key": normalized_card_key,
                "type": "pdm",
                "name": "",
                "url": "",
            },
        ]

    @rx.event
    def remove_history_document(
        self,
        index: int,
    ):
        self.history_documents = [
            dict(item)
            for position, item
            in enumerate(
                self.history_documents
            )
            if position != index
        ]

