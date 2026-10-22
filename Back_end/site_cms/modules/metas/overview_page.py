import reflex as rx

from Back_end.interface.layouts.admin_layout import (
    admin_layout,
)
from Back_end.interface.theme.semantic import (
    BORDER,
    SURFACE,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)
from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
    FONT_FAMILY_SECUNDARY,
)
from Back_end.site_cms.modules.metas.overview_state import (
    MetaOverviewCmsState,
)


def _field_label(
    label: str,
) -> rx.Component:
    return rx.text(
        label,
        color=TEXT_PRIMARY,
        font_family=(
            FONT_FAMILY_PRIMARY
        ),
        font_size="0.76rem",
        font_weight="600",
    )


def _budget_axis_row(
    item,
    index,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    "Eixo ",
                    index + 1,
                    color=TEXT_PRIMARY,
                    font_weight="700",
                    font_size="0.8rem",
                ),
                rx.spacer(),
                rx.cond(
                    MetaOverviewCmsState
                    .budget_source
                    == "cms",
                    rx.button(
                        rx.icon(
                            tag="trash_2",
                            size=13,
                        ),
                        "Remover",
                        size="1",
                        variant="soft",
                        color_scheme="red",
                        on_click=lambda: (
                            MetaOverviewCmsState
                            .remove_axis(
                                index
                            )
                        ),
                    ),
                    rx.box(),
                ),
                width="100%",
                align="center",
            ),

            rx.grid(
                rx.vstack(
                    _field_label(
                        "Nome"
                    ),
                    rx.input(
                        value=item["name"],
                        on_change=lambda value: (
                            MetaOverviewCmsState
                            .update_axis_field(
                                index,
                                "name",
                                value,
                            )
                        ),
                        disabled=(
                            MetaOverviewCmsState
                            .budget_source
                            != "cms"
                        ),
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),

                rx.vstack(
                    _field_label(
                        "Cor"
                    ),
                    rx.input(
                        value=item["color"],
                        on_change=lambda value: (
                            MetaOverviewCmsState
                            .update_axis_field(
                                index,
                                "color",
                                value,
                            )
                        ),
                        disabled=(
                            MetaOverviewCmsState
                            .budget_source
                            != "cms"
                        ),
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),

                rx.vstack(
                    _field_label(
                        "Quantidade de metas"
                    ),
                    rx.input(
                        value=item[
                            "meta_count"
                        ],
                        on_change=lambda value: (
                            MetaOverviewCmsState
                            .update_axis_field(
                                index,
                                "meta_count",
                                value,
                            )
                        ),
                        disabled=(
                            MetaOverviewCmsState
                            .budget_source
                            != "cms"
                        ),
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),

                rx.vstack(
                    _field_label(
                        "Orçamento"
                    ),
                    rx.input(
                        value=item["budget"],
                        on_change=lambda value: (
                            MetaOverviewCmsState
                            .update_axis_field(
                                index,
                                "budget",
                                value,
                            )
                        ),
                        disabled=(
                            MetaOverviewCmsState
                            .budget_source
                            != "cms"
                        ),
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),

                columns={
                    "initial": "1",
                    "md": "2",
                    "xl": "4",
                },
                spacing="3",
                width="100%",
            ),

            spacing="3",
            width="100%",
            align="stretch",
        ),
        padding="0.9rem",
        border=f"1px solid {BORDER}",
        border_radius="9px",
        width="100%",
    )


def _know_item(
    item,
    index,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    "Card ",
                    index + 1,
                    color=TEXT_PRIMARY,
                    font_weight="700",
                    font_size="0.8rem",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon(
                        tag="trash_2",
                        size=13,
                    ),
                    "Remover",
                    size="1",
                    variant="soft",
                    color_scheme="red",
                    on_click=lambda: (
                        MetaOverviewCmsState
                        .remove_know_item(
                            index
                        )
                    ),
                ),
                width="100%",
                align="center",
            ),

            rx.grid(
                rx.vstack(
                    _field_label(
                        "Nome"
                    ),
                    rx.input(
                        value=item["name"],
                        on_change=lambda value: (
                            MetaOverviewCmsState
                            .update_know_item(
                                index,
                                "name",
                                value,
                            )
                        ),
                        placeholder=(
                            "Ex.: Metas atingidas"
                        ),
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),

                rx.vstack(
                    _field_label(
                        "Valor"
                    ),
                    rx.input(
                        value=item["value"],
                        on_change=lambda value: (
                            MetaOverviewCmsState
                            .update_know_item(
                                index,
                                "value",
                                value,
                            )
                        ),
                        placeholder=(
                            "Ex.: 19 ou 93%"
                        ),
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),

                rx.vstack(
                    _field_label(
                        "Ordem"
                    ),
                    rx.input(
                        value=item["order"],
                        on_change=lambda value: (
                            MetaOverviewCmsState
                            .update_know_item(
                                index,
                                "order",
                                value,
                            )
                        ),
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),

                columns={
                    "initial": "1",
                    "md": "3",
                },
                spacing="3",
                width="100%",
            ),

            spacing="3",
            width="100%",
            align="stretch",
        ),
        padding="0.9rem",
        border=f"1px solid {BORDER}",
        border_radius="9px",
        width="100%",
    )


def _budget_card() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading(
                        "Orçamento Geral",
                        size="5",
                        color=TEXT_PRIMARY,
                        font_family=(
                            FONT_FAMILY_SECUNDARY
                        ),
                    ),
                    rx.text(
                        (
                            "Consolidado automaticamente a partir "
                            "do orçamento das Metas sincronizadas."
                        ),
                        color=TEXT_SECONDARY,
                        font_size="0.74rem",
                    ),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                rx.badge(
                    MetaOverviewCmsState
                    .source_label,
                    variant="soft",
                    color_scheme=rx.cond(
                        MetaOverviewCmsState
                        .budget_source
                        == "smae",
                        "blue",
                        rx.cond(
                            MetaOverviewCmsState
                            .budget_source
                            == "legacy",
                            "gray",
                            "orange",
                        ),
                    ),
                ),
                width="100%",
                align="center",
            ),

            rx.cond(
                MetaOverviewCmsState
                .budget_update_available,
                rx.callout(
                    (
                        "O SMAE possui novos valores orçamentários. "
                        "O orçamento personalizado foi preservado."
                    ),
                    icon="refresh_cw",
                    color_scheme="orange",
                    width="100%",
                ),
                rx.box(),
            ),

            rx.hstack(
                rx.cond(
                    MetaOverviewCmsState
                    .budget_source
                    != "cms",
                    rx.button(
                        "Personalizar orçamento",
                        size="2",
                        variant="soft",
                        on_click=(
                            MetaOverviewCmsState
                            .enable_budget_override
                        ),
                    ),
                    rx.button(
                        rx.icon(
                            tag="refresh_ccw",
                            size=13,
                        ),
                        "Voltar ao automático",
                        size="2",
                        variant="soft",
                        on_click=(
                            MetaOverviewCmsState
                            .use_automatic_budget
                        ),
                    ),
                ),
                rx.spacer(),
                rx.cond(
                    MetaOverviewCmsState
                    .budget_source
                    == "cms",
                    rx.button(
                        rx.icon(
                            tag="plus",
                            size=13,
                        ),
                        "Adicionar eixo",
                        size="2",
                        variant="soft",
                        on_click=(
                            MetaOverviewCmsState
                            .add_axis
                        ),
                    ),
                    rx.box(),
                ),
                width="100%",
                align="center",
                wrap="wrap",
            ),

            rx.grid(
                rx.vstack(
                    _field_label(
                        "Orçamento total"
                    ),
                    rx.input(
                        value=(
                            MetaOverviewCmsState
                            .total_budget
                        ),
                        on_change=(
                            MetaOverviewCmsState
                            .set_total_budget
                        ),
                        disabled=(
                            MetaOverviewCmsState
                            .budget_source
                            != "cms"
                        ),
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),

                rx.vstack(
                    _field_label(
                        "Total de metas"
                    ),
                    rx.input(
                        value=(
                            MetaOverviewCmsState
                            .total_metas
                        ),
                        on_change=(
                            MetaOverviewCmsState
                            .set_total_metas
                        ),
                        disabled=(
                            MetaOverviewCmsState
                            .budget_source
                            != "cms"
                        ),
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),

                columns={
                    "initial": "1",
                    "md": "2",
                },
                spacing="3",
                width="100%",
            ),

            rx.vstack(
                rx.foreach(
                    MetaOverviewCmsState
                    .axes_budget,
                    _budget_axis_row,
                ),
                spacing="3",
                width="100%",
                align="stretch",
            ),

            spacing="4",
            width="100%",
            align="stretch",
        ),
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="12px",
        padding="1.2rem",
        width="100%",
    )


def _know_metas_card() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading(
                        "Conheça Metas",
                        size="5",
                        color=TEXT_PRIMARY,
                        font_family=(
                            FONT_FAMILY_SECUNDARY
                        ),
                    ),
                    rx.text(
                        (
                            "Cards editoriais totalmente manuais. "
                            "Nome, valor e ordem ficam sob controle do CMS."
                        ),
                        color=TEXT_SECONDARY,
                        font_size="0.74rem",
                    ),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon(
                        tag="plus",
                        size=13,
                    ),
                    "Adicionar card",
                    size="2",
                    variant="soft",
                    on_click=(
                        MetaOverviewCmsState
                        .add_know_item
                    ),
                ),
                width="100%",
                align="center",
            ),

            rx.vstack(
                _field_label(
                    "Título da seção"
                ),
                rx.input(
                    value=(
                        MetaOverviewCmsState
                        .know_title
                    ),
                    on_change=(
                        MetaOverviewCmsState
                        .set_know_title
                    ),
                    width="100%",
                ),
                spacing="1",
                width="100%",
            ),

            rx.vstack(
                rx.foreach(
                    MetaOverviewCmsState
                    .know_items,
                    _know_item,
                ),
                spacing="3",
                width="100%",
                align="stretch",
            ),

            spacing="4",
            width="100%",
            align="stretch",
        ),
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="12px",
        padding="1.2rem",
        width="100%",
    )


def _action_bar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.cond(
                MetaOverviewCmsState
                .error_message
                != "",
                rx.callout(
                    MetaOverviewCmsState
                    .error_message,
                    icon="triangle_alert",
                    color_scheme="red",
                    width="100%",
                ),
                rx.box(),
            ),

            rx.cond(
                MetaOverviewCmsState
                .success_message
                != "",
                rx.callout(
                    MetaOverviewCmsState
                    .success_message,
                    icon="circle_check",
                    color_scheme="green",
                    width="100%",
                ),
                rx.box(),
            ),

            rx.grid(
                rx.vstack(
                    _field_label(
                        "Nota da publicação"
                    ),
                    rx.input(
                        value=(
                            MetaOverviewCmsState
                            .publication_note
                        ),
                        on_change=(
                            MetaOverviewCmsState
                            .set_publication_note
                        ),
                        placeholder=(
                            "Ex.: atualização dos indicadores"
                        ),
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),

                rx.hstack(
                    rx.button(
                        rx.icon(
                            tag="save",
                            size=14,
                        ),
                        "Salvar rascunho",
                        variant="outline",
                        on_click=(
                            MetaOverviewCmsState
                            .save_draft
                        ),
                        disabled=(
                            ~MetaOverviewCmsState
                            .can_edit_content
                        ),
                    ),

                    rx.cond(
                        MetaOverviewCmsState
                        .can_publish_content,
                        rx.button(
                            rx.icon(
                                tag="send",
                                size=14,
                            ),
                            "Publicar",
                            background="#272361",
                            color="white",
                            on_click=(
                                MetaOverviewCmsState
                                .publish
                            ),
                        ),
                        rx.box(),
                    ),

                    spacing="2",
                    justify="end",
                    wrap="wrap",
                ),

                columns={
                    "initial": "1",
                    "lg": "2",
                },
                spacing="4",
                align_items="end",
                width="100%",
            ),

            spacing="3",
            width="100%",
            align="stretch",
        ),
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="12px",
        padding="1rem",
        width="100%",
    )


def overview_content() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.text(
                    "SITE / METAS",
                    color="#1281AA",
                    font_size="0.72rem",
                    font_weight="700",
                    letter_spacing="0.08em",
                ),
                rx.heading(
                    "Visão Geral",
                    size="7",
                    color=TEXT_PRIMARY,
                    font_family=(
                        FONT_FAMILY_SECUNDARY
                    ),
                ),
                rx.text(
                    (
                        "Orçamento automático do SMAE e cards "
                        "editoriais de Conheça Metas."
                    ),
                    color=TEXT_SECONDARY,
                    font_family=(
                        FONT_FAMILY_PRIMARY
                    ),
                    font_size="0.84rem",
                ),
                spacing="2",
                align="start",
            ),
            rx.spacer(),
            rx.badge(
                MetaOverviewCmsState
                .status_label,
                color_scheme=rx.cond(
                    MetaOverviewCmsState
                    .status_label
                    == "Publicado",
                    "green",
                    "orange",
                ),
                variant="soft",
            ),
            width="100%",
            align="start",
        ),

        rx.hstack(
            rx.link(
                rx.button(
                    rx.icon(
                        tag="arrow_left",
                        size=14,
                    ),
                    "Metas",
                    variant="outline",
                ),
                href="/admin/site/metas",
                text_decoration="none",
            ),
            width="100%",
        ),

        rx.cond(
            MetaOverviewCmsState.loading,
            rx.center(
                rx.spinner(
                    size="3"
                ),
                min_height="300px",
                width="100%",
            ),
            rx.vstack(
                _budget_card(),
                _know_metas_card(),
                _action_bar(),
                spacing="4",
                width="100%",
                align="stretch",
            ),
        ),

        spacing="5",
        width="100%",
        max_width="1180px",
        margin="0 auto",
        padding_bottom="5rem",
        align="stretch",
    )


def meta_overview_cms_page() -> rx.Component:
    return admin_layout(
        overview_content()
    )
