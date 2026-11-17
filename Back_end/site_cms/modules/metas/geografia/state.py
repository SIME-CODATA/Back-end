"""Editor Reflex para as 19 colunas de cada ação/localização de uma Meta."""
from __future__ import annotations
from typing import Any
from pathlib import Path
from tempfile import TemporaryDirectory
import reflex as rx

from Back_end.access.states.auth_state import AuthState
from Back_end.access.core.permissions import Permission
from Back_end.site_cms.modules.metas.code import canonical_meta_code
from Back_end.site_cms.modules.metas.geografia.parser import COLUMNS, IDENTITY_FIELDS, PUBLIC_FLAG
from Back_end.site_cms.modules.metas.geografia import service


class GeoCmsState(AuthState):
    meta_code: str = ""
    rows: list[dict[str, str]] = []
    selected_id: int = 0
    fields: list[dict[str, str]] = []
    edited_values: dict[str, str] = {}
    loading: bool = False
    saving: bool = False
    error_geo: str = ""
    notice_geo: str = ""
    selected_status: str = ""
    selected_source: str = ""
    pending_count: int = 0

    @rx.var
    def total_registros(self) -> int:
        return len(self.rows)

    @rx.var
    def can_publish_geo(self) -> bool:
        from Back_end.access.core.guards import can_access
        return can_access(self.current_user_role, Permission.SITE_PUBLISH)

    def _refresh_rows(self):
        self.rows = []
        for item in service.list_rows(self.meta_code):
            draft = item.draft_payload or {}
            self.rows.append({
                "id": str(item.id),
                "codigo": str(draft.get("codigo", item.external_code)),
                "descricao": str(draft.get("Descrição Projeto", "")) or "Sem descrição",
                "distrito": str(draft.get("Distrito", "")),
                "status": "Publicado" if item.published_payload is not None else "Não publicado",
                "publicavel": str(draft.get(PUBLIC_FLAG, "")) or "Indefinido",
                "conflitos": str(len(item.pending_updates or {})),
            })

    def _display_record(self, item):
        if not item:
            self.selected_id = 0
            self.fields = []
            return
        self.selected_id = int(item.id)
        self.edited_values = {}
        original = dict(item.source_payload or {})
        draft = dict(item.draft_payload or {})
        sources = dict(item.source_map or {})
        pending = dict(item.pending_updates or {})
        keys = list(COLUMNS) + sorted((draft.keys() | original.keys()) - set(COLUMNS))
        self.fields = [
            {
                "key": key,
                "label": key,
                "value": str(draft.get(key, "")),
                "original": str(original.get(key, "")),
                "source": str(sources.get(key, item.source)),
                "locked": "sim" if key in IDENTITY_FIELDS else "nao",
                "conflict": "sim" if key in pending else "nao",
                "has_source": "sim" if key in original else "nao",
            }
            for key in keys
        ]
        self.selected_status = "Publicado" if item.published_payload is not None else "Não publicado"
        self.selected_source = item.source
        self.pending_count = len(pending)

    @rx.event
    def load_page(self):
        redirect = self._require_permission(Permission.SITE_VIEW)
        if redirect is not None:
            return redirect
        self.loading, self.error_geo, self.notice_geo = True, "", ""
        yield
        try:
            # /admin/site/metas/{codigo}/territorio
            code = self.router.url.path.strip("/").split("/")[-2]
            self.meta_code = canonical_meta_code(code)
            self._refresh_rows()
            self._display_record(None)
        except Exception as error:
            self.error_geo = f"Erro ao abrir geografia: {error}"
        finally:
            self.loading = False

    @rx.event
    def select_record(self, row_id: str):
        redirect = self._require_permission(Permission.SITE_VIEW)
        if redirect is not None:
            return redirect
        self.error_geo, self.notice_geo = "", ""
        record = service.get_row(int(row_id), self.meta_code)
        if record is None:
            self.error_geo = "Registro não encontrado nesta Meta."
            return
        self._display_record(record)

    @rx.event
    def edit_field(self, field_key: str, value: str):
        redirect = self._require_permission(Permission.SITE_EDIT)
        if redirect is not None:
            return redirect
        if field_key in IDENTITY_FIELDS:
            return
        self.edited_values = {**self.edited_values, field_key: value}
        self.fields = [
            {**entry, "value": value, "source": "manual"}
            if entry["key"] == field_key else entry
            for entry in self.fields
        ]

    @rx.event
    async def upload_geography(self, files: list[rx.UploadFile]):
        """Importação segura pela interface, sem armazenar arquivos na pasta pública."""
        redirect = self._require_permission(Permission.SITE_EDIT)
        if redirect is not None:
            return redirect
        if not files or len(files) != 1:
            self.error_geo = "Selecione exatamente um arquivo CSV, XLSX ou JSON."
            return
        file = files[0]
        extension = Path(file.name or "").suffix.lower()
        if extension not in {".csv", ".xlsx", ".xlsm", ".json"}:
            self.error_geo = "Formato inválido. Use CSV, XLSX/XLSM ou JSON."
            return
        try:
            # Limite de 15 MiB para evitar consumo excessivo de memória.
            contents = await file.read(15 * 1024 * 1024 + 1)
            if len(contents) > 15 * 1024 * 1024:
                raise ValueError("Arquivo maior que 15 MiB. Use a CLI de importação.")
            from Back_end.site_cms.modules.metas.geografia.parser import read_records
            with TemporaryDirectory(prefix="cms_geo_upload_") as directory:
                destination = Path(directory) / ("importacao" + extension)
                destination.write_bytes(contents)
                entries = read_records(destination, source="json" if extension == ".json" else "planilha")
                counts = service.import_rows(entries, dry_run=False)
            self._refresh_rows()
            self._display_record(None)
            self.error_geo = ""
            self.notice_geo = (
                f"Importação: {counts['received']} linhas; "
                f"{counts['created']} criadas; {counts['updated']} atualizadas; "
                f"{counts['unchanged']} inalteradas. Nenhuma publicação automática."
            )
        except Exception as error:
            self.error_geo = f"Importação cancelada: {error}"

    @rx.event
    def create_record(self):
        redirect = self._require_permission(Permission.SITE_EDIT)
        if redirect is not None:
            return redirect
        try:
            row_id = service.create_manual(self.meta_code, actor_user_id=self.current_user_id)
            self._refresh_rows()
            self._display_record(service.get_row(row_id, self.meta_code))
            self.notice_geo = "Registro manual criado em rascunho."
        except Exception as error:
            self.error_geo = str(error)

    @rx.event
    def save_changes(self):
        redirect = self._require_permission(Permission.SITE_EDIT)
        if redirect is not None:
            return redirect
        if not self.selected_id:
            return
        try:
            if self.edited_values:
                service.save_draft(self.selected_id, dict(self.edited_values), actor_user_id=self.current_user_id)
            self._refresh_rows()
            self._display_record(service.get_row(self.selected_id, self.meta_code))
            self.notice_geo = "Rascunho salvo. A API pública permanece inalterada."
            self.error_geo = ""
        except Exception as error:
            self.error_geo = str(error)

    @rx.event
    def restore_field(self, field_key: str):
        redirect = self._require_permission(Permission.SITE_EDIT)
        if redirect is not None:
            return redirect
        if self.edited_values:
            self.error_geo = "Salve ou descarte as alterações antes de restaurar."
            return
        try:
            service.use_source(self.selected_id, field_key, actor_user_id=self.current_user_id)
            self._display_record(service.get_row(self.selected_id, self.meta_code))
            self.notice_geo = f"Campo restaurado da origem: {field_key}"
            self.error_geo = ""
        except Exception as error:
            self.error_geo = str(error)

    @rx.event
    def publish_record(self):
        redirect = self._require_permission(Permission.SITE_PUBLISH)
        if redirect is not None:
            return redirect
        if not self.selected_id:
            return
        try:
            if self.edited_values:
                service.save_draft(self.selected_id, dict(self.edited_values), actor_user_id=self.current_user_id)
            version = service.publish_row(self.selected_id, actor_user_id=self.current_user_id,
                                          note="Publicação pela interface de geografia")
            self._refresh_rows()
            self._display_record(service.get_row(self.selected_id, self.meta_code))
            self.notice_geo = (f"Versão {version} publicada. Somente linhas explicitamente "
                               "autorizadas pela fonte aparecem na API pública.")
            self.error_geo = ""
        except Exception as error:
            self.error_geo = str(error)

    @rx.event
    def unpublish_record(self):
        redirect = self._require_permission(Permission.SITE_PUBLISH)
        if redirect is not None:
            return redirect
        if not self.selected_id:
            return
        try:
            service.unpublish_row(self.selected_id, actor_user_id=self.current_user_id)
            self._refresh_rows()
            self._display_record(service.get_row(self.selected_id, self.meta_code))
            self.notice_geo = "Publicação retirada; histórico preservado."
            self.error_geo = ""
        except Exception as error:
            self.error_geo = str(error)
