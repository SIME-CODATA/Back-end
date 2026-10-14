import reflex as rx

from Back_end.interface.state.meta.meta_print_state import (
    MetaPrintState,
    MetaPrintFichaItem,
)

from Back_end.interface.state.meta.meta_detail_state import (
    MetaObraItem,
    MetaProjetoItem,
)

from Back_end.interface.components.meta.print.meta_print_header import (
    meta_print_header,
)

from Back_end.interface.components.meta.print.meta_print_section import (
    meta_print_section,
    meta_print_info,
    meta_print_chip,
)

from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
)


# ============================================================
# HELPERS
# ============================================================

def print_chip_item(
    value,
) -> rx.Component:
    """Chip utilizado no documento."""

    return meta_print_chip(
        value
    )


def print_text_item(
    value,
) -> rx.Component:
    """Item textual compacto."""

    return rx.box(
        rx.text(
            value,

            color="#17213C",

            font_family=FONT_FAMILY_PRIMARY,

            font_size="0.72rem",

            line_height="1.35",
        ),

        class_name="print-card",

        width="100%",

        padding="0.5rem 0.65rem",

        border="1px solid #E1E6ED",

        border_radius="7px",

        background="#FAFBFC",
    )


# ============================================================
# OBRA
# ============================================================

def print_work_item(
    obra: rx.Var[MetaObraItem],
) -> rx.Component:
    """Card compacto de uma obra."""

    return rx.box(
        rx.vstack(

            # ------------------------------------------------
            # Cabeçalho
            # ------------------------------------------------

            rx.hstack(
                rx.vstack(
                    rx.text(
                        obra["codigo"],

                        color="#288140",

                        font_size="0.62rem",

                        font_weight="700",
                    ),

                    rx.text(
                        obra["nome"],

                        color="#17213C",

                        font_size="0.76rem",

                        font_weight="700",

                        line_height="1.25",
                    ),

                    spacing="1",

                    align="start",

                    flex="1",

                    min_width="0",
                ),

                rx.box(
                    rx.text(
                        obra["percentual"],

                        color="#288140",

                        font_size="0.65rem",

                        font_weight="700",
                    ),

                    padding="0.25rem 0.4rem",

                    background="#EAF5ED",

                    border_radius="999px",
                ),

                align="start",

                spacing="2",

                width="100%",
            ),

            # ------------------------------------------------
            # Informações
            # ------------------------------------------------

            rx.grid(
                meta_print_info(
                    "Status",
                    obra["status"],
                ),

                meta_print_info(
                    "Tipo",
                    obra["tipo"],
                ),

                meta_print_info(
                    "Equipamento",
                    obra["equipamento"],
                ),

                meta_print_info(
                    "Subprefeituras",
                    obra["subprefeituras"],
                ),

                columns="2",

                spacing="2",

                width="100%",
            ),

            spacing="2",

            align="stretch",

            width="100%",
        ),

        class_name="print-card",

        width="100%",

        padding="0.65rem",

        border="1px solid #DCE2EA",

        border_radius="8px",

        background="#FFFFFF",
    )


# ============================================================
# PROJETO
# ============================================================

def print_project_item(
    projeto: rx.Var[MetaProjetoItem],
) -> rx.Component:
    """Card compacto de um projeto."""

    return rx.box(
        rx.vstack(
            rx.text(
                projeto["codigo"],

                color="#272361",

                font_size="0.62rem",

                font_weight="700",
            ),

            rx.text(
                projeto["nome"],

                color="#17213C",

                font_size="0.76rem",

                font_weight="700",

                line_height="1.25",
            ),

            rx.grid(
                meta_print_info(
                    "Portfólio",
                    projeto["portfolio"],
                ),

                meta_print_info(
                    "Etapa",
                    projeto["etapa"],
                ),

                columns="2",

                spacing="2",

                width="100%",
            ),

            spacing="2",

            align="stretch",

            width="100%",
        ),

        class_name="print-card",

        width="100%",

        padding="0.65rem",

        border="1px solid #DCE2EA",

        border_radius="8px",

        background="#FFFFFF",
    )


# ============================================================
# UMA FICHA
# ============================================================

def print_single_meta(
    ficha: rx.Var[MetaPrintFichaItem],
) -> rx.Component:
    """
    Renderiza uma única Ficha da Meta.

    Quando houver várias fichas, cada uma é colocada
    como um documento completo dentro do PDF.
    """

    return rx.box(
        rx.vstack(

            # =================================================
            # HEADER
            # =================================================

            meta_print_header(
                ficha
            ),

            # =================================================
            # STATUS
            # =================================================

            meta_print_section(
                "STATUS DA META",

                rx.grid(
                    meta_print_info(
                        "Andamento",
                        ficha["andamento"],
                    ),

                    meta_print_info(
                        "Situação",
                        ficha["situacao"],
                    ),

                    meta_print_info(
                        "Previsão",
                        ficha["prazo"],
                    ),

                    columns="3",

                    spacing="3",

                    width="100%",
                ),
            ),

            # =================================================
            # CLASSIFICAÇÕES
            # =================================================

            meta_print_section(
                "CLASSIFICAÇÕES",

                rx.grid(

                    # -----------------------------------------
                    # Órgãos
                    # -----------------------------------------

                    rx.vstack(
                        rx.text(
                            "Órgãos vinculados",

                            color="#667085",

                            font_size="0.66rem",

                            font_weight="700",
                        ),

                        rx.cond(
                            ficha["orgaos"].length() > 0,

                            rx.flex(
                                rx.foreach(
                                    ficha["orgaos"],
                                    print_chip_item,
                                ),

                                wrap="wrap",

                                gap="0.35rem",
                            ),

                            rx.text(
                                "Não informado.",

                                color="#667085",

                                font_size="0.7rem",
                            ),
                        ),

                        spacing="2",

                        align="start",
                    ),

                    # -----------------------------------------
                    # ODS
                    # -----------------------------------------

                    rx.vstack(
                        rx.text(
                            "ODS vinculados",

                            color="#667085",

                            font_size="0.66rem",

                            font_weight="700",
                        ),

                        rx.cond(
                            ficha["ods"].length() > 0,

                            rx.flex(
                                rx.foreach(
                                    ficha["ods"],
                                    print_chip_item,
                                ),

                                wrap="wrap",

                                gap="0.35rem",
                            ),

                            rx.text(
                                "Não informado.",

                                color="#667085",

                                font_size="0.7rem",
                            ),
                        ),

                        spacing="2",

                        align="start",
                    ),

                    columns="2",

                    spacing="4",

                    width="100%",
                ),

                # ---------------------------------------------
                # Outras tags
                # ---------------------------------------------

                rx.cond(
                    ficha[
                        "outras_tags"
                    ].length()
                    > 0,

                    rx.vstack(
                        rx.text(
                            "Demais classificações",

                            color="#667085",

                            font_size="0.66rem",

                            font_weight="700",
                        ),

                        rx.flex(
                            rx.foreach(
                                ficha[
                                    "outras_tags"
                                ],
                                print_chip_item,
                            ),

                            wrap="wrap",

                            gap="0.35rem",
                        ),

                        spacing="2",

                        align="start",
                    ),
                ),
            ),

            # =================================================
            # ORÇAMENTO
            # =================================================

            meta_print_section(
                "ORÇAMENTO",

                rx.grid(
                    meta_print_info(
                        "Recursos previstos",
                        ficha["previsao"],
                    ),

                    meta_print_info(
                        "Empenhado",
                        ficha["empenhado"],
                    ),

                    meta_print_info(
                        "Liquidado",
                        ficha["liquidado"],
                    ),

                    columns="3",

                    spacing="3",

                    width="100%",
                ),
            ),

            # =================================================
            # REGIONALIZAÇÃO
            # =================================================

            meta_print_section(
                "REGIONALIZAÇÃO",

                rx.grid(

                    # -----------------------------------------
                    # Regiões
                    # -----------------------------------------

                    rx.vstack(
                        rx.text(
                            "Regiões com obras relacionadas",

                            color="#667085",

                            font_size="0.66rem",

                            font_weight="700",
                        ),

                        rx.cond(
                            ficha[
                                "regioes"
                            ].length()
                            > 0,

                            rx.flex(
                                rx.foreach(
                                    ficha[
                                        "regioes"
                                    ],
                                    print_chip_item,
                                ),

                                wrap="wrap",

                                gap="0.35rem",
                            ),

                            rx.text(
                                "Nenhuma região identificada.",

                                color="#667085",

                                font_size="0.7rem",
                            ),
                        ),

                        spacing="2",

                        align="start",
                    ),

                    # -----------------------------------------
                    # Subprefeituras
                    # -----------------------------------------

                    rx.vstack(
                        rx.text(
                            "Subprefeituras",

                            color="#667085",

                            font_size="0.66rem",

                            font_weight="700",
                        ),

                        rx.cond(
                            ficha[
                                "subprefeituras"
                            ].length()
                            > 0,

                            rx.flex(
                                rx.foreach(
                                    ficha[
                                        "subprefeituras"
                                    ],
                                    print_chip_item,
                                ),

                                wrap="wrap",

                                gap="0.35rem",
                            ),

                            rx.text(
                                "Nenhuma subprefeitura "
                                "identificada.",

                                color="#667085",

                                font_size="0.7rem",
                            ),
                        ),

                        spacing="2",

                        align="start",
                    ),

                    columns="2",

                    spacing="4",

                    width="100%",
                ),
            ),

            # =================================================
            # INICIATIVAS
            # =================================================

            meta_print_section(
                "INICIATIVAS",

                rx.cond(
                    ficha[
                        "iniciativas"
                    ].length()
                    > 0,

                    rx.vstack(
                        rx.foreach(
                            ficha[
                                "iniciativas"
                            ],
                            print_text_item,
                        ),

                        spacing="2",

                        align="stretch",
                    ),

                    rx.text(
                        "Nenhuma iniciativa cadastrada.",

                        color="#667085",

                        font_size="0.72rem",
                    ),
                ),
            ),

            # =================================================
            # METAS RELACIONADAS
            # =================================================

            rx.cond(
                ficha[
                    "metas_relacionadas"
                ].length()
                > 0,

                meta_print_section(
                    "METAS RELACIONADAS",

                    rx.vstack(
                        rx.foreach(
                            ficha[
                                "metas_relacionadas"
                            ],
                            print_text_item,
                        ),

                        spacing="2",

                        align="stretch",
                    ),
                ),
            ),

            # =================================================
            # OBRAS
            # =================================================

            meta_print_section(
                "OBRAS RELACIONADAS",

                rx.text(
                    ficha["obras"].length(),

                    " obra(s) relacionada(s)",

                    color="#667085",

                    font_size="0.68rem",
                ),

                rx.cond(
                    ficha[
                        "obras"
                    ].length()
                    > 0,

                    rx.grid(
                        rx.foreach(
                            ficha[
                                "obras"
                            ],
                            print_work_item,
                        ),

                        columns="2",

                        spacing="3",

                        width="100%",
                    ),

                    rx.text(
                        "Nenhuma obra relacionada.",

                        color="#667085",

                        font_size="0.72rem",
                    ),
                ),

                allow_break=True,
            ),

            # =================================================
            # PROJETOS
            # =================================================

            meta_print_section(
                "PROJETOS RELACIONADOS",

                rx.text(
                    ficha[
                        "projetos"
                    ].length(),

                    " projeto(s) relacionado(s)",

                    color="#667085",

                    font_size="0.68rem",
                ),

                rx.cond(
                    ficha[
                        "projetos"
                    ].length()
                    > 0,

                    rx.grid(
                        rx.foreach(
                            ficha[
                                "projetos"
                            ],
                            print_project_item,
                        ),

                        columns="2",

                        spacing="3",

                        width="100%",
                    ),

                    rx.text(
                        "Nenhum projeto relacionado.",

                        color="#667085",

                        font_size="0.72rem",
                    ),
                ),

                allow_break=True,
            ),

            # =================================================
            # RODAPÉ
            # =================================================

            rx.box(
                rx.text(
                    "Programa de Metas 2025-2028 "
                    "• Ficha gerada pelo sistema administrativo",

                    color="#98A2B3",

                    font_size="0.58rem",

                    text_align="center",
                ),

                width="100%",

                padding_top="0.5rem",

                border_top=(
                    "1px solid #E4E7EC"
                ),
            ),

            spacing="4",

            align="stretch",

            width="100%",
        ),

        class_name=(
            "meta-print-ficha"
        ),

        width="100%",
    )


# ============================================================
# DOCUMENTO COMPLETO
# ============================================================

def meta_print_document() -> rx.Component:
    """
    Documento imprimível.

    Pode conter uma ou várias Fichas da Meta.
    """

    return rx.box(
        rx.foreach(
            MetaPrintState.fichas,
            print_single_meta,
        ),

        class_name=(
            "meta-print-document"
        ),

        width="100%",
    )