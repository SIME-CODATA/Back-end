from __future__ import annotations

from copy import deepcopy
from typing import Any

import reflex as rx

from Back_end.access.core.guards import (
    can_access,
)
from Back_end.access.core.permissions import (
    Permission,
)
from Back_end.access.states.auth_state import (
    AuthState,
)
from Back_end.site_cms.modules.metas.overview_service import (
    get_effective_budget,
    get_overview_section,
)
from Back_end.site_cms.services.editorial_service import (
    publish_section,
    save_section_draft,
)


KnowMetaRow = dict[str, str]
AxisBudgetRow = dict[str, str]


def _format_money_input(
    value: Any,
) -> str:
    try:
        number = float(
            value or 0
        )
    except (
        TypeError,
        ValueError,
    ):
        return "0"

    if number.is_integer():
        return str(
            int(number)
        )

    return str(number)


def _parse_number(
    value: object,
) -> float:
    raw = str(
        value or ""
    ).strip()

    if not raw:
        return 0.0

    normalized = (
        raw
        .replace("R$", "")
        .replace(" ", "")
    )

    if (
        "," in normalized
        and "." in normalized
    ):
        normalized = (
            normalized
            .replace(".", "")
            .replace(",", ".")
        )
    elif "," in normalized:
        normalized = (
            normalized
            .replace(",", ".")
        )

    try:
        return float(
            normalized
        )
    except ValueError:
        return 0.0


def _parse_int(
    value: object,
) -> int:
    try:
        return int(
            float(
                str(
                    value or "0"
                )
                .strip()
                .replace(",", ".")
            )
        )
    except ValueError:
        return 0


class MetaOverviewCmsState(AuthState):
    """CMS da Visão Geral das Metas."""

    section_id: int | None = None

    loading: bool = False
    saving: bool = False
    publishing: bool = False

    error_message: str = ""
    success_message: str = ""

    status_label: str = ""

    # ========================================================
    # ORÇAMENTO
    # ========================================================

    budget_source: str = "smae"
    budget_update_available: bool = False

    total_budget: str = "0"
    total_metas: str = "0"

    axes_budget: list[
        AxisBudgetRow
    ] = []

    # ========================================================
    # CONHEÇA METAS
    # ========================================================

    know_title: str = "CONHEÇA METAS"

    know_items: list[
        KnowMetaRow
    ] = []

    publication_note: str = ""

    # ========================================================
    # PERMISSÕES
    # ========================================================

    @rx.var
    def can_edit_content(
        self,
    ) -> bool:
        return can_access(
            self.current_user_role,
            Permission.SITE_EDIT,
        )

    @rx.var
    def can_publish_content(
        self,
    ) -> bool:
        return can_access(
            self.current_user_role,
            Permission.SITE_PUBLISH,
        )

    @rx.var
    def source_label(
        self,
    ) -> str:
        if (
            self.budget_source
            == "cms"
        ):
            return "Personalizado"

        if (
            self.budget_source
            == "legacy"
        ):
            return "API antiga"

        return "SMAE"

    def _require_edit(
        self,
    ) -> bool:
        if not can_access(
            self.current_user_role,
            Permission.SITE_EDIT,
        ):
            self.error_message = (
                "Seu perfil não possui permissão "
                "para editar o Site."
            )
            return False

        return True

    def _require_publish(
        self,
    ) -> bool:
        if not can_access(
            self.current_user_role,
            Permission.SITE_PUBLISH,
        ):
            self.error_message = (
                "Seu perfil não possui permissão "
                "para publicar o Site."
            )
            return False

        return True

    def _load_budget(
        self,
        content: dict[str, Any],
    ) -> None:
        budget_wrapper = (
            content.get("budget")
            or {}
        )

        self.budget_source = str(
            budget_wrapper.get(
                "source"
            )
            or "smae"
        )

        self.budget_update_available = bool(
            budget_wrapper.get(
                "update_available"
            )
        )

        budget = get_effective_budget(
            content
        )

        self.total_budget = (
            _format_money_input(
                budget.get(
                    "total_budget"
                )
            )
        )

        self.total_metas = str(
            budget.get(
                "total_metas"
            )
            or 0
        )

        self.axes_budget = [
            {
                "name": str(
                    item.get(
                        "name"
                    )
                    or ""
                ),
                "color": str(
                    item.get(
                        "color"
                    )
                    or ""
                ),
                "meta_count": str(
                    item.get(
                        "meta_count"
                    )
                    or 0
                ),
                "budget": (
                    _format_money_input(
                        item.get(
                            "budget"
                        )
                    )
                ),
            }
            for item in (
                budget.get(
                    "axes"
                )
                or []
            )
        ]

    def _load_know_metas(
        self,
        content: dict[str, Any],
    ) -> None:
        know = (
            content.get(
                "know_metas"
            )
            or {}
        )

        self.know_title = str(
            know.get(
                "title"
            )
            or "CONHEÇA METAS"
        )

        self.know_items = [
            {
                "name": str(
                    item.get(
                        "name"
                    )
                    or ""
                ),
                "value": str(
                    item.get(
                        "value"
                    )
                    or ""
                ),
                "order": str(
                    item.get(
                        "order"
                    )
                    or index + 1
                ),
            }
            for index, item
            in enumerate(
                know.get(
                    "items"
                )
                or []
            )
        ]

    def _load_section(
        self,
    ) -> bool:
        section = (
            get_overview_section()
        )

        if (
            section is None
            or section.id is None
        ):
            self.error_message = (
                "A Visão Geral ainda não foi inicializada. "
                "Execute bootstrap_overview."
            )
            return False

        self.section_id = int(
            section.id
        )

        content = dict(
            section.draft_content
            or section.published_content
            or {}
        )

        self._load_budget(
            content
        )
        self._load_know_metas(
            content
        )

        self.status_label = (
            "Rascunho"
            if (
                section.draft_content
                != section.published_content
            )
            else "Publicado"
        )

        return True

    def _current_budget_value(
        self,
    ) -> dict[str, Any]:
        return {
            "total_budget": (
                _parse_number(
                    self.total_budget
                )
            ),
            "total_metas": (
                _parse_int(
                    self.total_metas
                )
            ),
            "axes": [
                {
                    "name": str(
                        row.get(
                            "name"
                        )
                        or ""
                    ).strip(),
                    "color": str(
                        row.get(
                            "color"
                        )
                        or ""
                    ).strip(),
                    "meta_count": (
                        _parse_int(
                            row.get(
                                "meta_count"
                            )
                        )
                    ),
                    "budget": (
                        _parse_number(
                            row.get(
                                "budget"
                            )
                        )
                    ),
                }
                for row in (
                    self.axes_budget
                )
            ],
            "source": (
                self.budget_source
            ),
        }

    def _build_content(
        self,
    ) -> dict[str, Any]:
        section = (
            get_overview_section()
        )

        base = dict(
            section.draft_content
            or {}
        ) if section else {}

        budget_wrapper = deepcopy(
            base.get("budget")
            or {}
        )

        if (
            self.budget_source
            == "cms"
        ):
            budget_wrapper[
                "source"
            ] = "cms"
            budget_wrapper[
                "cms_value"
            ] = (
                self._current_budget_value()
            )
        else:
            # Mantém a origem automática que já está ativa.
            # Pode ser "legacy" enquanto o orçamento SMAE local
            # ainda não estiver disponível.
            budget_wrapper[
                "source"
            ] = self.budget_source
            budget_wrapper[
                "cms_value"
            ] = None
            budget_wrapper[
                "update_available"
            ] = False

        know_items = [
            {
                "name": str(
                    row.get(
                        "name"
                    )
                    or ""
                ).strip(),
                "value": str(
                    row.get(
                        "value"
                    )
                    or ""
                ).strip(),
                "order": str(
                    row.get(
                        "order"
                    )
                    or ""
                ).strip(),
            }
            for row in (
                self.know_items
            )
        ]

        def _know_sort_key(
            item: dict[str, str],
        ):
            raw = str(
                item.get(
                    "order"
                )
                or ""
            ).strip()

            try:
                return (
                    0,
                    int(raw),
                )
            except ValueError:
                return (
                    1,
                    raw.casefold(),
                )

        know_items.sort(
            key=_know_sort_key
        )

        return {
            **base,
            "budget": (
                budget_wrapper
            ),
            "know_metas": {
                "title": (
                    self.know_title
                    .strip()
                ),
                "items": know_items,
            },
        }

    # ========================================================
    # LOAD
    # ========================================================

    @rx.event
    def load_page(
        self,
    ):
        redirect = (
            self._require_permission(
                Permission.SITE_VIEW
            )
        )

        if redirect is not None:
            return redirect

        self.loading = True
        self.error_message = ""
        self.success_message = ""
        self.publication_note = ""

        yield

        try:
            self._load_section()

        except Exception as error:
            print(
                "Erro ao carregar Visão Geral CMS: "
                f"{error}"
            )

            self.error_message = (
                "Não foi possível carregar "
                "a Visão Geral."
            )

        finally:
            self.loading = False

    # ========================================================
    # ORÇAMENTO
    # ========================================================

    @rx.event
    def enable_budget_override(
        self,
    ):
        self.budget_source = "cms"
        self.budget_update_available = False

    @rx.event
    def use_automatic_budget(
        self,
    ):
        section = (
            get_overview_section()
        )

        if section is None:
            return

        content = dict(
            section.draft_content
            or {}
        )

        budget_wrapper = (
            content.get(
                "budget"
            )
            or {}
        )

        smae_value = (
            budget_wrapper.get(
                "smae_value"
            )
            or {}
        )

        legacy_value = (
            budget_wrapper.get(
                "legacy_value"
            )
            or {}
        )

        smae_total = float(
            smae_value.get(
                "total_budget"
            )
            or 0
        )

        if smae_total > 0:
            automatic_source = "smae"
        elif legacy_value:
            automatic_source = "legacy"
        else:
            automatic_source = "smae"

        self.budget_source = (
            automatic_source
        )
        self.budget_update_available = False

        self._load_budget({
            **content,
            "budget": {
                **budget_wrapper,
                "source": (
                    automatic_source
                ),
                "cms_value": None,
                "update_available": False,
            },
        })

    @rx.event
    def set_total_budget(
        self,
        value: str,
    ):
        self.total_budget = value
        self.budget_source = "cms"

    @rx.event
    def set_total_metas(
        self,
        value: str,
    ):
        self.total_metas = value
        self.budget_source = "cms"

    def _update_axis(
        self,
        index: int,
        field: str,
        value: str,
    ) -> None:
        rows = [
            dict(row)
            for row in (
                self.axes_budget
            )
        ]

        if (
            0
            <= index
            < len(rows)
        ):
            rows[
                index
            ][
                field
            ] = value

            self.axes_budget = rows
            self.budget_source = "cms"

    @rx.event
    def update_axis_field(
        self,
        index: int,
        field: str,
        value: str,
    ):
        self._update_axis(
            index,
            field,
            value,
        )

    @rx.event
    def add_axis(
        self,
    ):
        self.axes_budget = [
            *self.axes_budget,
            {
                "name": "",
                "color": "",
                "meta_count": "0",
                "budget": "0",
            },
        ]
        self.budget_source = "cms"

    @rx.event
    def remove_axis(
        self,
        index: int,
    ):
        self.axes_budget = [
            dict(row)
            for position, row
            in enumerate(
                self.axes_budget
            )
            if position != index
        ]
        self.budget_source = "cms"

    # ========================================================
    # CONHEÇA METAS
    # ========================================================

    @rx.event
    def set_know_title(
        self,
        value: str,
    ):
        self.know_title = value

    def _update_know_item(
        self,
        index: int,
        field: str,
        value: str,
    ) -> None:
        rows = [
            dict(row)
            for row in (
                self.know_items
            )
        ]

        if (
            0
            <= index
            < len(rows)
        ):
            rows[
                index
            ][
                field
            ] = value

            self.know_items = rows

    @rx.event
    def update_know_item(
        self,
        index: int,
        field: str,
        value: str,
    ):
        self._update_know_item(
            index,
            field,
            value,
        )

    @rx.event
    def add_know_item(
        self,
    ):
        self.know_items = [
            *self.know_items,
            {
                "name": "",
                "value": "",
                "order": str(
                    len(
                        self.know_items
                    )
                    + 1
                ),
            },
        ]

    @rx.event
    def remove_know_item(
        self,
        index: int,
    ):
        self.know_items = [
            dict(row)
            for position, row
            in enumerate(
                self.know_items
            )
            if position != index
        ]

    @rx.event
    def set_publication_note(
        self,
        value: str,
    ):
        self.publication_note = value

    # ========================================================
    # SAVE / PUBLISH
    # ========================================================

    @rx.event
    def save_draft(
        self,
    ):
        if not self._require_edit():
            return

        if self.section_id is None:
            return

        self.saving = True
        self.error_message = ""
        self.success_message = ""

        try:
            save_section_draft(
                section_id=(
                    self.section_id
                ),
                content=(
                    self._build_content()
                ),
                actor_user_id=(
                    self.current_user_id
                    or 0
                ),
            )

            self._load_section()

            self._audit(
                action=(
                    "SITE_META_OVERVIEW_UPDATED"
                ),
                entity_type=(
                    "cms_section"
                ),
                entity_id=(
                    self.section_id
                ),
                description=(
                    "Rascunho da Visão Geral "
                    "das Metas atualizado."
                ),
            )

            self.success_message = (
                "Rascunho salvo com sucesso."
            )

        except Exception as error:
            print(
                "Erro ao salvar Visão Geral CMS: "
                f"{error}"
            )

            self.error_message = (
                "Não foi possível salvar "
                "o rascunho."
            )

        finally:
            self.saving = False

    @rx.event
    def publish(
        self,
    ):
        if not self._require_publish():
            return

        if self.section_id is None:
            return

        self.publishing = True
        self.error_message = ""
        self.success_message = ""

        try:
            # Garante que a tela atual está no draft.
            save_section_draft(
                section_id=(
                    self.section_id
                ),
                content=(
                    self._build_content()
                ),
                actor_user_id=(
                    self.current_user_id
                    or 0
                ),
            )

            _, version = publish_section(
                section_id=(
                    self.section_id
                ),
                actor_user_id=(
                    self.current_user_id
                    or 0
                ),
                note=(
                    self.publication_note
                ),
            )

            self.publication_note = ""

            self._load_section()

            self._audit(
                action=(
                    "SITE_META_OVERVIEW_PUBLISHED"
                ),
                entity_type=(
                    "cms_section"
                ),
                entity_id=(
                    self.section_id
                ),
                description=(
                    "Visão Geral das Metas "
                    f"publicada na versão "
                    f"{version.version_number}."
                ),
            )

            self.success_message = (
                "Visão Geral publicada com sucesso."
            )

        except Exception as error:
            print(
                "Erro ao publicar Visão Geral CMS: "
                f"{error}"
            )

            self.error_message = (
                "Não foi possível publicar "
                "a Visão Geral."
            )

        finally:
            self.publishing = False
