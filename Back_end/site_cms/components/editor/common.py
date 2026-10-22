import reflex as rx

from Back_end.site_cms.state.section_editor_state import (
    SectionEditorState,
)


TEXT_PRIMARY = rx.color_mode_cond(
    "#1B263B",
    "#F4F7FF",
)

TEXT_MUTED = rx.color_mode_cond(
    "#6C7890",
    "#B8C4DA",
)

CARD_BG = rx.color_mode_cond(
    "#FFFFFF",
    "#18243E",
)

CARD_BORDER = rx.color_mode_cond(
    "rgba(22, 37, 63, 0.10)",
    "rgba(255, 255, 255, 0.10)",
)

SOFT_BG = rx.color_mode_cond(
    "#F7F9FC",
    "#111A2E",
)


def field_label(
    label: str,
    help_text: str = "",
) -> rx.Component:
    return rx.vstack(
        rx.text(
            label,
            color=TEXT_PRIMARY,
            font_size="0.8rem",
            font_weight="600",
        ),
        rx.cond(
            help_text != "",
            rx.text(
                help_text,
                color=TEXT_MUTED,
                font_size="0.7rem",
            ),
            rx.box(),
        ),
        spacing="1",
        align="start",
    )


def text_field(
    *,
    label: str,
    value,
    on_change,
    placeholder: str = "",
    help_text: str = "",
    disabled=False,
) -> rx.Component:
    return rx.vstack(
        field_label(
            label,
            help_text,
        ),
        rx.input(
            value=value,
            on_change=on_change,
            placeholder=placeholder,
            width="100%",
            disabled=disabled,
        ),
        spacing="2",
        align="stretch",
        width="100%",
    )


def textarea_field(
    *,
    label: str,
    value,
    on_change,
    placeholder: str = "",
    help_text: str = "",
    min_height: str = "130px",
    disabled=False,
) -> rx.Component:
    return rx.vstack(
        field_label(
            label,
            help_text,
        ),
        rx.text_area(
            value=value,
            on_change=on_change,
            placeholder=placeholder,
            width="100%",
            min_height=min_height,
            resize="vertical",
            disabled=disabled,
        ),
        spacing="2",
        align="stretch",
        width="100%",
    )


def section_box(
    title: str,
    description: str,
    *children,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    title,
                    size="4",
                    color=TEXT_PRIMARY,
                ),
                rx.text(
                    description,
                    color=TEXT_MUTED,
                    font_size="0.78rem",
                    line_height="1.45",
                ),
                spacing="1",
                align="start",
            ),
            *children,
            spacing="4",
            align="stretch",
            width="100%",
        ),
        width="100%",
        padding="1rem",
        background=CARD_BG,
        border=f"1px solid {CARD_BORDER}",
        border_radius="12px",
    )


def action_bar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(
                    "Fluxo editorial",
                    color=TEXT_PRIMARY,
                    font_size="0.78rem",
                    font_weight="600",
                ),
                rx.text(
                    (
                        "Salve como rascunho, revise no preview "
                        "e publique quando estiver pronto."
                    ),
                    color=TEXT_MUTED,
                    font_size="0.7rem",
                ),
                spacing="1",
                align="start",
            ),

            rx.spacer(),

            rx.button(
                rx.icon(
                    tag="save",
                    size=15,
                ),
                "Salvar rascunho",
                on_click=SectionEditorState.save_draft,
                loading=SectionEditorState.saving,
                disabled=rx.cond(
                    SectionEditorState.can_edit_content,
                    False,
                    True,
                ),
                variant="soft",
            ),

            rx.button(
                rx.icon(
                    tag="eye",
                    size=15,
                ),
                "Preview",
                on_click=SectionEditorState.open_preview,
                variant="soft",
            ),

            rx.cond(
                SectionEditorState.can_publish_content,
                rx.button(
                    rx.icon(
                        tag="send",
                        size=15,
                    ),
                    "Publicar",
                    on_click=SectionEditorState.publish,
                    loading=SectionEditorState.publishing,
                    background="#272361",
                    color="#FFFFFF",
                    _hover={
                        "background": "#124E8A",
                    },
                ),
                rx.box(),
            ),

            width="100%",
            align="center",
            spacing="3",
            wrap="wrap",
        ),
        position="sticky",
        bottom="0",
        z_index="5",
        width="100%",
        padding="0.85rem 1rem",
        background=rx.color_mode_cond(
            "rgba(255, 255, 255, 0.96)",
            "rgba(24, 36, 62, 0.96)",
        ),
        border=f"1px solid {CARD_BORDER}",
        border_radius="12px",
        backdrop_filter="blur(8px)",
    )


def messages() -> rx.Component:
    return rx.vstack(
        rx.cond(
            SectionEditorState.error_message != "",
            rx.box(
                rx.hstack(
                    rx.icon(
                        tag="triangle_alert",
                        size=16,
                        color="#C62828",
                    ),
                    rx.text(
                        SectionEditorState.error_message,
                        color="#C62828",
                        font_size="0.8rem",
                    ),
                    spacing="3",
                    align="center",
                ),
                width="100%",
                padding="0.75rem 0.9rem",
                background="rgba(198, 40, 40, 0.08)",
                border_radius="9px",
            ),
            rx.box(),
        ),

        rx.cond(
            SectionEditorState.success_message != "",
            rx.box(
                rx.hstack(
                    rx.icon(
                        tag="circle_check",
                        size=16,
                        color="#288140",
                    ),
                    rx.text(
                        SectionEditorState.success_message,
                        color="#288140",
                        font_size="0.8rem",
                    ),
                    spacing="3",
                    align="center",
                ),
                width="100%",
                padding="0.75rem 0.9rem",
                background="rgba(40, 129, 64, 0.08)",
                border_radius="9px",
            ),
            rx.box(),
        ),

        spacing="2",
        width="100%",
    )


def version_history() -> rx.Component:
    def version_row(version):
        return rx.hstack(
            rx.box(
                rx.text(
                    "v",
                    version["number"],
                    font_size="0.72rem",
                    font_weight="700",
                    color="#1281AA",
                ),
                width="38px",
            ),
            rx.vstack(
                rx.text(
                    version["note"],
                    color=TEXT_PRIMARY,
                    font_size="0.76rem",
                ),
                rx.text(
                    version["published_at"],
                    color=TEXT_MUTED,
                    font_size="0.68rem",
                ),
                spacing="1",
                align="start",
                flex="1",
            ),
            rx.cond(
                SectionEditorState.can_edit_content,
                rx.button(
                    "Restaurar",
                    size="1",
                    variant="soft",
                    on_click=lambda: (
                        SectionEditorState.restore_version(
                            version["number"]
                        )
                    ),
                ),
                rx.box(),
            ),
            width="100%",
            align="center",
            spacing="2",
        )

    return section_box(
        "Histórico de versões",
        (
            "Restaurar traz uma versão antiga para o rascunho. "
            "Ela só volta ao site depois de uma nova publicação."
        ),
        rx.vstack(
            rx.foreach(
                SectionEditorState.versions,
                version_row,
            ),
            spacing="3",
            width="100%",
            align="stretch",
        ),
    )


def publication_note() -> rx.Component:
    return rx.cond(
        SectionEditorState.can_publish_content,
        section_box(
            "Nota da publicação",
            (
                "Opcional. Ajuda a identificar o motivo da alteração "
                "no histórico."
            ),
            rx.input(
                value=SectionEditorState.publication_note,
                on_change=SectionEditorState.set_publication_note,
                placeholder=(
                    "Ex.: atualização de texto aprovada pela equipe"
                ),
                width="100%",
            ),
        ),
        rx.box(),
    )


def media_notice() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon(
                tag="image",
                size=16,
                color="#1281AA",
            ),
            rx.text(
                (
                    "Os campos de mídia continuam preservando a referência atual. "
                    "Upload e biblioteca de imagens serão conectados ao módulo "
                    "de mídia depois, sem refazer estes editores."
                ),
                color=TEXT_MUTED,
                font_size="0.75rem",
                line_height="1.4",
            ),
            spacing="3",
            align="start",
        ),
        width="100%",
        padding="0.75rem 0.9rem",
        background=SOFT_BG,
        border_radius="9px",
    )
