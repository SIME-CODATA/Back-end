from __future__ import annotations

import json
import uuid
import re
from copy import deepcopy
from typing import Any

import reflex as rx

from Back_end.media_library.service.service import (
    get_asset,
    list_assets,
    public_asset_url,
    save_asset,
)

from Back_end.access.core.guards import (
    can_access,
)
from Back_end.access.core.permissions import (
    Permission,
)
from Back_end.access.states.auth_state import (
    AuthState,
)
from Back_end.site_cms.modules.metas.code import (
    canonical_meta_code,
)
from Back_end.site_cms.modules.metas.content_service import (
    get_meta_content,
    publish_meta,
    set_manual_field,
    use_smae_field,
)
from Back_end.site_cms.modules.metas.list_service import (
    CmsMetaListItem,
    list_cms_metas,
)
from Back_end.site_cms.modules.metas.sync_service import (
    list_pending_conflicts,
    resolve_all_conflicts,
    resolve_conflict,
)


ActionRow = dict[str, str]
ResultRow = dict[str, str]
RegionBlockRow = dict[str, str]
AssociatedWorkRow = dict[str, str]
AssociatedProjectRow = dict[str, str]
ExtraSectionRow = dict[str, str]
ConflictRow = dict[str, str]


def _media_url(value: Any) -> str:
    """Preserva a identidade da mídia cadastrada, sem perder URLs antigas."""
    if not isinstance(value, dict):
        return ""
    media_id = value.get("media_id")
    if media_id not in (None, ""):
        return f"media:{media_id}"
    return str(value.get("legacy_source") or value.get("url") or "")


def _media_reference(value: str) -> dict[str, Any] | None:
    normalized = str(value or "").strip()
    if not normalized:
        return None
    if normalized.startswith("media:"):
        try:
            media_id = int(normalized.split(":", 1)[1])
            if media_id > 0:
                return {"media_id": media_id, "legacy_source": None}
        except (ValueError, IndexError):
            pass
        return None
    return {"media_id": None, "legacy_source": normalized}


def _media_preview(value: str) -> str:
    ref = str(value or "").strip()
    if ref.startswith("media:"):
        try:
            return public_asset_url(int(ref.split(":", 1)[1]))
        except ValueError:
            return ""
    if ref.startswith("http://programademetas.prefeitura.sp.gov.br"):
        return "https://" + ref.removeprefix("http://")
    return ref


def re_hex_color(value: str) -> bool:
    return bool(re.fullmatch(r"#[0-9A-Fa-f]{6}", str(value or "")))


def _split_lines(
    value: str,
) -> list[str]:
    return [
        line.strip()
        for line in str(
            value or ""
        ).splitlines()
        if line.strip()
    ]


def _join_lines(
    values: list[Any],
) -> str:
    return "\n".join(
        str(value or "").strip()
        for value in (
            values or []
        )
        if str(
            value or ""
        ).strip()
    )


def _safe_int(
    value: object,
) -> int | None:
    raw = str(
        value or ""
    ).strip()

    if not raw:
        return None

    try:
        return int(raw)
    except ValueError:
        return None


def _source_label(
    source: str,
) -> str:
    return {
        "smae": "SMAE",
        "cms": "Personalizado",
        "legacy": "API antiga",
    }.get(
        str(
            source or ""
        ),
        "Sem origem",
    )


def _pretty_value(
    value: Any,
) -> str:
    if isinstance(
        value,
        (
            dict,
            list,
        ),
    ):
        return json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
        )

    if value is None:
        return "Sem valor"

    return str(value)


class MetaCmsState(AuthState):
    """Editor da ficha pública das Metas."""

    # ========================================================
    # LISTAGEM
    # ========================================================

    metas: list[
        CmsMetaListItem
    ] = []

    search_text: str = ""

    list_loading: bool = False
    list_error: str = ""

    # ========================================================
    # META ATUAL
    # ========================================================

    meta_content_id: int | None = None
    meta_code: str = ""

    loading: bool = False
    saving: bool = False
    publishing: bool = False

    error_message: str = ""
    success_message: str = ""

    has_draft: bool = False
    status_label: str = ""

    dirty_fields: list[str] = []

    # ========================================================
    # CAMPOS
    # ========================================================

    number: str = ""
    title: str = ""
    title_highlight: str = ""
    title_complement: str = ""
    projection: str = ""
    indicator: str = ""

    responsible_agencies_text: str = ""

    axis_name: str = ""
    axis_primary_color: str = ""
    axis_secondary_color: str = ""
    axis_phrases_text: str = ""

    evolution: str = ""
    monitoring: str = ""

    strategic_actions: list[
        ActionRow
    ] = []

    measured_results: list[
        ResultRow
    ] = []

    regionalization_mode: str = (
        "not_regionalizable"
    )
    regionalization_note: str = ""
    regionalization_blocks: list[
        RegionBlockRow
    ] = []

    associated_works: list[
        AssociatedWorkRow
    ] = []

    associated_projects: list[
        AssociatedProjectRow
    ] = []

    extra_sections: list[
        ExtraSectionRow
    ] = []

    # ========================================================
    # ORIGENS
    # ========================================================

    source_number: str = ""
    source_title: str = ""
    source_title_highlight: str = ""
    source_title_complement: str = ""
    source_projection: str = ""
    source_strategic_actions: str = ""
    source_indicator: str = ""
    source_responsible_agencies: str = ""
    source_axis_name: str = ""
    source_axis_primary_color: str = ""
    source_axis_secondary_color: str = ""
    source_axis_phrases: str = ""
    source_evolution: str = ""
    source_monitoring: str = ""
    source_measured_results: str = ""
    source_regionalization: str = ""
    source_associated_works: str = ""
    source_associated_projects: str = ""

    # ========================================================
    # CONFLITOS
    # ========================================================

    conflicts: list[
        ConflictRow
    ] = []

    conflict_dialog_open: bool = False

    # ========================================================
    # PUBLICAÇÃO
    # ========================================================

    publication_note: str = ""

    # Editor visual da ficha, sem alterar o modelo de banco.
    visual_region_tab: str = "executed"
    visual_open_action_index: int = -1
    visual_result_index: int = 0
    visual_show_advanced: bool = False
    visual_show_title_fields: bool = False
    visual_media_picker: str = ""
    visual_media_assets: list[dict[str, str]] = []
    visual_media_uploading: bool = False
    visual_media_message: str = ""

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
    def filtered_metas(
        self,
    ) -> list[CmsMetaListItem]:
        term = (
            self.search_text
            .strip()
            .casefold()
        )

        if not term:
            return self.metas

        result: list[
            CmsMetaListItem
        ] = []

        for meta in self.metas:
            if (
                term
                in str(
                    meta.get(
                        "codigo",
                        "",
                    )
                ).casefold()
                or term
                in str(
                    meta.get(
                        "titulo",
                        "",
                    )
                ).casefold()
                or term
                in str(
                    meta.get(
                        "eixo",
                        "",
                    )
                ).casefold()
            ):
                result.append(
                    meta
                )

        return result

    @rx.var
    def conflict_count(
        self,
    ) -> int:
        return len(
            self.conflicts
        )

    # ========================================================
    # PREVIA E BANCO DE MIDIA
    # ========================================================

    @rx.var
    def visual_axis_color(self) -> str:
        color = str(self.axis_primary_color or "").strip()
        return color if re_hex_color(color) else "#3DB54A"

    @rx.var
    def visual_axis_secondary(self) -> str:
        color = str(self.axis_secondary_color or "").strip()
        return color if re_hex_color(color) else "#288140"

    @rx.var
    def visual_axis_phrase_one(self) -> str:
        phrases = _split_lines(self.axis_phrases_text)
        return phrases[0] if phrases else ""

    @rx.var
    def visual_axis_phrase_two(self) -> str:
        phrases = _split_lines(self.axis_phrases_text)
        return " ".join(phrases[1:]) if len(phrases) > 1 else ""

    @rx.var
    def visual_result_value(self) -> str:
        if not self.measured_results:
            return "Item não cadastrado"
        index = min(self.visual_result_index, len(self.measured_results) - 1)
        return str(self.measured_results[index].get("value") or "Item não cadastrado")

    @rx.var
    def visual_result_period(self) -> str:
        if not self.measured_results:
            return "Sem resultado"
        index = min(self.visual_result_index, len(self.measured_results) - 1)
        first = self.measured_results[index]
        return f"{first.get('month') or ''}/{first.get('year') or ''}".strip("/")

    @rx.var
    def visual_has_many_results(self) -> bool:
        return len(self.measured_results) > 1

    @rx.event
    def visual_previous_result(self):
        if self.measured_results:
            self.visual_result_index = (
                self.visual_result_index - 1
            ) % len(self.measured_results)

    @rx.event
    def visual_next_result(self):
        if self.measured_results:
            self.visual_result_index = (
                self.visual_result_index + 1
            ) % len(self.measured_results)

    @rx.var
    def visual_active_image(self) -> str:
        for row in self.regionalization_blocks:
            if row.get("key") == self.visual_region_tab:
                return str(row.get("image_preview") or "")
        return ""

    @rx.var
    def visual_active_text(self) -> str:
        for row in self.regionalization_blocks:
            if row.get("key") == self.visual_region_tab:
                return str(row.get("text") or "")
        return ""

    @rx.var
    def visual_active_footer(self) -> str:
        for row in self.regionalization_blocks:
            if row.get("key") == self.visual_region_tab:
                return str(row.get("footer") or "")
        return ""

    @rx.var
    def visual_media_count(self) -> int:
        return len(self.visual_media_assets)

    @rx.event
    def set_visual_region_tab(self, slot: str):
        if slot in {"planned", "executed"}:
            self.visual_region_tab = slot

    @rx.event
    def set_visual_region_executed(self, checked: bool):
        self.visual_region_tab = "executed" if checked else "planned"

    @rx.event
    def toggle_visual_advanced(self):
        self.visual_show_advanced = not self.visual_show_advanced

    @rx.event
    def toggle_visual_title_fields(self):
        self.visual_show_title_fields = not self.visual_show_title_fields

    @rx.event
    def toggle_visual_action(self, index: int):
        self.visual_open_action_index = (
            -1 if self.visual_open_action_index == index else index
        )

    @rx.event
    def toggle_region_media_picker(self, slot: str):
        if slot in {"planned", "executed"}:
            self.visual_media_picker = (
                "" if self.visual_media_picker == slot else slot
            )

    def _reload_visual_media(self):
        if not can_access(self.current_user_role, Permission.MEDIA_VIEW):
            self.visual_media_assets = []
            return
        try:
            assets = list_assets(media_type="image")
            self.visual_media_assets = [
                {
                    "id": str(asset.id),
                    "name": str(asset.name),
                    "url": public_asset_url(int(asset.id)),
                }
                for asset in reversed(assets[-24:]) if asset.id is not None
            ]
        except Exception as exc:
            print(f"[CMS METAS] Falha ao consultar Banco de Mídia: {exc}")
            self.visual_media_assets = []
            self.visual_media_message = (
                "Não foi possível consultar as imagens. Verifique o Banco de Mídia."
            )

    def _assign_region_asset(self, slot: str, asset_id: int):
        if slot not in {"planned", "executed"}:
            raise ValueError("Imagem de regionalização inválida.")
        asset = get_asset(asset_id)
        if asset is None or asset.media_type != "image":
            raise ValueError("Imagem não encontrada ou inativa no Banco de Mídia.")
        for i, row in enumerate(self.regionalization_blocks):
            if row.get("key") == slot:
                self._update_region_block(i, "image_url", f"media:{asset_id}")
                self._update_region_block(i, "enabled", "true")
                self.regionalization_mode = "custom"
                self._mark_field_dirty("regionalization")
                self.visual_region_tab = slot
                self.visual_media_picker = ""
                return
        raise ValueError("Bloco de imagem não encontrado na Meta.")

    @rx.event
    def choose_region_media(self, slot: str, asset_id: str):
        if not self._require_edit():
            return
        if not can_access(self.current_user_role, Permission.MEDIA_VIEW):
            self.visual_media_message = "Sem permissão para selecionar mídias."
            return
        try:
            self._assign_region_asset(slot, int(asset_id))
            self.visual_media_message = "Imagem selecionada. Salve o rascunho."
        except (ValueError, TypeError) as exc:
            self.visual_media_message = str(exc)

    async def _upload_region_image(self, slot: str, files: list[rx.UploadFile]):
        if not self._require_edit():
            return
        if not can_access(self.current_user_role, Permission.MEDIA_ADD):
            self.visual_media_message = "Sem permissão para enviar imagens."
            return
        if slot not in {"planned", "executed"} or len(files or []) != 1:
            self.visual_media_message = "Selecione uma imagem para o campo correto."
            return
        if self.visual_media_uploading:
            return
        self.visual_media_uploading = True
        self.visual_media_message = ""
        try:
            incoming = files[0]
            original_name = str(incoming.filename or "imagem")
            content = await incoming.read()
            asset = save_asset(
                original_name=original_name,
                content=content,
                name=f"meta_{self.meta_code}_{slot}_{uuid.uuid4().hex[:10]}",
                folder="imagens",
                alt_text=f"Meta {self.meta_code}: mapa {'planejado' if slot == 'planned' else 'executado'}",
                description="Regionalização da ficha de Meta",
                actor_user_id=None,
            )
            if asset.id is None:
                raise ValueError("A mídia foi salva sem identificador.")
            self._assign_region_asset(slot, int(asset.id))
            self._reload_visual_media()
            self.visual_media_message = (
                "Imagem enviada e selecionada. Clique em Salvar rascunho."
            )
        except (ValueError, OSError, RuntimeError) as exc:
            self.visual_media_message = f"Não foi possível enviar a imagem: {exc}"
        except Exception as exc:
            print(f"[CMS METAS] Erro inesperado no envio de imagem: {exc}")
            self.visual_media_message = (
                "Falha no envio. Confira a conexão com o Banco de Mídia e os logs."
            )
        finally:
            self.visual_media_uploading = False

    @rx.event
    async def upload_region_planned(self, files: list[rx.UploadFile]):
        await self._upload_region_image("planned", files)

    @rx.event
    async def upload_region_executed(self, files: list[rx.UploadFile]):
        await self._upload_region_image("executed", files)

    # ========================================================
    # HELPERS
    # ========================================================

    def _require_edit(
        self,
    ) -> bool:
        if not can_access(
            self.current_user_role,
            Permission.SITE_EDIT,
        ):
            self.error_message = (
                "Seu perfil não possui "
                "permissão para editar "
                "conteúdo do site."
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
                "Seu perfil não possui "
                "permissão para publicar "
                "conteúdo do site."
            )
            return False

        return True

    def _mark_field_dirty(
        self,
        field_key: str,
    ) -> None:
        if (
            field_key
            not in self.dirty_fields
        ):
            self.dirty_fields = [
                *self.dirty_fields,
                field_key,
            ]

    def _apply_sources(
        self,
        source_map: dict[
            str,
            str,
        ],
    ) -> None:
        self.source_number = (
            _source_label(
                source_map.get(
                    "number",
                    "",
                )
            )
        )
        self.source_title = (
            _source_label(
                source_map.get(
                    "title",
                    "",
                )
            )
        )
        self.source_title_highlight = (
            _source_label(
                source_map.get(
                    "title_highlight",
                    "",
                )
            )
        )
        self.source_title_complement = (
            _source_label(
                source_map.get(
                    "title_complement",
                    "",
                )
            )
        )
        self.source_projection = (
            _source_label(
                source_map.get(
                    "projection",
                    "",
                )
            )
        )
        self.source_strategic_actions = (
            _source_label(
                source_map.get(
                    "strategic_actions",
                    "",
                )
            )
        )
        self.source_indicator = (
            _source_label(
                source_map.get(
                    "indicator",
                    "",
                )
            )
        )
        self.source_responsible_agencies = (
            _source_label(
                source_map.get(
                    "responsible_agencies",
                    "",
                )
            )
        )
        self.source_axis_name = (
            _source_label(
                source_map.get(
                    "axis_name",
                    "",
                )
            )
        )
        self.source_axis_primary_color = (
            _source_label(
                source_map.get(
                    "axis_primary_color",
                    "",
                )
            )
        )
        self.source_axis_secondary_color = (
            _source_label(
                source_map.get(
                    "axis_secondary_color",
                    "",
                )
            )
        )
        self.source_axis_phrases = (
            _source_label(
                source_map.get(
                    "axis_phrases",
                    "",
                )
            )
        )
        self.source_evolution = (
            _source_label(
                source_map.get(
                    "evolution",
                    "",
                )
            )
        )
        self.source_monitoring = (
            _source_label(
                source_map.get(
                    "monitoring",
                    "",
                )
            )
        )
        self.source_measured_results = (
            _source_label(
                source_map.get(
                    "measured_results",
                    "",
                )
            )
        )
        self.source_regionalization = (
            _source_label(
                source_map.get(
                    "regionalization",
                    "",
                )
            )
        )
        self.source_associated_works = (
            _source_label(
                source_map.get(
                    "associated_works",
                    "",
                )
            )
        )
        self.source_associated_projects = (
            _source_label(
                source_map.get(
                    "associated_projects",
                    "",
                )
            )
        )

    def _apply_content(
        self,
        content: dict[
            str,
            Any,
        ],
    ) -> None:
        self.number = str(
            content.get(
                "number"
            )
            or self.meta_code
        )

        self.title = str(
            content.get(
                "title"
            )
            or ""
        )

        self.title_highlight = str(
            content.get(
                "title_highlight"
            )
            or ""
        )

        self.title_complement = str(
            content.get(
                "title_complement"
            )
            or ""
        )

        self.projection = str(
            content.get(
                "projection"
            )
            or ""
        )

        self.indicator = str(
            content.get(
                "indicator"
            )
            or ""
        )

        self.responsible_agencies_text = (
            _join_lines(
                content.get(
                    "responsible_agencies"
                )
                or []
            )
        )

        self.axis_name = str(
            content.get(
                "axis_name"
            )
            or ""
        )

        self.axis_primary_color = str(
            content.get(
                "axis_primary_color"
            )
            or ""
        )

        self.axis_secondary_color = str(
            content.get(
                "axis_secondary_color"
            )
            or ""
        )

        self.axis_phrases_text = (
            _join_lines(
                content.get(
                    "axis_phrases"
                )
                or []
            )
        )

        self.evolution = str(
            content.get(
                "evolution"
            )
            or ""
        )

        self.monitoring = str(
            content.get(
                "monitoring"
            )
            or ""
        )

        self.strategic_actions = [
            {
                "number": str(
                    item.get(
                        "number"
                    )
                    or ""
                ),
                "description": str(
                    item.get(
                        "description"
                    )
                    or ""
                ),
                "completed": (
                    "true"
                    if bool(
                        item.get(
                            "completed"
                        )
                    )
                    else "false"
                ),
                "evolution_label": str(
                    item.get(
                        "evolution_label"
                    )
                    or ""
                ),
                "evolution_description": str(
                    item.get(
                        "evolution_description"
                    )
                    or ""
                ),
            }
            for item in (
                content.get(
                    "strategic_actions"
                )
                or []
            )
        ]

        self.measured_results = [
            {
                "value": str(
                    item.get(
                        "value"
                    )
                    or ""
                ),
                "month": str(
                    item.get(
                        "month"
                    )
                    or ""
                ),
                "year": str(
                    item.get(
                        "year"
                    )
                    or ""
                ),
                "date": str(
                    item.get(
                        "date"
                    )
                    or ""
                ),
            }
            for item in (
                content.get(
                    "measured_results"
                )
                or []
            )
        ]

        regionalization = (
            content.get(
                "regionalization"
            )
            or {}
        )

        self.regionalization_mode = str(
            regionalization.get(
                "mode"
            )
            or "not_regionalizable"
        )

        self.regionalization_note = str(
            regionalization.get(
                "note"
            )
            or ""
        )

        # Garante dois slots de imagem sem eliminar blocos editoriais existentes.
        original_blocks = [
            item for item in (regionalization.get("blocks") or [])
            if isinstance(item, dict)
        ]
        by_key = {str(item.get("key") or ""): item for item in original_blocks}
        base_blocks = []
        for slot, title in (("planned", "Planejada"), ("executed", "Executada")):
            base_blocks.append(by_key.get(slot) or {
                "key": slot, "title": title, "enabled": True,
                "image": None, "text": "", "footer": "", "buttons": []
            })
        base_blocks.extend(
            item for item in original_blocks
            if str(item.get("key") or "") not in {"planned", "executed"}
        )

        self.regionalization_blocks = [
            {
                "key": str(item.get("key") or ""),
                "title": str(item.get("title") or ""),
                "enabled": "true" if item.get("enabled", True) else "false",
                "image_url": _media_url(item.get("image")),
                "image_preview": _media_preview(_media_url(item.get("image"))),
                "text": str(item.get("text") or ""),
                "footer": str(item.get("footer") or ""),
            }
            for item in base_blocks
        ]

        self.associated_works = [
            {
                "code": str(item.get("code") or ""),
                "name": str(item.get("name") or ""),
                "intervention_type": str(item.get("intervention_type") or ""),
                "subprefectures": _join_lines([
                    sub.get("name") or ""
                    for sub in (item.get("subprefectures") or [])
                    if isinstance(sub, dict)
                ]),
                "regions": _join_lines(item.get("regions") or []),
                "equipment": str(item.get("equipment") or ""),
                "status": str(item.get("status") or ""),
                "percent_complete": str(
                    item.get("percent_complete")
                    if item.get("percent_complete") is not None
                    else ""
                ),
                "latitude": str((item.get("location") or {}).get("latitude") or ""),
                "longitude": str((item.get("location") or {}).get("longitude") or ""),
                "address": str((item.get("location") or {}).get("address") or ""),
            }
            for item in (content.get("associated_works") or [])
            if isinstance(item, dict)
        ]

        self.associated_projects = [
            {
                "code": str(item.get("code") or ""),
                "name": str(item.get("name") or ""),
                "portfolio": str(item.get("portfolio") or ""),
                "stage": str(item.get("stage") or ""),
                "latitude": str((item.get("location") or {}).get("latitude") or ""),
                "longitude": str((item.get("location") or {}).get("longitude") or ""),
                "address": str((item.get("location") or {}).get("address") or ""),
            }
            for item in (content.get("associated_projects") or [])
            if isinstance(item, dict)
        ]

        self.extra_sections = [
            {
                "title": str(item.get("title") or ""),
                "text": str(item.get("text") or ""),
                "image_url": _media_url(item.get("image")),
                "enabled": "true" if item.get("enabled", True) else "false",
            }
            for item in (content.get("extra_sections") or [])
            if isinstance(item, dict)
        ]

    def _content_for_field(
        self,
        field_key: str,
    ) -> Any:
        values: dict[
            str,
            Any,
        ] = {
            "number": (
                canonical_meta_code(
                    self.number
                )
            ),
            "title": self.title.strip(),
            "title_highlight": self.title_highlight.strip(),
            "title_complement": self.title_complement.strip(),
            "projection": (
                self.projection.strip()
            ),
            "indicator": (
                self.indicator.strip()
            ),
            "responsible_agencies": (
                _split_lines(
                    self.responsible_agencies_text
                )
            ),
            "axis_name": (
                self.axis_name.strip()
            ),
            "axis_primary_color": (
                self.axis_primary_color.strip()
            ),
            "axis_secondary_color": (
                self.axis_secondary_color.strip()
            ),
            "axis_phrases": (
                _split_lines(
                    self.axis_phrases_text
                )
            ),
            "evolution": (
                self.evolution.strip()
            ),
            "monitoring": (
                self.monitoring.strip()
            ),
            "strategic_actions": [
                {
                    "number": str(
                        row.get(
                            "number"
                        )
                        or ""
                    ).strip(),
                    "description": str(
                        row.get(
                            "description"
                        )
                        or ""
                    ).strip(),
                    "completed": (
                        str(
                            row.get(
                                "completed"
                            )
                            or "false"
                        )
                        == "true"
                    ),
                    "evolution_label": str(
                        row.get(
                            "evolution_label"
                        )
                        or ""
                    ).strip(),
                    "evolution_description": str(
                        row.get(
                            "evolution_description"
                        )
                        or ""
                    ).strip(),
                }
                for row in (
                    self.strategic_actions
                )
            ],
            "measured_results": [
                {
                    "value": str(
                        row.get(
                            "value"
                        )
                        or ""
                    ).strip(),
                    "month": str(
                        row.get(
                            "month"
                        )
                        or ""
                    ).strip(),
                    "year": (
                        _safe_int(
                            row.get(
                                "year"
                            )
                        )
                    ),
                    "date": str(
                        row.get(
                            "date"
                        )
                        or ""
                    ).strip(),
                }
                for row in (
                    self.measured_results
                )
            ],
            "associated_works": [
                {
                    "id": None,
                    "code": str(row.get("code") or "").strip(),
                    "name": str(row.get("name") or "").strip(),
                    "intervention_type": str(row.get("intervention_type") or "").strip(),
                    "subprefectures": [
                        {"id": None, "name": name, "parent_id": None}
                        for name in _split_lines(str(row.get("subprefectures") or ""))
                    ],
                    "regions": _split_lines(str(row.get("regions") or "")),
                    "equipment": str(row.get("equipment") or "").strip(),
                    "status": str(row.get("status") or "").strip(),
                    "percent_complete": (
                        str(row.get("percent_complete") or "").strip() or None
                    ),
                    "location": {
                        "latitude": (str(row.get("latitude") or "").strip() or None),
                        "longitude": (str(row.get("longitude") or "").strip() or None),
                        "address": str(row.get("address") or "").strip(),
                    },
                }
                for row in self.associated_works
            ],
            "associated_projects": [
                {
                    "id": None,
                    "code": str(row.get("code") or "").strip(),
                    "name": str(row.get("name") or "").strip(),
                    "portfolio": str(row.get("portfolio") or "").strip(),
                    "stage": str(row.get("stage") or "").strip(),
                    "location": {
                        "latitude": (str(row.get("latitude") or "").strip() or None),
                        "longitude": (str(row.get("longitude") or "").strip() or None),
                        "address": str(row.get("address") or "").strip(),
                    },
                }
                for row in self.associated_projects
            ],
            "extra_sections": [
                {
                    "title": str(row.get("title") or "").strip(),
                    "text": str(row.get("text") or "").strip(),
                    "image": _media_reference(str(row.get("image_url") or "")),
                    "enabled": str(row.get("enabled") or "true") == "true",
                }
                for row in self.extra_sections
            ],
            "regionalization": {
                "mode": (
                    self.regionalization_mode
                ),
                "note": (
                    self.regionalization_note.strip()
                    or None
                ),
                "blocks": [
                    {
                        "key": str(
                            row.get(
                                "key"
                            )
                            or ""
                        ).strip(),
                        "title": str(
                            row.get(
                                "title"
                            )
                            or ""
                        ).strip(),
                        "enabled": (
                            str(
                                row.get(
                                    "enabled"
                                )
                                or "true"
                            )
                            == "true"
                        ),
                        "image": (
                            _media_reference(
                                str(
                                    row.get(
                                        "image_url"
                                    )
                                    or ""
                                )
                            )
                        ),
                        "text": str(
                            row.get(
                                "text"
                            )
                            or ""
                        ).strip(),
                        "footer": str(
                            row.get(
                                "footer"
                            )
                            or ""
                        ).strip(),
                        "buttons": [],
                    }
                    for row in (
                        self.regionalization_blocks
                    )
                ],
            },
        }

        return deepcopy(
            values[
                field_key
            ]
        )

    def _refresh_conflicts(
        self,
    ) -> None:
        if not self.meta_code:
            self.conflicts = []
            return

        rows = (
            list_pending_conflicts(
                meta_code=(
                    self.meta_code
                )
            )
        )

        self.conflicts = [
            {
                "id": str(
                    row.id
                    or ""
                ),
                "field_key": str(
                    row.field_key
                ),
                "reason": str(
                    row.reason
                ),
                "cms_value": (
                    _pretty_value(
                        row.cms_value
                    )
                ),
                "smae_value": (
                    _pretty_value(
                        row.incoming_smae_value
                    )
                ),
            }
            for row in rows
        ]

    def _load_record(
        self,
        code: str,
    ) -> bool:
        normalized_code = (
            canonical_meta_code(
                code
            )
        )

        meta = get_meta_content(
            normalized_code
        )

        if (
            meta is None
            or meta.id is None
        ):
            self.meta_code = (
                normalized_code
            )
            self.error_message = (
                "Meta não encontrada "
                "no CMS do site."
            )
            return False

        self.meta_content_id = int(
            meta.id
        )
        self.meta_code = str(
            meta.meta_code
        )

        draft = dict(
            meta.draft_content
            or {}
        )
        published = dict(
            meta.published_content
            or {}
        )

        self._apply_content(
            draft
            if draft
            else published
        )

        self._apply_sources(
            dict(
                meta.source_map
                or {}
            )
        )

        self.has_draft = (
            draft
            != published
        )
        self.status_label = (
            "Rascunho"
            if self.has_draft
            else "Publicado"
        )

        self.dirty_fields = []

        self._refresh_conflicts()
        self.visual_region_tab = "executed"
        self.visual_open_action_index = -1
        self.visual_result_index = 0
        self.visual_show_advanced = False
        self.visual_show_title_fields = False
        self.visual_media_picker = ""
        self.visual_media_message = ""
        self._reload_visual_media()

        return True

    # ========================================================
    # CARREGAMENTO
    # ========================================================

    @rx.event
    def load_metas(
        self,
    ):
        redirect = self._require_permission(
            Permission.SITE_VIEW
        )

        if redirect is not None:
            return redirect

        self.list_loading = True
        self.list_error = ""
        self.search_text = ""

        yield

        try:
            self.metas = (
                list_cms_metas()
            )
        except Exception as error:
            print(
                "Erro ao listar metas CMS: "
                f"{error}"
            )
            self.list_error = (
                "Não foi possível carregar "
                "as Metas do CMS."
            )
        finally:
            self.list_loading = False

    @rx.event
    def load_meta(
        self,
    ):
        redirect = self._require_permission(
            Permission.SITE_VIEW
        )

        if redirect is not None:
            return redirect

        self.loading = True
        self.error_message = ""
        self.success_message = ""
        self.publication_note = ""
        self.conflict_dialog_open = False

        yield

        try:
            code = (
                self.router.url.path
                .rstrip("/")
                .rsplit(
                    "/",
                    1,
                )[-1]
            )

            self._load_record(
                code
            )

        except Exception as error:
            print(
                "Erro ao carregar Meta CMS: "
                f"{error}"
            )

            self.error_message = (
                "Não foi possível carregar "
                "a Meta no CMS."
            )

        finally:
            self.loading = False

    # ========================================================
    # LISTAGEM
    # ========================================================

    @rx.event
    def set_search_text(
        self,
        value: str,
    ):
        self.search_text = value

    # ========================================================
    # SETTERS SIMPLES
    # ========================================================

    @rx.event
    def set_number(
        self,
        value: str,
    ):
        self.number = value
        self._mark_field_dirty(
            "number"
        )

    @rx.event
    def set_title(
        self,
        value: str,
    ):
        self.title = value
        self._mark_field_dirty(
            "title"
        )

    @rx.event
    def set_title_highlight(
        self,
        value: str,
    ):
        self.title_highlight = value
        self._mark_field_dirty(
            "title_highlight"
        )

    @rx.event
    def set_title_complement(
        self,
        value: str,
    ):
        self.title_complement = value
        self._mark_field_dirty(
            "title_complement"
        )

    @rx.event
    def set_projection(
        self,
        value: str,
    ):
        self.projection = value
        self._mark_field_dirty(
            "projection"
        )

    @rx.event
    def set_indicator(
        self,
        value: str,
    ):
        self.indicator = value
        self._mark_field_dirty(
            "indicator"
        )

    @rx.event
    def set_responsible_agencies_text(
        self,
        value: str,
    ):
        self.responsible_agencies_text = (
            value
        )
        self._mark_field_dirty(
            "responsible_agencies"
        )

    @rx.event
    def set_axis_name(
        self,
        value: str,
    ):
        self.axis_name = value
        self._mark_field_dirty(
            "axis_name"
        )

    @rx.event
    def set_axis_primary_color(
        self,
        value: str,
    ):
        self.axis_primary_color = value
        self._mark_field_dirty(
            "axis_primary_color"
        )

    @rx.event
    def set_axis_secondary_color(
        self,
        value: str,
    ):
        self.axis_secondary_color = (
            value
        )
        self._mark_field_dirty(
            "axis_secondary_color"
        )

    @rx.event
    def set_axis_phrases_text(
        self,
        value: str,
    ):
        self.axis_phrases_text = value
        self._mark_field_dirty(
            "axis_phrases"
        )

    @rx.event
    def set_evolution(
        self,
        value: str,
    ):
        self.evolution = value
        self._mark_field_dirty(
            "evolution"
        )

    @rx.event
    def set_monitoring(
        self,
        value: str,
    ):
        self.monitoring = value
        self._mark_field_dirty(
            "monitoring"
        )

    @rx.event
    def set_regionalization_mode(
        self,
        value: str,
    ):
        self.regionalization_mode = (
            value
        )
        self._mark_field_dirty(
            "regionalization"
        )

    @rx.event
    def set_regionalization_note(
        self,
        value: str,
    ):
        self.regionalization_note = (
            value
        )
        self._mark_field_dirty(
            "regionalization"
        )

    @rx.event
    def set_publication_note(
        self,
        value: str,
    ):
        self.publication_note = value

    # ========================================================
    # AÇÕES ESTRATÉGICAS
    # ========================================================

    def _update_action(
        self,
        index: int,
        field: str,
        value: str,
    ) -> None:
        rows = [
            dict(row)
            for row in (
                self.strategic_actions
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

            self.strategic_actions = (
                rows
            )
            self._mark_field_dirty(
                "strategic_actions"
            )

    @rx.event
    def update_action_field(
        self,
        index: int,
        field: str,
        value: str,
    ):
        self._update_action(
            index,
            field,
            value,
        )

    @rx.event
    def add_action(
        self,
    ):
        self.strategic_actions = [
            *self.strategic_actions,
            {
                "number": "",
                "description": "",
                "completed": "false",
                "evolution_label": "",
                "evolution_description": "",
            },
        ]

        self._mark_field_dirty(
            "strategic_actions"
        )

    @rx.event
    def remove_action(
        self,
        index: int,
    ):
        self.strategic_actions = [
            dict(row)
            for position, row
            in enumerate(
                self.strategic_actions
            )
            if position != index
        ]

        self._mark_field_dirty(
            "strategic_actions"
        )

    # ========================================================
    # RESULTADOS
    # ========================================================

    def _update_result(
        self,
        index: int,
        field: str,
        value: str,
    ) -> None:
        rows = [
            dict(row)
            for row in (
                self.measured_results
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

            self.measured_results = (
                rows
            )
            self._mark_field_dirty(
                "measured_results"
            )

    @rx.event
    def update_result_field(
        self,
        index: int,
        field: str,
        value: str,
    ):
        self._update_result(
            index,
            field,
            value,
        )

    @rx.event
    def add_result(
        self,
    ):
        self.measured_results = [
            *self.measured_results,
            {
                "value": "",
                "month": "",
                "year": "",
                "date": "",
            },
        ]

        self._mark_field_dirty(
            "measured_results"
        )

    @rx.event
    def remove_result(
        self,
        index: int,
    ):
        self.measured_results = [
            dict(row)
            for position, row
            in enumerate(
                self.measured_results
            )
            if position != index
        ]

        self._mark_field_dirty(
            "measured_results"
        )

    # ========================================================
    # OBRAS ASSOCIADAS
    # ========================================================

    def _update_work(self, index: int, field: str, value: str) -> None:
        rows = [dict(row) for row in self.associated_works]
        if 0 <= index < len(rows):
            rows[index][field] = value
            self.associated_works = rows
            self._mark_field_dirty("associated_works")

    @rx.event
    def update_work_field(self, index: int, field: str, value: str):
        self._update_work(index, field, value)

    @rx.event
    def add_work(self):
        self.associated_works = [
            *self.associated_works,
            {
                "code": "",
                "name": "",
                "intervention_type": "",
                "subprefectures": "",
                "regions": "",
                "equipment": "",
                "status": "",
                "percent_complete": "",
                "latitude": "",
                "longitude": "",
                "address": "",
            },
        ]
        self._mark_field_dirty("associated_works")

    @rx.event
    def remove_work(self, index: int):
        self.associated_works = [
            dict(row)
            for position, row in enumerate(self.associated_works)
            if position != index
        ]
        self._mark_field_dirty("associated_works")

    # ========================================================
    # PROJETOS ASSOCIADOS
    # ========================================================

    def _update_project(self, index: int, field: str, value: str) -> None:
        rows = [dict(row) for row in self.associated_projects]
        if 0 <= index < len(rows):
            rows[index][field] = value
            self.associated_projects = rows
            self._mark_field_dirty("associated_projects")

    @rx.event
    def update_project_field(self, index: int, field: str, value: str):
        self._update_project(index, field, value)

    @rx.event
    def add_project(self):
        self.associated_projects = [
            *self.associated_projects,
            {
                "code": "",
                "name": "",
                "portfolio": "",
                "stage": "",
                "latitude": "",
                "longitude": "",
                "address": "",
            },
        ]
        self._mark_field_dirty("associated_projects")

    @rx.event
    def remove_project(self, index: int):
        self.associated_projects = [
            dict(row)
            for position, row in enumerate(self.associated_projects)
            if position != index
        ]
        self._mark_field_dirty("associated_projects")

    # ========================================================
    # SEÇÕES EXTRAS
    # ========================================================

    def _update_extra_section(self, index: int, field: str, value: str) -> None:
        rows = [dict(row) for row in self.extra_sections]
        if 0 <= index < len(rows):
            rows[index][field] = value
            self.extra_sections = rows
            self._mark_field_dirty("extra_sections")

    @rx.event
    def update_extra_section_field(self, index: int, field: str, value: str):
        self._update_extra_section(index, field, value)

    @rx.event
    def add_extra_section(self):
        self.extra_sections = [
            *self.extra_sections,
            {"title": "", "text": "", "image_url": "", "enabled": "true"},
        ]
        self._mark_field_dirty("extra_sections")

    @rx.event
    def remove_extra_section(self, index: int):
        self.extra_sections = [
            dict(row)
            for position, row in enumerate(self.extra_sections)
            if position != index
        ]
        self._mark_field_dirty("extra_sections")

    # ========================================================
    # REGIONALIZAÇÃO
    # ========================================================

    def _update_region_block(
        self,
        index: int,
        field: str,
        value: str,
    ) -> None:
        rows = [
            dict(row)
            for row in (
                self.regionalization_blocks
            )
        ]

        if (
            0
            <= index
            < len(rows)
        ):
            rows[index][field] = value
            if field == "image_url":
                rows[index]["image_preview"] = _media_preview(value)

            self.regionalization_blocks = (
                rows
            )

            self._mark_field_dirty(
                "regionalization"
            )

    @rx.event
    def update_region_block_field(
        self,
        index: int,
        field: str,
        value: str,
    ):
        self._update_region_block(
            index,
            field,
            value,
        )

    @rx.event
    def add_region_block(
        self,
    ):
        sequence = (
            len(
                self.regionalization_blocks
            )
            + 1
        )

        self.regionalization_blocks = [
            *self.regionalization_blocks,
            {
                "key": (
                    f"block_{sequence}"
                ),
                "title": "",
                "enabled": "true",
                "image_url": "",
                "image_preview": "",
                "text": "",
                "footer": "",
            },
        ]

        self.regionalization_mode = (
            "custom"
        )
        self._mark_field_dirty(
            "regionalization"
        )

    @rx.event
    def remove_region_block(
        self,
        index: int,
    ):
        self.regionalization_blocks = [
            dict(row)
            for position, row
            in enumerate(
                self.regionalization_blocks
            )
            if position != index
        ]

        self._mark_field_dirty(
            "regionalization"
        )

    # ========================================================
    # RASCUNHO
    # ========================================================

    def _save_dirty_fields(
        self,
    ) -> None:
        fields = list(
            self.dirty_fields
        )

        for field_key in fields:
            set_manual_field(
                meta_code=(
                    self.meta_code
                ),
                field_key=field_key,
                value=(
                    self._content_for_field(
                        field_key
                    )
                ),
                actor_user_id=(
                    self.current_user_id
                    or 0
                ),
            )

        self.dirty_fields = []

        self._load_record(
            self.meta_code
        )

    @rx.event
    def save_draft(
        self,
    ):
        if not self._require_edit():
            return

        self.saving = True
        self.error_message = ""
        self.success_message = ""

        try:
            if not self.dirty_fields:
                self.success_message = (
                    "Nenhuma alteração para salvar."
                )
                return

            changed = ", ".join(
                self.dirty_fields
            )

            self._save_dirty_fields()

            self._audit(
                action=(
                    "SITE_META_UPDATED"
                ),
                entity_type=(
                    "cms_meta"
                ),
                entity_id=(
                    self.meta_content_id
                ),
                description=(
                    f"Rascunho da Meta "
                    f"{self.meta_code} salvo. "
                    f"Campos: {changed}."
                ),
            )

            self.success_message = (
                "Rascunho salvo com sucesso."
            )

        except Exception as error:
            print(
                "Erro ao salvar Meta CMS: "
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

        self.publishing = True
        self.error_message = ""
        self.success_message = ""

        try:
            if self.dirty_fields:
                self._save_dirty_fields()

            _, version = publish_meta(
                meta_code=(
                    self.meta_code
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

            self._load_record(
                self.meta_code
            )

            self._audit(
                action=(
                    "SITE_META_PUBLISHED"
                ),
                entity_type=(
                    "cms_meta"
                ),
                entity_id=(
                    self.meta_content_id
                ),
                description=(
                    f"Meta {self.meta_code} "
                    f"publicada na versão "
                    f"{version.version_number}."
                ),
            )

            self.success_message = (
                "Meta publicada com sucesso."
            )

        except Exception as error:
            print(
                "Erro ao publicar Meta CMS: "
                f"{error}"
            )

            self.error_message = (
                "Não foi possível publicar "
                "a Meta."
            )

        finally:
            self.publishing = False

    # ========================================================
    # VOLTAR A USAR SMAE
    # ========================================================

    @rx.event
    def restore_field_from_smae(
        self,
        field_key: str,
    ):
        if not self._require_edit():
            return

        try:
            use_smae_field(
                meta_code=(
                    self.meta_code
                ),
                field_key=field_key,
                actor_user_id=(
                    self.current_user_id
                    or 0
                ),
            )

            self._load_record(
                self.meta_code
            )

            self.success_message = (
                "Campo restaurado "
                "para o valor do SMAE."
            )

        except Exception as error:
            print(
                "Erro ao restaurar "
                f"campo SMAE: {error}"
            )

            self.error_message = (
                "O SMAE ainda não possui "
                "um valor disponível para "
                "este campo."
            )

    # ========================================================
    # CONFLITOS
    # ========================================================

    @rx.event
    def open_conflicts(
        self,
    ):
        self._refresh_conflicts()
        self.conflict_dialog_open = True

    @rx.event
    def close_conflicts(
        self,
    ):
        self.conflict_dialog_open = False

    @rx.event
    def choose_conflict(
        self,
        conflict_id: str,
        decision: str,
    ):
        if not self._require_edit():
            return

        try:
            resolve_conflict(
                conflict_id=int(
                    conflict_id
                ),
                decision=decision,
                actor_user_id=(
                    self.current_user_id
                    or 0
                ),
            )

            self._load_record(
                self.meta_code
            )

            if not self.conflicts:
                self.conflict_dialog_open = (
                    False
                )

            self.success_message = (
                "Conflito resolvido."
            )

        except Exception as error:
            print(
                "Erro ao resolver "
                f"conflito: {error}"
            )

            self.error_message = (
                "Não foi possível resolver "
                "o conflito."
            )

    @rx.event
    def choose_all_conflicts(
        self,
        decision: str,
    ):
        if not self._require_edit():
            return

        try:
            count = (
                resolve_all_conflicts(
                    meta_code=(
                        self.meta_code
                    ),
                    decision=decision,
                    actor_user_id=(
                        self.current_user_id
                        or 0
                    ),
                )
            )

            self._load_record(
                self.meta_code
            )

            self.conflict_dialog_open = (
                False
            )

            self.success_message = (
                f"{count} conflito(s) "
                "resolvido(s)."
            )

        except Exception as error:
            print(
                "Erro ao resolver "
                f"conflitos: {error}"
            )

            self.error_message = (
                "Não foi possível resolver "
                "os conflitos."
            )
