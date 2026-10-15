import reflex as rx

from Back_end.interface.state.meta.meta_print_state import (
    MetaPrintFichaItem,
)

from Back_end.interface.theme.semantic import (
    COLOR_UNIVERSO,
    COLOR_VIVER,
    COLOR_CIDADE,
    COLOR_CAPITAL,
)

from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
    FONT_FAMILY_SECUNDARY,
)


def get_print_eixo_color(
    eixo: rx.Var[str],
):
    return rx.cond(
        eixo == "Universo SP",
        COLOR_UNIVERSO,

        rx.cond(
            eixo == "Viver São Paulo",
            COLOR_VIVER,

            rx.cond(
                eixo
                == "Cidade Empreendedora",

                COLOR_CIDADE,

                rx.cond(
                    eixo
                    == "Capital do Futuro",

                    COLOR_CAPITAL,

                    "#288140",
                ),
            ),
        ),
    )


def meta_print_header(
    ficha: rx.Var[
        MetaPrintFichaItem
    ],
) -> rx.Component:

    eixo_color = (
        get_print_eixo_color(
            ficha["eixo"]
        )
    )

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text(
                        "PROGRAMA DE METAS "
                        "2025-2028",

                        color="#667085",

                        font_family=(
                            FONT_FAMILY_PRIMARY
                        ),

                        font_size="0.68rem",

                        font_weight="700",
                    ),

                    rx.text(
                        "FICHA DA META",

                        color="#17213C",

                        font_family=(
                            FONT_FAMILY_SECUNDARY
                        ),

                        font_size="1.25rem",

                        line_height="1",
                    ),

                    spacing="1",
                    align="start",
                ),

                rx.spacer(),

                rx.box(
                    rx.vstack(
                        rx.text(
                            "META ",
                            ficha["codigo"],

                            color="white",

                            font_family=(
                                FONT_FAMILY_SECUNDARY
                            ),

                            font_size="1.25rem",
                        ),

                        rx.text(
                            ficha["eixo"],

                            color="white",

                            font_family=(
                                FONT_FAMILY_PRIMARY
                            ),

                            font_size="0.68rem",
                        ),

                        spacing="2",

                        align="center",
                    ),

                    background=eixo_color,

                    padding="0.7rem 1rem",

                    border_radius="8px",

                    min_width="120px",
                ),

                width="100%",

                align="center",
            ),

            rx.text(
                ficha["titulo"],

                color="#17213C",

                font_family=(
                    FONT_FAMILY_SECUNDARY
                ),

                font_size="1.35rem",

                line_height="1.2",
            ),

            rx.cond(
                ficha["contexto"] != "",

                rx.box(
                    rx.text(
                        ficha["contexto"],

                        color="#344054",

                        font_family=(
                            FONT_FAMILY_PRIMARY
                        ),

                        font_size="0.76rem",

                        line_height="1.5",

                        white_space="pre-wrap",
                    ),

                    width="100%",

                    padding="0.75rem",

                    background="#F7F9FB",

                    border_radius="8px",
                ),
            ),

            spacing="4",

            align="stretch",

            width="100%",
        ),

        class_name="print-card",

        width="100%",

        padding_bottom="0.3rem",

        border_bottom=(
            f"4px solid "
            f"{eixo_color}"
        ),
    )