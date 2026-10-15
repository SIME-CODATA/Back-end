import reflex as rx

from Back_end.interface.state.meta.meta_detail_state import ( MetaDetailState,)
from Back_end.interface.theme.semantic import ( BORDER, BORDER_DARK, SURFACE, SURFACE_DARK, TEXT_PRIMARY, TEXT_PRIMARY_DARK, TEXT_SECONDARY, TEXT_SECONDARY_DARK, COLOR_UNIVERSO, COLOR_VIVER, COLOR_CIDADE, COLOR_CAPITAL,)
from Back_end.interface.theme.typography import ( FONT_FAMILY_PRIMARY, FONT_FAMILY_SECUNDARY, FONT_WEIGHT_SEMIBOLD,)


# ============================================================
# CORES
# ============================================================

HERO_BACKGROUND = rx.color_mode_cond(
    SURFACE,
    SURFACE_DARK,
)

HERO_BORDER = rx.color_mode_cond(
    BORDER,
    BORDER_DARK,
)

HERO_TEXT = rx.color_mode_cond(
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
)

HERO_TEXT_SECONDARY = rx.color_mode_cond(
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)


# ============================================================
# COR DO EIXO
# ============================================================

def get_meta_eixo_color(
    eixo: rx.Var[str],
):
    """Retorna a cor correspondente ao eixo."""

    return rx.cond(
        eixo == "Universo SP",
        COLOR_UNIVERSO,

        rx.cond(
            eixo == "Viver São Paulo",
            COLOR_VIVER,

            rx.cond(
                eixo == "Cidade Empreendedora",
                COLOR_CIDADE,

                rx.cond(
                    eixo == "Capital do Futuro",
                    COLOR_CAPITAL,

                    "#288140",
                ),
            ),
        ),
    )


# ============================================================
# HERO
# ============================================================

def meta_hero() -> rx.Component:
    """
    Cabeçalho principal da ficha da meta.

    Exibe:
    - título;
    - contexto;
    - número da meta;
    - eixo.
    """

    eixo_color = get_meta_eixo_color(
        MetaDetailState.eixo
    )

    return rx.box(
        rx.flex(

            # =================================================
            # CONTEÚDO PRINCIPAL
            # =================================================

            rx.vstack(
                rx.text(
                    MetaDetailState.titulo,
                    color=HERO_TEXT,
                    font_family=FONT_FAMILY_SECUNDARY,
                    font_size={ "initial": "1.45rem", "md": "1.8rem", },
                    line_height="1.15",
                    width="100%",
                ),

                rx.text(
                    MetaDetailState.contexto,
                    color=HERO_TEXT_SECONDARY,
                    font_family=FONT_FAMILY_PRIMARY,
                    font_size="0.88rem",
                    line_height="1.55",
                    white_space="pre-wrap",
                    width="100%",
                ),

                spacing="4",
                align="start",
                flex="1",
                min_width="0",
            ),

            # =================================================
            # BLOCO DA META
            # =================================================

            rx.center(
                rx.vstack(
                    rx.text(
                        "META ",
                        MetaDetailState.codigo_atual,
                        color="white",
                        font_family=FONT_FAMILY_SECUNDARY,
                        font_size={ "initial": "1.8rem", "md": "2.2rem", },
                        line_height="1",
                        white_space="nowrap",
                    ),

                    rx.box(
                        rx.text(
                            MetaDetailState.eixo,
                            color="white",
                            font_family=FONT_FAMILY_PRIMARY,
                            font_size="0.78rem",
                            font_weight=FONT_WEIGHT_SEMIBOLD,
                        ),

                        background="rgba(255,255,255,0.16)",
                        padding="0.35rem 0.7rem",
                        border_radius="999px",
                    ),

                    spacing="3",
                    align="center",
                ),

                width={"initial": "100%","lg": "260px",},
                min_width={ "initial": "100%", "lg": "260px", },
                min_height={ "initial": "120px", "lg": "180px", },
                background=eixo_color,
                border_radius={ "initial": "16px", "lg": "0 48px 0 0",},
            ),

            direction={ "initial": "column", "lg": "row", },

            gap="1.5rem",
            align="stretch",
            padding="1rem",
            width="100%",
        ),

        width="100%",
        background=HERO_BACKGROUND,
        border=f"1px solid {HERO_BORDER}",
        border_radius="18px",
        padding={ "initial": "1rem", "md": "1.4rem",},
    )