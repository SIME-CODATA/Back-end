import reflex as rx

from Back_end.access.core.roles import (
    UserRole,
    get_role_label,
)
from Back_end.access.modules.auth.service import (
    validate_session,
)
from Back_end.access.modules.users.service import (
    create_managed_user,
    delete_managed_user,
    list_users_for_management,
    update_managed_user,
)
from Back_end.access.states.auth_state import AuthState


UserRow = dict[str, str | int | bool]


class UserManagementState(AuthState):
    """Estado da tela de gerenciamento de usuários."""

    users: list[UserRow] = []

    loading: bool = False
    saving: bool = False

    user_error_message: str = ""
    user_success_message: str = ""

    search_text: str = ""
    role_filter: str = "all"
    status_filter: str = "all"

    editor_open: bool = False
    editor_mode: str = "create"
    editing_user_id: int | None = None

    form_name: str = ""
    form_email: str = ""
    form_password: str = ""
    form_role: str = UserRole.USER.value
    form_status: str = "active"

    delete_confirm_open: bool = False
    delete_user_id: int | None = None
    delete_user_name: str = ""

    # ========================================================
    # HELPERS
    # ========================================================

    def _actor_user_id(self) -> int:
        actor_user_id = validate_session(
            self.session_token
        )

        if actor_user_id is None:
            raise PermissionError(
                "Sua sessão expirou. Entre novamente."
            )

        return actor_user_id

    @staticmethod
    def _serialize_user(user) -> UserRow:
        name = str(user.name or "").strip()

        initials = "".join(
            part[0].upper()
            for part in name.split()
            if part
        )[:2]

        if not initials:
            initials = "U"

        return {
            "id": int(user.id or 0),
            "name": name,
            "email": str(user.email or ""),
            "role": str(user.role or UserRole.USER.value),
            "role_label": get_role_label(user.role),
            "is_active": bool(user.is_active),
            "initials": initials,
        }

    def _reload_users(self) -> None:
        actor_user_id = self._actor_user_id()

        users = list_users_for_management(
            actor_user_id
        )

        self.users = [
            self._serialize_user(user)
            for user in users
        ]

    def _clear_editor(self) -> None:
        self.editor_mode = "create"
        self.editing_user_id = None

        self.form_name = ""
        self.form_email = ""
        self.form_password = ""
        self.form_role = UserRole.USER.value
        self.form_status = "active"

    def _clear_delete_confirmation(self) -> None:
        self.delete_confirm_open = False
        self.delete_user_id = None
        self.delete_user_name = ""

    # ========================================================
    # COMPUTED VARS
    # ========================================================

    @rx.var
    def filtered_users(self) -> list[UserRow]:
        query = self.search_text.strip().casefold()

        result: list[UserRow] = []

        for user in self.users:
            name = str(user["name"]).casefold()
            email = str(user["email"]).casefold()
            role = str(user["role"])
            is_active = bool(user["is_active"])

            if (
                query
                and query not in name
                and query not in email
            ):
                continue

            if (
                self.role_filter != "all"
                and role != self.role_filter
            ):
                continue

            if (
                self.status_filter == "active"
                and not is_active
            ):
                continue

            if (
                self.status_filter == "inactive"
                and is_active
            ):
                continue

            result.append(user)

        return result

    @rx.var
    def total_users(self) -> int:
        return len(self.users)

    @rx.var
    def active_users(self) -> int:
        return sum(
            1
            for user in self.users
            if bool(user["is_active"])
        )

    @rx.var
    def inactive_users(self) -> int:
        return sum(
            1
            for user in self.users
            if not bool(user["is_active"])
        )

    @rx.var
    def administrator_users(self) -> int:
        return sum(
            1
            for user in self.users
            if str(user["role"])
            in {
                UserRole.SUPERADMIN.value,
                UserRole.ADMIN.value,
            }
        )

    @rx.var
    def result_count(self) -> int:
        return len(self.filtered_users)

    @rx.var
    def editor_title(self) -> str:
        if self.editor_mode == "edit":
            return "Editar usuário"

        return "Novo usuário"

    @rx.var
    def editor_submit_label(self) -> str:
        if self.editor_mode == "edit":
            return "Salvar alterações"

        return "Criar usuário"

    @rx.var
    def password_label(self) -> str:
        if self.editor_mode == "edit":
            return "Nova senha (opcional)"

        return "Senha inicial"

    # ========================================================
    # CARREGAMENTO
    # ========================================================

    @rx.event
    def load_users(self):
        self.loading = True
        self.user_error_message = ""

        yield

        try:
            self._reload_users()

        except PermissionError as error:
            self.user_error_message = str(error)

        except Exception as error:
            print(
                "Erro ao carregar usuários: "
                f"{error}"
            )

            self.user_error_message = (
                "Não foi possível carregar os usuários."
            )

        finally:
            self.loading = False

    # ========================================================
    # FILTROS
    # ========================================================

    @rx.event
    def update_search_text(
        self,
        value: str,
    ):
        self.search_text = value

    @rx.event
    def update_role_filter(
        self,
        value: str,
    ):
        self.role_filter = value

    @rx.event
    def update_status_filter(
        self,
        value: str,
    ):
        self.status_filter = value

    @rx.event
    def clear_filters(self):
        self.search_text = ""
        self.role_filter = "all"
        self.status_filter = "all"

    # ========================================================
    # FORMULÁRIO
    # ========================================================

    @rx.event
    def update_form_name(
        self,
        value: str,
    ):
        self.form_name = value

    @rx.event
    def update_form_email(
        self,
        value: str,
    ):
        self.form_email = value

    @rx.event
    def update_form_password(
        self,
        value: str,
    ):
        self.form_password = value

    @rx.event
    def update_form_role(
        self,
        value: str,
    ):
        self.form_role = value

    @rx.event
    def update_form_status(
        self,
        value: str,
    ):
        self.form_status = value

    @rx.event
    def open_create(self):
        self.user_error_message = ""
        self.user_success_message = ""

        self._clear_editor()

        self.editor_mode = "create"
        self.editor_open = True

    @rx.event
    def open_edit(
        self,
        user_id: int,
    ):
        self.user_error_message = ""
        self.user_success_message = ""

        user = next(
            (
                item
                for item in self.users
                if int(item["id"]) == user_id
            ),
            None,
        )

        if user is None:
            self.user_error_message = (
                "Usuário não encontrado."
            )
            return

        if user_id == self.current_user_id:
            self.user_error_message = (
                "Sua própria conta deve ser alterada pelo menu Perfil."
            )
            return

        if (
            str(user["role"])
            == UserRole.SUPERADMIN.value
            and self.current_user_role
            != UserRole.SUPERADMIN.value
        ):
            self.user_error_message = (
                "Admin não pode alterar uma conta SuperAdmin."
            )
            return

        self.editor_mode = "edit"
        self.editing_user_id = user_id

        self.form_name = str(user["name"])
        self.form_email = str(user["email"])
        self.form_password = ""
        self.form_role = str(user["role"])
        self.form_status = (
            "active"
            if bool(user["is_active"])
            else "inactive"
        )

        self.editor_open = True

    @rx.event
    def close_editor(self):
        self.editor_open = False
        self._clear_editor()

    @rx.event
    def save_user(self):
        self.saving = True
        self.user_error_message = ""
        self.user_success_message = ""

        yield

        try:
            actor_user_id = self._actor_user_id()

            is_active = (
                self.form_status == "active"
            )

            if self.editor_mode == "create":
                target_name = self.form_name.strip()
                target_email = self.form_email.strip()
                target_role = self.form_role

                create_managed_user(
                    actor_user_id=actor_user_id,
                    name=self.form_name,
                    email=self.form_email,
                    password=self.form_password,
                    role=self.form_role,
                    is_active=is_active,
                )

                self._audit(
                    action="USER_CREATED",
                    entity_type="user",
                    entity_id=target_email,
                    description=(
                        f"Usuário {target_name} "
                        f"({target_email}) criado como "
                        f"{get_role_label(target_role)}, "
                        f"status "
                        f"{'ativo' if is_active else 'inativo'}."
                    ),
                )

                self.user_success_message = (
                    "Usuário criado com sucesso."
                )

            else:
                if self.editing_user_id is None:
                    raise ValueError(
                        "Nenhum usuário foi selecionado para edição."
                    )

                target_user_id = self.editing_user_id

                previous_user = next(
                    (
                        item
                        for item in self.users
                        if int(item["id"])
                        == target_user_id
                    ),
                    None,
                )

                if previous_user is None:
                    raise ValueError(
                        "Usuário não encontrado."
                    )

                previous_name = str(
                    previous_user["name"]
                )
                previous_email = str(
                    previous_user["email"]
                )
                previous_role = str(
                    previous_user["role"]
                )
                previous_active = bool(
                    previous_user["is_active"]
                )

                new_name = self.form_name.strip()
                new_email = self.form_email.strip()
                new_role = self.form_role
                password_changed = bool(
                    self.form_password
                )

                update_managed_user(
                    actor_user_id=actor_user_id,
                    target_user_id=target_user_id,
                    name=self.form_name,
                    email=self.form_email,
                    role=self.form_role,
                    is_active=is_active,
                    password=self.form_password,
                )

                general_changes: list[str] = []

                if previous_name != new_name:
                    general_changes.append(
                        "nome alterado"
                    )

                if (
                    previous_email.casefold()
                    != new_email.casefold()
                ):
                    general_changes.append(
                        "e-mail alterado"
                    )

                if password_changed:
                    general_changes.append(
                        "senha alterada"
                    )

                if general_changes:
                    self._audit(
                        action="USER_UPDATED",
                        entity_type="user",
                        entity_id=target_user_id,
                        description=(
                            f"Dados do usuário "
                            f"{new_name} ({new_email}) "
                            f"atualizados: "
                            f"{', '.join(general_changes)}."
                        ),
                    )

                if previous_role != new_role:
                    self._audit(
                        action="USER_ROLE_CHANGED",
                        entity_type="user",
                        entity_id=target_user_id,
                        description=(
                            f"Perfil de {new_name} "
                            f"({new_email}) alterado de "
                            f"{get_role_label(previous_role)} "
                            f"para "
                            f"{get_role_label(new_role)}."
                        ),
                    )

                if previous_active != is_active:
                    self._audit(
                        action=(
                            "USER_ENABLED"
                            if is_active
                            else "USER_DISABLED"
                        ),
                        entity_type="user",
                        entity_id=target_user_id,
                        description=(
                            f"Usuário {new_name} "
                            f"({new_email}) "
                            f"{'ativado' if is_active else 'desativado'}."
                        ),
                    )

                self.user_success_message = (
                    "Usuário atualizado com sucesso."
                )

            self.editor_open = False
            self._clear_editor()
            self._reload_users()

        except (ValueError, PermissionError) as error:
            self.user_error_message = str(error)

        except Exception as error:
            print(
                "Erro ao salvar usuário: "
                f"{error}"
            )

            self.user_error_message = (
                "Não foi possível salvar o usuário."
            )

        finally:
            self.saving = False

    # ========================================================
    # EXCLUSÃO
    # ========================================================

    @rx.event
    def request_delete(
        self,
        user_id: int,
    ):
        self.user_error_message = ""
        self.user_success_message = ""

        user = next(
            (
                item
                for item in self.users
                if int(item["id"]) == user_id
            ),
            None,
        )

        if user is None:
            self.user_error_message = (
                "Usuário não encontrado."
            )
            return

        if user_id == self.current_user_id:
            self.user_error_message = (
                "Você não pode excluir a própria conta."
            )
            return

        self.delete_user_id = user_id
        self.delete_user_name = str(
            user["name"]
        )
        self.delete_confirm_open = True

    @rx.event
    def cancel_delete(self):
        self._clear_delete_confirmation()

    @rx.event
    def confirm_delete(self):
        if self.delete_user_id is None:
            return

        self.saving = True
        self.user_error_message = ""
        self.user_success_message = ""

        yield

        try:
            actor_user_id = self._actor_user_id()

            target_user_id = self.delete_user_id

            target_user = next(
                (
                    item
                    for item in self.users
                    if int(item["id"])
                    == target_user_id
                ),
                None,
            )

            if target_user is None:
                raise ValueError(
                    "Usuário não encontrado."
                )

            target_name = str(
                target_user["name"]
            )
            target_email = str(
                target_user["email"]
            )
            target_role = str(
                target_user["role"]
            )

            delete_managed_user(
                actor_user_id=actor_user_id,
                target_user_id=target_user_id,
            )

            self._audit(
                action="USER_DELETED",
                entity_type="user",
                entity_id=target_user_id,
                description=(
                    f"Usuário {target_name} "
                    f"({target_email}), perfil "
                    f"{get_role_label(target_role)}, "
                    "foi excluído."
                ),
            )

            self.user_success_message = (
                "Usuário excluído com sucesso."
            )

            self._clear_delete_confirmation()
            self._reload_users()

        except (ValueError, PermissionError) as error:
            self.user_error_message = str(error)

        except Exception as error:
            print(
                "Erro ao excluir usuário: "
                f"{error}"
            )

            self.user_error_message = (
                "Não foi possível excluir o usuário."
            )

        finally:
            self.saving = False

    # ========================================================
    # MENSAGENS
    # ========================================================

    @rx.event
    def clear_user_error_message(self):
        self.user_error_message = ""

    @rx.event
    def clear_user_success_message(self):
        self.user_success_message = ""
