from __future__ import annotations

import reflex as rx
import traceback
from Back_end.access.core.guards import can_access
from Back_end.access.core.permissions import Permission
from Back_end.access.states.auth_state import AuthState

from Back_end.media_library.service import ( FOLDER_LABELS, archive_asset, list_assets, public_asset_url, save_asset, update_asset,)


MediaRow = dict[str, str]


def _format_size(value: int,) -> str:
    size = float(value or 0)
    if size < 1024:
        return f"{int(size)} B"
    size /= 1024
    if size < 1024:
        return f"{size:.1f} KB"
    size /= 1024
    if size < 1024:
        return f"{size:.1f} MB"
    return f"{size / 1024:.1f} GB"


class MediaLibraryState(AuthState):
    assets: list[MediaRow] = []

    loading: bool = False
    uploading: bool = False
    saving: bool = False

    media_error_message: str = ""
    media_success_message: str = ""

    search_text: str = ""
    media_type_filter: str = "all"
    folder_filter: str = "all"

    upload_name: str = ""
    upload_folder: str = "imagens"
    upload_alt_text: str = ""
    upload_description: str = ""

    editor_open: bool = False
    editing_asset_id: int | None = None
    editing_name: str = ""
    editing_folder: str = "imagens"
    editing_alt_text: str = ""
    editing_description: str = ""

    delete_confirm_open: bool = False
    delete_asset_id: int | None = None
    delete_asset_name: str = ""

    @rx.var
    def can_add_media(self) -> bool:
        return can_access(self.current_user_role, Permission.MEDIA_ADD)

    @rx.var
    def can_edit_media(self) -> bool:
        return can_access(self.current_user_role, Permission.MEDIA_EDIT)

    @rx.var
    def can_delete_media(self) -> bool:
        return can_access(self.current_user_role, Permission.MEDIA_DELETE)
    
    def _actor_user_id(self,) -> int | None:
        value = self.current_user_id
        if value is None:
            return None
        raw = str(value).strip()
        if not raw:
            return None
        try:
            return int(raw)
        except (TypeError, ValueError):
            print(
                "[MEDIA] current_user_id inválido "
                f"para auditoria: {value!r}"
            )
            return None

    @staticmethod
    def _asset_to_row(asset,) -> MediaRow:
        return {
            "id": str(int(asset.id or 0)),
            "name": str(asset.name or ""),
            "folder": str(asset.folder or ""),
            "folder_label": str(
                FOLDER_LABELS.get(
                    asset.folder,
                    asset.folder,
                )
            ),
            "original_name": str(
                asset.original_name or ""
            ),
            "alt_text": str(
                asset.alt_text or ""
            ),
            "description": str(
                asset.description or ""
            ),
            "media_type": str(
                asset.media_type or ""
            ),
            "mime_type": str(
                asset.mime_type or ""
            ),
            "size_label": str(
                _format_size(
                    asset.size_bytes
                )
            ),
            "url": str(
                public_asset_url(
                    int(asset.id or 0)
                )
            ),
        }

    def _reload(self,) -> None:
        self.assets = [
            self._asset_to_row(asset)
            for asset in list_assets(
                search=self.search_text,
                media_type=self.media_type_filter,
                folder=self.folder_filter,
            )
        ]

    @rx.event
    def load_page(self):
        redirect = self._require_permission(Permission.MEDIA_VIEW)
        if redirect is not None:
            return redirect
        self.loading = True
        yield
        try:
            self._reload()
        except Exception as error:
            self.media_error_message = str(error)
        finally:
            self.loading = False

    @rx.event
    def set_search_text(self, value: str):
        self.search_text = value
        self._reload()

    @rx.event
    def set_media_type_filter(self, value: str):
        self.media_type_filter = value
        self._reload()

    @rx.event
    def set_folder_filter(self, value: str):
        self.folder_filter = value
        self._reload()

    @rx.event
    def set_upload_name(self, value: str):
        self.upload_name = value

    @rx.event
    def set_upload_folder(self, value: str):
        self.upload_folder = value

    @rx.event
    def set_upload_alt_text(self, value: str):
        self.upload_alt_text = value

    @rx.event
    def set_upload_description(self, value: str):
        self.upload_description = value

    @rx.event 
    async def upload_files( self, files: list[rx.UploadFile],):
        if self.uploading:
            yield rx.toast.warning(
                "Já existe um upload em andamento.",
                position="top-right",
                duration=4000,
                close_button=True,
            )
            return

        if not can_access(
            self.current_user_role,
            Permission.MEDIA_ADD,
        ):
            self.media_error_message = (
                "Seu perfil não pode adicionar arquivos."
            )

            yield rx.toast.error(
                "Upload não permitido",
                description=self.media_error_message,
                position="top-right",
                duration=6000,
                close_button=True,
            )
            return

        if not self.upload_name.strip():
            self.media_error_message = (
                "Informe o nome/chave da mídia."
            )

            yield rx.toast.warning(
                "Nome da mídia obrigatório",
                description=self.media_error_message,
                position="top-right",
                duration=5000,
                close_button=True,
            )
            return

        if len(files or []) != 1:
            self.media_error_message = (
                "Envie exatamente um arquivo por vez."
            )

            yield rx.toast.warning(
                "Selecione um arquivo",
                description=self.media_error_message,
                position="top-right",
                duration=5000,
                close_button=True,
            )
            return

        self.uploading = True
        self.media_error_message = ""
        self.media_success_message = ""

        # Envia a mudança para a tela imediatamente.
        # Assim o botão pode ficar bloqueado durante o upload.
        yield

        try:
            file = files[0]

            original_name = str(
                file.filename
                or "arquivo"
            )

            actor_user_id = (
                self._actor_user_id()
            )

            print(
                "[MEDIA] Upload iniciado:",
                {
                    "arquivo": original_name,
                    "name": self.upload_name,
                    "folder": self.upload_folder,
                    "actor_user_id": actor_user_id,
                    "current_user_id_original": repr(
                        self.current_user_id
                    ),
                },
            )

            content = await file.read()

            asset = save_asset(
                original_name=original_name,
                content=content,
                name=self.upload_name.strip(),
                folder=self.upload_folder,
                alt_text=self.upload_alt_text.strip(),
                description=(
                    self.upload_description.strip()
                ),
                actor_user_id=None,
            )

            print(
                "[MEDIA] Registro salvo:",
                asset.id,
                asset.name,
                asset.folder,
            )

            # Auditoria não deve transformar um upload
            # já salvo em "falha".
            try:
                self._audit(
                    action="MEDIA_CREATED",
                    entity_type="media_asset",
                    entity_id=asset.id,
                    description=(
                        "Mídia adicionada: "
                        f"{asset.folder}/{asset.name}."
                    ),
                )
            except Exception as audit_error:
                print(
                    "[MEDIA] Aviso: falha na auditoria:",
                    audit_error,
                )

            self.upload_name = ""
            self.upload_alt_text = ""
            self.upload_description = ""

            self._reload()

            self.media_success_message = (
                f"'{asset.name}' foi salvo "
                f"em {asset.folder}."
            )

            yield rx.toast.success(
                "Upload concluído",
                description=(
                    f"{original_name} foi salvo em "
                    f"{asset.folder} com a chave "
                    f"'{asset.name}'."
                ),
                position="top-right",
                duration=7000,
                close_button=True,
            )

        except Exception as error:
            traceback.print_exc()

            self.media_error_message = str(
                error
            )

            yield rx.toast.error(
                "Não foi possível salvar a mídia",
                description=str(error),
                position="top-right",
                duration=10000,
                close_button=True,
            )

        finally:
            self.uploading = False
            yield
            
        print(
            "[MEDIA] SALVO NO BANCO:",
            asset.id,
            asset.name,
            asset.folder,
        )

        self._reload()

        self.upload_name = ""
        self.upload_alt_text = ""
        self.upload_description = ""

        self.media_success_message = (
            f"Mídia '{asset.name}' enviada com sucesso."
        )

        yield rx.toast.success(
            "Upload concluído",
            description=(
                f"{original_name} foi salvo "
                f"em {asset.folder}."
            ),
            position="top-right",
            duration=7000,
            close_button=True,
        )
        try:
            self._audit(
                action="MEDIA_CREATED",
                entity_type="media_asset",
                entity_id=asset.id,
                description=(
                    "Mídia adicionada: "
                    f"{asset.folder}/{asset.name}."
                ),
            )
        except Exception as audit_error:
            print(
                "[MEDIA] Falha apenas na auditoria:",
                audit_error,
            )

    @rx.event
    def open_editor(self,asset_id: str,):
        asset = next( (item for item in self.assets if item["id"] == str(asset_id)), None,)
        if asset is None:
            return
        self.editing_asset_id = int(asset_id)
        self.editing_name = str(asset["name"])
        self.editing_folder = str(asset["folder"])
        self.editing_alt_text = str(asset["alt_text"])
        self.editing_description = str(asset["description"])
        self.editor_open = True

    @rx.event
    def close_editor(self):
        self.editor_open = False
        self.editing_asset_id = None

    @rx.event
    def set_editing_name(self, value: str):
        self.editing_name = value

    @rx.event
    def set_editing_folder(self, value: str):
        self.editing_folder = value

    @rx.event
    def set_editing_alt_text(self, value: str):
        self.editing_alt_text = value

    @rx.event
    def set_editing_description(self, value: str):
        self.editing_description = value

    @rx.event
    def save_editor(self):
        if self.editing_asset_id is None:
            return
        self.saving = True
        try:
            asset = update_asset(
                asset_id=self.editing_asset_id,
                name=self.editing_name,
                folder=self.editing_folder,
                alt_text=self.editing_alt_text,
                description=self.editing_description,
                actor_user_id=self.current_user_id,
            )
            self._audit(
                action="MEDIA_UPDATED",
                entity_type="media_asset",
                entity_id=asset.id,
                description=f"Mídia atualizada: {asset.folder}/{asset.name}.",
            )
            self.editor_open = False
            self._reload()
            self.media_success_message = "Mídia atualizada."
        except Exception as error:
            self.media_error_message = str(error)
        finally:
            self.saving = False

    @rx.event
    def ask_delete(self,asset_id: str,name: str,):
        self.delete_asset_id = int(asset_id)
        self.delete_asset_name = str(name)
        self.delete_confirm_open = True

    @rx.event
    def cancel_delete(self):
        self.delete_confirm_open = False
        self.delete_asset_id = None

    @rx.event
    def confirm_delete(self):
        if self.delete_asset_id is None:
            return
        try:
            asset = archive_asset(
                asset_id=self.delete_asset_id,
                actor_user_id=self.current_user_id,
            )
            self._audit(
                action="MEDIA_ARCHIVED",
                entity_type="media_asset",
                entity_id=asset.id,
                description=f"Mídia arquivada: {asset.folder}/{asset.name}.",
            )
            self.delete_confirm_open = False
            self.delete_asset_id = None
            self._reload()
            self.media_success_message = "Mídia removida da biblioteca."
        except Exception as error:
            self.media_error_message = str(error)
