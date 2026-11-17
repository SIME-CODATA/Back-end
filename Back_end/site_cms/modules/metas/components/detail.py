import reflex as rx

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
from Back_end.site_cms.modules.metas.components.common import (
    cms_card,
    field_header,
    source_badge,
    text_input,
    textarea_input,
)
from Back_end.site_cms.modules.metas.state import (
    MetaCmsState,
)


def meta_cms_breadcrumb() -> rx.Component:
    return rx.hstack(
        rx.link(
            "Site",
            href="/admin/site",
            text_decoration="none",
        ),
        rx.text(
            "/",
            color=TEXT_SECONDARY,
        ),
        rx.link(
            "Metas",
            href="/admin/site/metas",
            text_decoration="none",
        ),
        rx.text(
            "/",
            color=TEXT_SECONDARY,
        ),
        rx.text(
            "Meta ",
            MetaCmsState.meta_code,
            color=TEXT_SECONDARY,
        ),
        spacing="2",
        align="center",
        width="100%",
        font_size="0.76rem",
    )


def meta_cms_hero() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    "META",
                    color="#1281AA",
                    font_size="0.72rem",
                    font_weight="700",
                    letter_spacing="0.08em",
                ),
                source_badge(
                    MetaCmsState
                    .source_number
                ),
                rx.spacer(),
                rx.badge(
                    MetaCmsState
                    .status_label,
                    color_scheme=rx.cond(
                        MetaCmsState.has_draft,
                        "orange",
                        "green",
                    ),
                    variant="soft",
                ),
                width="100%",
                align="center",
            ),

            rx.grid(
                text_input(
                    label="Número",
                    source=(
                        MetaCmsState
                        .source_number
                    ),
                    field_key="number",
                    value=(
                        MetaCmsState.number
                    ),
                    on_change=(
                        MetaCmsState
                        .set_number
                    ),
                ),
                text_input(
                    label="Eixo",
                    source=(
                        MetaCmsState
                        .source_axis_name
                    ),
                    field_key="axis_name",
                    value=(
                        MetaCmsState
                        .axis_name
                    ),
                    on_change=(
                        MetaCmsState
                        .set_axis_name
                    ),
                ),
                columns={
                    "initial": "1",
                    "md": "2",
                },
                spacing="4",
                width="100%",
            ),

            textarea_input(
                label="Título completo",
                source=(
                    MetaCmsState
                    .source_title
                ),
                field_key="title",
                value=(
                    MetaCmsState.title
                ),
                on_change=(
                    MetaCmsState
                    .set_title
                ),
                min_height="110px",
            ),

            rx.grid(
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "Trecho destacado",
                            color=TEXT_PRIMARY,
                            font_size="0.78rem",
                            font_weight="600",
                        ),
                        source_badge(MetaCmsState.source_title_highlight),
                        spacing="2",
                    ),
                    rx.text_area(
                        value=MetaCmsState.title_highlight,
                        on_change=MetaCmsState.set_title_highlight,
                        min_height="90px",
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                    align="stretch",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "Complemento do título",
                            color=TEXT_PRIMARY,
                            font_size="0.78rem",
                            font_weight="600",
                        ),
                        source_badge(MetaCmsState.source_title_complement),
                        spacing="2",
                    ),
                    rx.text_area(
                        value=MetaCmsState.title_complement,
                        on_change=MetaCmsState.set_title_complement,
                        min_height="90px",
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                    align="stretch",
                ),
                columns={"initial": "1", "xl": "2"},
                spacing="4",
                width="100%",
            ),

            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.badge(
                            "META ",
                            MetaCmsState.number,
                            variant="solid",
                            color_scheme="green",
                        ),
                        rx.spacer(),
                        rx.badge(
                            MetaCmsState.monitoring,
                            variant="soft",
                            color_scheme="green",
                        ),
                        width="100%",
                    ),
                    rx.text(
                        MetaCmsState.title_highlight,
                        font_weight="800",
                        font_size="1rem",
                        color=rx.cond(
                            MetaCmsState.axis_primary_color != "",
                            MetaCmsState.axis_primary_color,
                            "#288140",
                        ),
                    ),
                    rx.text(
                        MetaCmsState.title_complement,
                        font_size="0.95rem",
                        color=TEXT_PRIMARY,
                    ),
                    spacing="2",
                    align="stretch",
                    width="100%",
                ),
                background="#F6FBF7",
                border=f"1px solid {BORDER}",
                border_radius="10px",
                padding="1rem",
                width="100%",
            ),

            spacing="4",
            align="stretch",
            width="100%",
        ),
        width="100%",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="12px",
        padding="1.4rem",
    )


def status_card() -> rx.Component:
    return cms_card(
        "Status e evolução",

        rx.vstack(
            field_header(
                "Monitoramento",
                MetaCmsState
                .source_monitoring,
                "monitoring",
            ),
            rx.select.root(
                rx.select.trigger(
                    placeholder=(
                        "Monitoramento"
                    ),
                    width="100%",
                ),
                rx.select.content(
                    rx.select.item(
                        "Planejamento",
                        value="planejamento",
                    ),
                    rx.select.item(
                        "Em progresso",
                        value="progresso",
                    ),
                    rx.select.item(
                        "Atingida",
                        value="atingida",
                    ),
                    position="popper",
                ),
                value=(
                    MetaCmsState.monitoring
                ),
                on_change=(
                    MetaCmsState
                    .set_monitoring
                ),
            ),
            spacing="2",
            width="100%",
            align="stretch",
        ),

        textarea_input(
            label="Evolução",
            source=(
                MetaCmsState
                .source_evolution
            ),
            field_key="evolution",
            value=(
                MetaCmsState.evolution
            ),
            on_change=(
                MetaCmsState
                .set_evolution
            ),
            min_height="180px",
        ),

        description=(
            "Mantém o desenho da ficha atual, "
            "mas os valores passam a ser editáveis."
        ),
    )


def classification_card() -> rx.Component:
    return cms_card(
        "Eixo e identidade visual",

        rx.grid(
            text_input(
                label="Cor principal",
                source=(
                    MetaCmsState
                    .source_axis_primary_color
                ),
                field_key=(
                    "axis_primary_color"
                ),
                value=(
                    MetaCmsState
                    .axis_primary_color
                ),
                on_change=(
                    MetaCmsState
                    .set_axis_primary_color
                ),
                placeholder="#1281AA",
            ),
            text_input(
                label="Cor secundária",
                source=(
                    MetaCmsState
                    .source_axis_secondary_color
                ),
                field_key=(
                    "axis_secondary_color"
                ),
                value=(
                    MetaCmsState
                    .axis_secondary_color
                ),
                on_change=(
                    MetaCmsState
                    .set_axis_secondary_color
                ),
                placeholder="#292561",
            ),
            columns={
                "initial": "1",
                "md": "2",
            },
            spacing="3",
            width="100%",
        ),

        textarea_input(
            label="Textos do eixo",
            source=(
                MetaCmsState
                .source_axis_phrases
            ),
            field_key="axis_phrases",
            value=(
                MetaCmsState
                .axis_phrases_text
            ),
            on_change=(
                MetaCmsState
                .set_axis_phrases_text
            ),
            placeholder=(
                "Um parágrafo por linha."
            ),
            min_height="160px",
        ),

        description=(
            "As cores e os textos continuam independentes "
            "e podem ser personalizados para o site."
        ),
    )


def projection_card() -> rx.Component:
    return cms_card(
        "Projeção e indicador",

        textarea_input(
            label="Projeção",
            source=(
                MetaCmsState
                .source_projection
            ),
            field_key="projection",
            value=(
                MetaCmsState
                .projection
            ),
            on_change=(
                MetaCmsState
                .set_projection
            ),
            min_height="180px",
        ),

        textarea_input(
            label="Indicador",
            source=(
                MetaCmsState
                .source_indicator
            ),
            field_key="indicator",
            value=(
                MetaCmsState
                .indicator
            ),
            on_change=(
                MetaCmsState
                .set_indicator
            ),
            min_height="110px",
        ),
    )


def agencies_card() -> rx.Component:
    return cms_card(
        "Órgãos responsáveis",

        textarea_input(
            label="Órgãos",
            source=(
                MetaCmsState
                .source_responsible_agencies
            ),
            field_key=(
                "responsible_agencies"
            ),
            value=(
                MetaCmsState
                .responsible_agencies_text
            ),
            on_change=(
                MetaCmsState
                .set_responsible_agencies_text
            ),
            placeholder=(
                "Uma sigla por linha."
            ),
            min_height="170px",
        ),

        description=(
            "O SMAE preenche inicialmente, mas o CMS "
            "pode manter uma versão editorial diferente."
        ),
    )


def _action_row(
    item,
    index,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    "Ação estratégica ",
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
                        MetaCmsState
                        .remove_action(
                            index
                        )
                    ),
                ),
                width="100%",
                align="center",
            ),

            rx.grid(
                rx.vstack(
                    rx.text(
                        "Número",
                        color=TEXT_SECONDARY,
                        font_size="0.72rem",
                    ),
                    rx.input(
                        value=item[
                            "number"
                        ],
                        on_change=lambda value: (
                            MetaCmsState
                            .update_action_field(
                                index,
                                "number",
                                value,
                            )
                        ),
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),

                rx.vstack(
                    rx.text(
                        "Situação",
                        color=TEXT_SECONDARY,
                        font_size="0.72rem",
                    ),
                    rx.select.root(
                        rx.select.trigger(
                            width="100%",
                        ),
                        rx.select.content(
                            rx.select.item(
                                "Em andamento",
                                value="false",
                            ),
                            rx.select.item(
                                "Concluída",
                                value="true",
                            ),
                            position="popper",
                        ),
                        value=item[
                            "completed"
                        ],
                        on_change=lambda value: (
                            MetaCmsState
                            .update_action_field(
                                index,
                                "completed",
                                value,
                            )
                        ),
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
                rx.text(
                    "Descrição",
                    color=TEXT_SECONDARY,
                    font_size="0.72rem",
                ),
                rx.text_area(
                    value=item[
                        "description"
                    ],
                    on_change=lambda value: (
                        MetaCmsState
                        .update_action_field(
                            index,
                            "description",
                            value,
                        )
                    ),
                    width="100%",
                    min_height="100px",
                ),
                spacing="1",
                width="100%",
            ),

            rx.grid(
                rx.vstack(
                    rx.text(
                        "Evolução em destaque",
                        color=TEXT_SECONDARY,
                        font_size="0.72rem",
                    ),
                    rx.input(
                        value=item[
                            "evolution_label"
                        ],
                        on_change=lambda value: (
                            MetaCmsState
                            .update_action_field(
                                index,
                                "evolution_label",
                                value,
                            )
                        ),
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),

                rx.vstack(
                    rx.text(
                        "Descrição da evolução",
                        color=TEXT_SECONDARY,
                        font_size="0.72rem",
                    ),
                    rx.text_area(
                        value=item[
                            "evolution_description"
                        ],
                        on_change=lambda value: (
                            MetaCmsState
                            .update_action_field(
                                index,
                                "evolution_description",
                                value,
                            )
                        ),
                        width="100%",
                        min_height="100px",
                    ),
                    spacing="1",
                    width="100%",
                ),

                columns={
                    "initial": "1",
                    "lg": "2",
                },
                spacing="3",
                width="100%",
            ),

            spacing="3",
            width="100%",
            align="stretch",
        ),
        padding="0.95rem",
        border=f"1px solid {BORDER}",
        border_radius="9px",
        width="100%",
    )


def initiatives_card() -> rx.Component:
    return cms_card(
        "Ações estratégicas",

        rx.hstack(
            source_badge(
                MetaCmsState
                .source_strategic_actions
            ),
            rx.spacer(),
            rx.button(
                rx.icon(
                    tag="plus",
                    size=14,
                ),
                "Adicionar ação",
                size="2",
                variant="soft",
                on_click=(
                    MetaCmsState.add_action
                ),
            ),
            width="100%",
            align="center",
        ),

        rx.vstack(
            rx.foreach(
                MetaCmsState
                .strategic_actions,
                _action_row,
            ),
            spacing="3",
            width="100%",
            align="stretch",
        ),

        description=(
            "A API antiga trouxe também evolução e situação "
            "das ações. Esses dados ficam preservados e editáveis."
        ),
    )


def _result_row(
    item,
    index,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    "Resultado ",
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
                        MetaCmsState
                        .remove_result(
                            index
                        )
                    ),
                ),
                width="100%",
                align="center",
            ),

            rx.grid(
                rx.input(
                    placeholder="Valor",
                    value=item["value"],
                    on_change=lambda value: (
                        MetaCmsState
                        .update_result_field(
                            index,
                            "value",
                            value,
                        )
                    ),
                ),
                rx.input(
                    placeholder="Mês",
                    value=item["month"],
                    on_change=lambda value: (
                        MetaCmsState
                        .update_result_field(
                            index,
                            "month",
                            value,
                        )
                    ),
                ),
                rx.input(
                    placeholder="Ano",
                    value=item["year"],
                    on_change=lambda value: (
                        MetaCmsState
                        .update_result_field(
                            index,
                            "year",
                            value,
                        )
                    ),
                ),
                rx.input(
                    placeholder="AAAA-MM-DD",
                    value=item["date"],
                    on_change=lambda value: (
                        MetaCmsState
                        .update_result_field(
                            index,
                            "date",
                            value,
                        )
                    ),
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
        padding="0.85rem",
        border=f"1px solid {BORDER}",
        border_radius="9px",
        width="100%",
    )


def results_card() -> rx.Component:
    return cms_card(
        "Resultados apurados",

        rx.hstack(
            source_badge(
                MetaCmsState
                .source_measured_results
            ),
            rx.spacer(),
            rx.button(
                rx.icon(
                    tag="plus",
                    size=14,
                ),
                "Adicionar resultado",
                size="2",
                variant="soft",
                on_click=(
                    MetaCmsState.add_result
                ),
            ),
            width="100%",
            align="center",
        ),

        rx.vstack(
            rx.foreach(
                MetaCmsState
                .measured_results,
                _result_row,
            ),
            spacing="3",
            width="100%",
            align="stretch",
        ),
    )


def _region_block(
    item,
    index,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    "Bloco ",
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
                        MetaCmsState
                        .remove_region_block(
                            index
                        )
                    ),
                ),
                width="100%",
                align="center",
            ),

            rx.grid(
                rx.input(
                    placeholder="Identificador",
                    value=item["key"],
                    on_change=lambda value: (
                        MetaCmsState
                        .update_region_block_field(
                            index,
                            "key",
                            value,
                        )
                    ),
                ),
                rx.input(
                    placeholder="Título",
                    value=item["title"],
                    on_change=lambda value: (
                        MetaCmsState
                        .update_region_block_field(
                            index,
                            "title",
                            value,
                        )
                    ),
                ),
                columns={
                    "initial": "1",
                    "md": "2",
                },
                spacing="3",
                width="100%",
            ),

            rx.vstack(
                rx.text(
                    "Imagem",
                    color=TEXT_SECONDARY,
                    font_size="0.72rem",
                ),
                rx.input(
                    value=item[
                        "image_url"
                    ],
                    on_change=lambda value: (
                        MetaCmsState
                        .update_region_block_field(
                            index,
                            "image_url",
                            value,
                        )
                    ),
                    placeholder=(
                        "Referência atual da imagem"
                    ),
                    width="100%",
                ),
                rx.text(
                    (
                        "O campo será trocado pelo Banco de Imagens "
                        "quando o módulo de mídia for conectado."
                    ),
                    color=TEXT_SECONDARY,
                    font_size="0.66rem",
                ),
                spacing="1",
                width="100%",
                align="stretch",
            ),

            rx.text_area(
                value=item["text"],
                on_change=lambda value: (
                    MetaCmsState
                    .update_region_block_field(
                        index,
                        "text",
                        value,
                    )
                ),
                placeholder="Texto / legenda",
                min_height="110px",
                width="100%",
            ),

            rx.text_area(
                value=item["footer"],
                on_change=lambda value: (
                    MetaCmsState
                    .update_region_block_field(
                        index,
                        "footer",
                        value,
                    )
                ),
                placeholder="Rodapé",
                min_height="90px",
                width="100%",
            ),

            spacing="3",
            width="100%",
            align="stretch",
        ),
        padding="0.95rem",
        border=f"1px solid {BORDER}",
        border_radius="9px",
        width="100%",
    )


def regionalization_card() -> rx.Component:
    return cms_card(
        "Regionalização",

        rx.hstack(
            source_badge(
                MetaCmsState
                .source_regionalization
            ),
            rx.spacer(),
            rx.button(
                rx.icon(
                    tag="plus",
                    size=14,
                ),
                "Adicionar bloco",
                size="2",
                variant="soft",
                on_click=(
                    MetaCmsState
                    .add_region_block
                ),
            ),
            width="100%",
            align="center",
        ),

        rx.vstack(
            rx.text(
                "Modo",
                color=TEXT_PRIMARY,
                font_size="0.78rem",
                font_weight="600",
            ),
            rx.select.root(
                rx.select.trigger(
                    width="100%",
                ),
                rx.select.content(
                    rx.select.item(
                        "Não regionalizável",
                        value=(
                            "not_regionalizable"
                        ),
                    ),
                    rx.select.item(
                        "Regionalização personalizada",
                        value="custom",
                    ),
                    position="popper",
                ),
                value=(
                    MetaCmsState
                    .regionalization_mode
                ),
                on_change=(
                    MetaCmsState
                    .set_regionalization_mode
                ),
            ),
            spacing="2",
            width="100%",
            align="stretch",
        ),

        rx.vstack(
            rx.text(
                "Nota",
                color=TEXT_PRIMARY,
                font_size="0.78rem",
                font_weight="600",
            ),
            rx.text_area(
                value=(
                    MetaCmsState
                    .regionalization_note
                ),
                on_change=(
                    MetaCmsState
                    .set_regionalization_note
                ),
                min_height="90px",
                width="100%",
            ),
            spacing="2",
            width="100%",
            align="stretch",
        ),

        rx.cond(
            MetaCmsState
            .regionalization_mode
            == "custom",
            rx.vstack(
                rx.foreach(
                    MetaCmsState
                    .regionalization_blocks,
                    _region_block,
                ),
                spacing="3",
                width="100%",
                align="stretch",
            ),
            rx.callout(
                (
                    "Esta Meta será publicada apenas como "
                    "\"não regionalizável\"."
                ),
                icon="map_pin_off",
                color_scheme="gray",
                width="100%",
            ),
        ),

        description=(
            "A regionalização deixa de ficar presa a três "
            "objetos fixos. Os blocos pertencem ao próprio CMS."
        ),
    )


def _work_row(item, index) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    "Obra ",
                    index + 1,
                    color=TEXT_PRIMARY,
                    font_weight="700",
                    font_size="0.8rem",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon(tag="trash_2", size=13),
                    "Remover",
                    size="1",
                    variant="soft",
                    color_scheme="red",
                    on_click=lambda: MetaCmsState.remove_work(index),
                ),
                width="100%",
                align="center",
            ),
            rx.grid(
                rx.input(
                    placeholder="Código",
                    value=item["code"],
                    on_change=lambda value: MetaCmsState.update_work_field(
                        index, "code", value
                    ),
                ),
                rx.input(
                    placeholder="Status",
                    value=item["status"],
                    on_change=lambda value: MetaCmsState.update_work_field(
                        index, "status", value
                    ),
                ),
                rx.input(
                    placeholder="Percentual concluído",
                    value=item["percent_complete"],
                    on_change=lambda value: MetaCmsState.update_work_field(
                        index, "percent_complete", value
                    ),
                ),
                columns={"initial": "1", "md": "3"},
                spacing="3",
                width="100%",
            ),
            rx.input(
                placeholder="Nome da obra/intervenção",
                value=item["name"],
                on_change=lambda value: MetaCmsState.update_work_field(
                    index, "name", value
                ),
                width="100%",
            ),
            rx.grid(
                rx.input(
                    placeholder="Tipo obra/intervenção",
                    value=item["intervention_type"],
                    on_change=lambda value: MetaCmsState.update_work_field(
                        index, "intervention_type", value
                    ),
                ),
                rx.input(
                    placeholder="Equipamento",
                    value=item["equipment"],
                    on_change=lambda value: MetaCmsState.update_work_field(
                        index, "equipment", value
                    ),
                ),
                columns={"initial": "1", "md": "2"},
                spacing="3",
                width="100%",
            ),
            rx.grid(
                rx.text_area(
                    placeholder="Subprefeituras, uma por linha",
                    value=item["subprefectures"],
                    on_change=lambda value: MetaCmsState.update_work_field(
                        index, "subprefectures", value
                    ),
                    min_height="80px",
                    width="100%",
                ),
                rx.text_area(
                    placeholder="Regiões, uma por linha",
                    value=item["regions"],
                    on_change=lambda value: MetaCmsState.update_work_field(
                        index, "regions", value
                    ),
                    min_height="80px",
                    width="100%",
                ),
                columns={"initial": "1", "md": "2"},
                spacing="3",
                width="100%",
            ),
            rx.grid(
                rx.input(
                    placeholder="Latitude",
                    value=item["latitude"],
                    on_change=lambda value: MetaCmsState.update_work_field(
                        index, "latitude", value
                    ),
                ),
                rx.input(
                    placeholder="Longitude",
                    value=item["longitude"],
                    on_change=lambda value: MetaCmsState.update_work_field(
                        index, "longitude", value
                    ),
                ),
                columns={"initial": "1", "md": "2"},
                spacing="3",
                width="100%",
            ),
            rx.input(
                placeholder="Endereço / referência geográfica",
                value=item["address"],
                on_change=lambda value: MetaCmsState.update_work_field(
                    index, "address", value
                ),
                width="100%",
            ),
            spacing="3",
            width="100%",
            align="stretch",
        ),
        padding="0.95rem",
        border=f"1px solid {BORDER}",
        border_radius="9px",
        width="100%",
    )


def associated_works_card() -> rx.Component:
    return cms_card(
        "Obras associadas",
        rx.hstack(
            source_badge(MetaCmsState.source_associated_works),
            rx.spacer(),
            rx.button(
                rx.icon(tag="plus", size=14),
                "Adicionar obra",
                size="2",
                variant="soft",
                on_click=MetaCmsState.add_work,
            ),
            width="100%",
            align="center",
        ),
        rx.vstack(
            rx.foreach(MetaCmsState.associated_works, _work_row),
            spacing="3",
            width="100%",
            align="stretch",
        ),
        description=(
            "Sincronizadas de /meta/relacionados e persistidas localmente. "
            "Qualquer edição aqui vira override do CMS e deixa de ser "
            "sobrescrita automaticamente pelo SMAE."
        ),
    )


def _project_row(item, index) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    "Projeto ", index + 1,
                    color=TEXT_PRIMARY,
                    font_weight="700",
                    font_size="0.8rem",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon(tag="trash_2", size=13),
                    "Remover",
                    size="1",
                    variant="soft",
                    color_scheme="red",
                    on_click=lambda: MetaCmsState.remove_project(index),
                ),
                width="100%",
            ),
            rx.grid(
                rx.input(
                    placeholder="Código",
                    value=item["code"],
                    on_change=lambda value: MetaCmsState.update_project_field(
                        index, "code", value
                    ),
                ),
                rx.input(
                    placeholder="Etapa",
                    value=item["stage"],
                    on_change=lambda value: MetaCmsState.update_project_field(
                        index, "stage", value
                    ),
                ),
                columns={"initial": "1", "md": "2"},
                spacing="3",
                width="100%",
            ),
            rx.input(
                placeholder="Nome do projeto",
                value=item["name"],
                on_change=lambda value: MetaCmsState.update_project_field(
                    index, "name", value
                ),
                width="100%",
            ),
            rx.input(
                placeholder="Portfólio",
                value=item["portfolio"],
                on_change=lambda value: MetaCmsState.update_project_field(
                    index, "portfolio", value
                ),
                width="100%",
            ),
            rx.grid(
                rx.input(
                    placeholder="Latitude",
                    value=item["latitude"],
                    on_change=lambda value: MetaCmsState.update_project_field(
                        index, "latitude", value
                    ),
                ),
                rx.input(
                    placeholder="Longitude",
                    value=item["longitude"],
                    on_change=lambda value: MetaCmsState.update_project_field(
                        index, "longitude", value
                    ),
                ),
                columns={"initial": "1", "md": "2"},
                spacing="3",
                width="100%",
            ),
            rx.input(
                placeholder="Endereço / referência geográfica",
                value=item["address"],
                on_change=lambda value: MetaCmsState.update_project_field(
                    index, "address", value
                ),
                width="100%",
            ),
            spacing="3",
            width="100%",
            align="stretch",
        ),
        padding="0.95rem",
        border=f"1px solid {BORDER}",
        border_radius="9px",
        width="100%",
    )


def associated_projects_card() -> rx.Component:
    return cms_card(
        "Projetos associados",
        rx.hstack(
            source_badge(MetaCmsState.source_associated_projects),
            rx.spacer(),
            rx.button(
                rx.icon(tag="plus", size=14),
                "Adicionar projeto",
                size="2",
                variant="soft",
                on_click=MetaCmsState.add_project,
            ),
            width="100%",
            align="center",
        ),
        rx.vstack(
            rx.foreach(MetaCmsState.associated_projects, _project_row),
            spacing="3",
            width="100%",
            align="stretch",
        ),
        description=(
            "Projetos vinculados no SMAE também entram no snapshot local e "
            "podem receber override editorial."
        ),
    )


def _extra_section_row(item, index) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    "Seção extra ",
                    index + 1,
                    color=TEXT_PRIMARY,
                    font_weight="700",
                    font_size="0.8rem",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon(tag="trash_2", size=13),
                    "Remover",
                    size="1",
                    variant="soft",
                    color_scheme="red",
                    on_click=lambda: MetaCmsState.remove_extra_section(index),
                ),
                width="100%",
            ),
            rx.input(
                placeholder="Título da seção",
                value=item["title"],
                on_change=lambda value: MetaCmsState.update_extra_section_field(
                    index, "title", value
                ),
                width="100%",
            ),
            rx.input(
                placeholder="Imagem opcional (URL / referência de mídia)",
                value=item["image_url"],
                on_change=lambda value: MetaCmsState.update_extra_section_field(
                    index, "image_url", value
                ),
                width="100%",
            ),
            rx.text_area(
                placeholder="Texto opcional",
                value=item["text"],
                on_change=lambda value: MetaCmsState.update_extra_section_field(
                    index, "text", value
                ),
                min_height="110px",
                width="100%",
            ),
            spacing="3",
            width="100%",
            align="stretch",
        ),
        padding="0.95rem",
        border=f"1px solid {BORDER}",
        border_radius="9px",
        width="100%",
    )


def extra_sections_card() -> rx.Component:
    return cms_card(
        "Seções extras opcionais",
        rx.hstack(
            rx.text(
                "Conteúdo que não existe no SMAE também pode entrar na ficha.",
                color=TEXT_SECONDARY,
                font_size="0.74rem",
            ),
            rx.spacer(),
            rx.button(
                rx.icon(tag="plus", size=14),
                "Adicionar seção",
                size="2",
                variant="soft",
                on_click=MetaCmsState.add_extra_section,
            ),
            width="100%",
            align="center",
        ),
        rx.vstack(
            rx.foreach(MetaCmsState.extra_sections, _extra_section_row),
            spacing="3",
            width="100%",
            align="stretch",
        ),
        description=(
            "Serve para textos, imagens ou explicações específicas de uma Meta "
            "sem exigir mudança no SMAE."
        ),
    )


def action_bar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.cond(
                MetaCmsState.error_message
                != "",
                rx.callout(
                    MetaCmsState
                    .error_message,
                    icon="triangle_alert",
                    color_scheme="red",
                    width="100%",
                ),
                rx.box(),
            ),

            rx.cond(
                MetaCmsState.success_message
                != "",
                rx.callout(
                    MetaCmsState
                    .success_message,
                    icon="circle_check",
                    color_scheme="green",
                    width="100%",
                ),
                rx.box(),
            ),

            rx.cond(
                MetaCmsState
                .conflict_count
                > 0,
                rx.callout(
                    rx.hstack(
                        rx.text(
                            MetaCmsState
                            .conflict_count,
                            " campo(s) com atualização do SMAE.",
                        ),
                        rx.spacer(),
                        rx.button(
                            "Revisar alterações",
                            size="1",
                            color_scheme="red",
                            on_click=(
                                MetaCmsState
                                .open_conflicts
                            ),
                        ),
                        width="100%",
                        align="center",
                    ),
                    icon="refresh_cw",
                    color_scheme="red",
                    width="100%",
                ),
                rx.box(),
            ),

            rx.grid(
                rx.vstack(
                    rx.text(
                        "Nota da publicação",
                        color=TEXT_SECONDARY,
                        font_size="0.72rem",
                    ),
                    rx.input(
                        value=(
                            MetaCmsState
                            .publication_note
                        ),
                        on_change=(
                            MetaCmsState
                            .set_publication_note
                        ),
                        placeholder=(
                            "Ex.: atualização semestral"
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
                            MetaCmsState
                            .save_draft
                        ),
                        disabled=(
                            ~MetaCmsState
                            .can_edit_content
                        ),
                        cursor="pointer",
                    ),

                    rx.cond(
                        MetaCmsState
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
                                MetaCmsState
                                .publish
                            ),
                            cursor="pointer",
                        ),
                        rx.box(),
                    ),

                    spacing="2",
                    justify="end",
                    align="center",
                    wrap="wrap",
                ),

                columns={
                    "initial": "1",
                    "lg": "2",
                },
                spacing="4",
                width="100%",
                align_items="end",
            ),

            spacing="3",
            width="100%",
            align="stretch",
        ),
        width="100%",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="12px",
        padding="1rem",
    )


def _conflict_row(
    item,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    item["field_key"],
                    variant="soft",
                ),
                rx.text(
                    rx.cond(
                        item["reason"]
                        == "removed_from_smae",
                        (
                            "O campo deixou de vir do SMAE."
                        ),
                        (
                            "O SMAE alterou um campo "
                            "personalizado."
                        ),
                    ),
                    color=TEXT_SECONDARY,
                    font_size="0.72rem",
                ),
                width="100%",
                align="center",
                spacing="2",
            ),

            rx.grid(
                rx.vstack(
                    rx.text(
                        "CMS atual",
                        color=TEXT_SECONDARY,
                        font_size="0.7rem",
                        font_weight="600",
                    ),
                    rx.code(
                        item["cms_value"],
                        white_space="pre-wrap",
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "Novo SMAE",
                        color=TEXT_SECONDARY,
                        font_size="0.7rem",
                        font_weight="600",
                    ),
                    rx.code(
                        item["smae_value"],
                        white_space="pre-wrap",
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),
                columns={
                    "initial": "1",
                    "lg": "2",
                },
                spacing="3",
                width="100%",
            ),

            rx.hstack(
                rx.button(
                    "Manter CMS",
                    size="2",
                    variant="outline",
                    on_click=lambda: (
                        MetaCmsState
                        .choose_conflict(
                            item["id"],
                            "keep_cms",
                        )
                    ),
                ),
                rx.button(
                    "Usar SMAE",
                    size="2",
                    color_scheme="blue",
                    on_click=lambda: (
                        MetaCmsState
                        .choose_conflict(
                            item["id"],
                            "use_smae",
                        )
                    ),
                ),
                spacing="2",
                justify="end",
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


def conflict_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Atualizações encontradas no SMAE"
            ),
            rx.dialog.description(
                (
                    "Escolha o que permanece personalizado "
                    "e o que deve voltar a usar o SMAE."
                )
            ),

            rx.hstack(
                rx.button(
                    "Manter tudo do CMS",
                    size="2",
                    variant="outline",
                    on_click=lambda: (
                        MetaCmsState
                        .choose_all_conflicts(
                            "keep_cms"
                        )
                    ),
                ),
                rx.button(
                    "Usar tudo do SMAE",
                    size="2",
                    color_scheme="blue",
                    on_click=lambda: (
                        MetaCmsState
                        .choose_all_conflicts(
                            "use_smae"
                        )
                    ),
                ),
                spacing="2",
                wrap="wrap",
            ),

            rx.scroll_area(
                rx.vstack(
                    rx.foreach(
                        MetaCmsState
                        .conflicts,
                        _conflict_row,
                    ),
                    spacing="3",
                    width="100%",
                    align="stretch",
                ),
                type="always",
                scrollbars="vertical",
                style={
                    "height": "58vh",
                },
            ),

            rx.hstack(
                rx.spacer(),
                rx.button(
                    "Fechar",
                    variant="soft",
                    on_click=(
                        MetaCmsState
                        .close_conflicts
                    ),
                ),
                width="100%",
            ),

            max_width="900px",
        ),
        open=(
            MetaCmsState
            .conflict_dialog_open
        ),
    )
