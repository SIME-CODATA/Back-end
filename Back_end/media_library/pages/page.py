import reflex as rx

from Back_end.interface.layouts.admin_layout import admin_layout
from Back_end.interface.theme.semantic import ( BORDER, SURFACE, TEXT_PRIMARY, TEXT_SECONDARY, )
from Back_end.interface.theme.typography import ( FONT_FAMILY_PRIMARY, FONT_FAMILY_SECUNDARY, )
from Back_end.media_library.state.state import MediaLibraryState


def folder_select(value, on_change, width="100%"):
    return rx.select.root(
        rx.select.trigger(width=width),
        rx.select.content(
            rx.select.item("Imagens", value="imagens"),
            rx.select.item("Logos", value="logos"),
            rx.select.item("Banners", value="banners"),
            rx.select.item("Ícones", value="icons"),
            rx.select.item("Outros", value="outros"),
            position="popper",
        ),
        value=value,
        on_change=on_change,
    )


def media_card(item):
    return rx.box(
        rx.vstack(
            rx.cond(
                item["media_type"] == "image",
                rx.image(
                    src=item["url"],
                    width="100%",
                    height="180px",
                    object_fit="contain",
                    border_radius="8px",
                    background=rx.color_mode_cond("#F7F9FC", "#101827"),
                ),
                rx.center(
                    rx.vstack(
                        rx.icon(tag="video", size=34, color="#1281AA"),
                        rx.text("Vídeo MP4", color=TEXT_SECONDARY),
                        align="center",
                    ),
                    height="180px",
                    width="100%",
                    background=rx.color_mode_cond("#EEF3F7", "#18233F"),
                    border_radius="8px",
                ),
            ),
            rx.hstack(
                rx.badge(item["folder_label"], variant="soft"),
                rx.badge(
                    rx.cond(
                        item["media_type"] == "image",
                        "Imagem",
                        "Vídeo",
                    ),
                    variant="soft",
                ),
                rx.spacer(),
                rx.text(
                    item["size_label"],
                    font_size="0.68rem",
                    color=TEXT_SECONDARY,
                ),
                width="100%",
            ),
            rx.text(
                item["name"],
                font_weight="700",
                color=TEXT_PRIMARY,
            ),
            rx.text(
                item["original_name"],
                font_size="0.68rem",
                color=TEXT_SECONDARY,
            ),
            rx.hstack(
                rx.link(
                    rx.button(
                        "Abrir",
                        size="1",
                        variant="soft",
                    ),
                    href=item["url"],
                    is_external=True,
                    text_decoration="none",
                ),
                rx.cond(
                    MediaLibraryState.can_edit_media,
                    rx.button(
                        "Editar",
                        size="1",
                        variant="soft",
                        on_click=lambda: MediaLibraryState.open_editor(
                            item["id"]
                        ),
                    ),
                    rx.box(),
                ),
                rx.spacer(),
                rx.cond(
                    MediaLibraryState.can_delete_media,
                    rx.button(
                        rx.icon(tag="trash_2", size=13),
                        size="1",
                        variant="ghost",
                        color_scheme="red",
                        on_click=lambda: MediaLibraryState.ask_delete(
                            item["id"],
                            item["name"],
                        ),
                    ),
                    rx.box(),
                ),
                width="100%",
            ),
            spacing="2",
            align="stretch",
        ),
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="12px",
        padding="0.75rem",
        width="100%",
    )


def upload_panel():
    return rx.cond(
        MediaLibraryState.can_add_media,
        rx.box(
            rx.vstack(
                rx.heading(
                    "Adicionar mídia",
                    size="4",
                    color=TEXT_PRIMARY,
                ),
                rx.text(
                    "Arquivo, nome/chave e pasta são obrigatórios.",
                    color=TEXT_SECONDARY,
                    font_size="0.74rem",
                ),
                rx.grid(
                    rx.vstack(
                        rx.text(
                            "Nome / chave *",
                            font_size="0.72rem",
                            font_weight="600",
                        ),
                        rx.input(
                            placeholder="Ex.: imagemHome",
                            value=MediaLibraryState.upload_name,
                            on_change=MediaLibraryState.set_upload_name,
                        ),
                        rx.text(
                            "Letras, números, ponto, hífen ou underline.",
                            color=TEXT_SECONDARY,
                            font_size="0.65rem",
                        ),
                        align="stretch",
                    ),
                    rx.vstack(
                        rx.text(
                            "Pasta *",
                            font_size="0.72rem",
                            font_weight="600",
                        ),
                        folder_select(
                            MediaLibraryState.upload_folder,
                            MediaLibraryState.set_upload_folder,
                        ),
                        align="stretch",
                    ),
                    columns={"initial": "1", "md": "2"},
                    spacing="3",
                    width="100%",
                ),
                rx.input(
                    placeholder="Texto alternativo / acessibilidade",
                    value=MediaLibraryState.upload_alt_text,
                    on_change=MediaLibraryState.set_upload_alt_text,
                ),
                rx.text_area(
                    placeholder="Descrição opcional",
                    value=MediaLibraryState.upload_description,
                    on_change=MediaLibraryState.set_upload_description,
                    min_height="80px",
                ),
                rx.upload(
                    rx.vstack(
                        rx.icon(
                            tag="cloud_upload",
                            size=28,
                            color="#1281AA",
                        ),
                        rx.text(
                            "Clique ou arraste um arquivo",
                            font_weight="600",
                        ),
                        rx.text(
                            "PNG, JPEG/JPG, SVG ou MP4",
                            font_size="0.7rem",
                            color=TEXT_SECONDARY,
                        ),
                        align="center",
                    ),
                    id="media_library_upload",
                    multiple=False,
                    width="100%",
                    padding="1.4rem",
                    border=f"1px dashed {BORDER}",
                    border_radius="10px",
                ),
                rx.button(
                    rx.cond(
                        MediaLibraryState.uploading,
                        "Enviando...",
                        "Enviar mídia",
                    ),
                    disabled=MediaLibraryState.uploading,
                    on_click=MediaLibraryState.upload_files(
                        rx.upload_files(
                            upload_id="media_library_upload"
                        )
                    ),
                    loading=MediaLibraryState.uploading,
                    background="#272361",
                    color="white",
                    align_self="end",
                ),
                spacing="3",
                align="stretch",
            ),
            background=SURFACE,
            border=f"1px solid {BORDER}",
            border_radius="12px",
            padding="1.1rem",
            width="100%",
        ),
        rx.box(),
    )


def editor_dialog():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Editar mídia"),
            rx.vstack(
                rx.input(
                    placeholder="Nome/chave",
                    value=MediaLibraryState.editing_name,
                    on_change=MediaLibraryState.set_editing_name,
                ),
                folder_select(
                    MediaLibraryState.editing_folder,
                    MediaLibraryState.set_editing_folder,
                ),
                rx.input(
                    placeholder="Texto alternativo",
                    value=MediaLibraryState.editing_alt_text,
                    on_change=MediaLibraryState.set_editing_alt_text,
                ),
                rx.text_area(
                    placeholder="Descrição",
                    value=MediaLibraryState.editing_description,
                    on_change=MediaLibraryState.set_editing_description,
                ),
                rx.hstack(
                    rx.spacer(),
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        on_click=MediaLibraryState.close_editor,
                    ),
                    rx.button(
                        "Salvar",
                        on_click=MediaLibraryState.save_editor,
                        loading=MediaLibraryState.saving,
                    ),
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            max_width="620px",
        ),
        open=MediaLibraryState.editor_open,
    )


def delete_dialog():
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title("Remover da biblioteca?"),
            rx.alert_dialog.description(
                "A exclusão é lógica. O arquivo físico será preservado "
                "para não quebrar conteúdo publicado."
            ),
            rx.text(
                MediaLibraryState.delete_asset_name,
                font_weight="600",
            ),
            rx.hstack(
                rx.spacer(),
                rx.button(
                    "Cancelar",
                    variant="soft",
                    on_click=MediaLibraryState.cancel_delete,
                ),
                rx.button(
                    "Remover",
                    color_scheme="red",
                    on_click=MediaLibraryState.confirm_delete,
                ),
                width="100%",
            ),
        ),
        open=MediaLibraryState.delete_confirm_open,
    )


def media_library_content():
    return rx.vstack(
        rx.vstack(
            rx.text(
                "CONTEÚDO",
                color="#1281AA",
                font_size="0.72rem",
                font_weight="700",
            ),
            rx.heading(
                "Banco de imagens e vídeos",
                size="7",
                color=TEXT_PRIMARY,
                font_family=FONT_FAMILY_SECUNDARY,
            ),
            rx.text(
                "Mídias reutilizáveis por qualquer módulo do CMS "
                "e pelo site público.",
                color=TEXT_SECONDARY,
                font_family=FONT_FAMILY_PRIMARY,
            ),
            align="start",
        ),
        rx.cond(
            MediaLibraryState.media_error_message != "",
            rx.callout(
                MediaLibraryState.media_error_message,
                icon="triangle_alert",
                color_scheme="red",
                width="100%",
            ),
            rx.box(),
        ),
        rx.cond(
            MediaLibraryState.media_success_message != "",
            rx.callout(
                MediaLibraryState.media_success_message,
                icon="circle_check",
                color_scheme="green",
                width="100%",
            ),
            rx.box(),
        ),
        upload_panel(),
        rx.hstack(
            rx.input(
                placeholder="Buscar...",
                value=MediaLibraryState.search_text,
                on_change=MediaLibraryState.set_search_text,
                max_width="360px",
            ),
            rx.select.root(
                rx.select.trigger(width="150px"),
                rx.select.content(
                    rx.select.item(
                        "Todos os tipos",
                        value="all",
                    ),
                    rx.select.item(
                        "Imagens",
                        value="image",
                    ),
                    rx.select.item(
                        "Vídeos",
                        value="video",
                    ),
                ),
                value=MediaLibraryState.media_type_filter,
                on_change=MediaLibraryState.set_media_type_filter,
            ),
            rx.select.root(
                rx.select.trigger(width="170px"),
                rx.select.content(
                    rx.select.item(
                        "Todas as pastas",
                        value="all",
                    ),
                    rx.select.item(
                        "Imagens",
                        value="imagens",
                    ),
                    rx.select.item(
                        "Logos",
                        value="logos",
                    ),
                    rx.select.item(
                        "Banners",
                        value="banners",
                    ),
                    rx.select.item(
                        "Ícones",
                        value="icons",
                    ),
                    rx.select.item(
                        "Outros",
                        value="outros",
                    ),
                ),
                value=MediaLibraryState.folder_filter,
                on_change=MediaLibraryState.set_folder_filter,
            ),
            spacing="3",
            wrap="wrap",
            width="100%",
        ),
        rx.cond(
            MediaLibraryState.loading,
            rx.center(
                rx.spinner(size="3"),
                min_height="220px",
                width="100%",
            ),
            rx.grid(
                rx.foreach(
                    MediaLibraryState.assets,
                    media_card,
                ),
                columns={
                    "initial": "1",
                    "md": "2",
                    "xl": "3",
                },
                spacing="4",
                width="100%",
            ),
        ),
        editor_dialog(),
        delete_dialog(),
        spacing="5",
        width="100%",
        max_width="1250px",
        margin="0 auto",
        padding_bottom="5rem",
        align="stretch",
    )


def media_library_page() -> rx.Component:
    return admin_layout(
        media_library_content()
    )
