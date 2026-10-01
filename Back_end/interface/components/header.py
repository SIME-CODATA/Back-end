import reflex as rx

from Back_end.interface.theme.semantic import ( BORDER, BORDER_DARK, HEADER_BACKGROUND, HEADER_BACKGROUND_DARK, TEXT_PRIMARY, TEXT_PRIMARY_DARK, TEXT_SECONDARY, TEXT_SECONDARY_DARK, PRIMARY, PRIMARY_HOVER,)
from Back_end.interface.theme.typography import ( FONT_SIZE_SM, FONT_WEIGHT_MEDIUM, FONT_WEIGHT_SEMIBOLD,)

from Back_end.interface.state.dashboard_state import ( DashboardState,)


# ============================================================
# CORES REATIVAS AO TEMA
# ============================================================


def primary_text():
    return rx.color_mode_cond( TEXT_PRIMARY, TEXT_PRIMARY_DARK,)

def secondary_text():
    return rx.color_mode_cond( TEXT_SECONDARY, TEXT_SECONDARY_DARK,)

def header_border():
    return rx.color_mode_cond( BORDER, BORDER_DARK,)


# ============================================================
# NOTIFICAÇÕES
# ============================================================


def sync_notification() -> rx.Component:
    """Notificações globais de sincronização."""

    return rx.box(
        # ----------------------------------------------------
        # Sucesso
        # ----------------------------------------------------

        rx.cond(
            DashboardState.sync_message != "",

            rx.box(
                rx.hstack(
                    rx.center(
                        rx.icon(
                            tag="circle_check",
                            size=18,
                            color="#288140",
                        ),

                        width="34px",
                        height="34px",
                        min_width="34px",

                        border_radius="50%",

                        background=(
                            "rgba(40, 129, 64, 0.10)"
                        ),
                    ),

                    rx.vstack(
                        rx.text(
                            "Atualização concluída",
                            color=primary_text(),
                            font_size=FONT_SIZE_SM,
                            font_weight=(
                                FONT_WEIGHT_SEMIBOLD
                            ),
                        ),

                        rx.text(
                            DashboardState.sync_message,
                            color=secondary_text(),
                            font_size="0.78rem",
                            line_height="1.35",
                        ),

                        spacing="1",
                        align="start",
                        flex="1",
                    ),

                    rx.button(
                        rx.icon(
                            tag="x",
                            size=16,
                        ),

                        on_click=(
                            DashboardState
                            .clear_sync_message
                        ),

                        background="transparent",
                        color=secondary_text(),

                        padding="0.3rem",
                        min_width="auto",
                        height="auto",

                        cursor="pointer",
                        border_radius="6px",

                        _hover={
                            "background":
                            "rgba(0, 0, 0, 0.06)",
                        },
                    ),

                    width="100%",
                    align="start",
                    spacing="3",
                ),

                width="390px",
                max_width="calc(100vw - 2rem)",

                padding="1rem",

                background=rx.color_mode_cond(
                    "rgba(255, 255, 255, 0.98)",
                    "rgba(25, 31, 56, 0.98)",
                ),

                border=(
                    "1px solid "
                    "rgba(40, 129, 64, 0.25)"
                ),

                border_left=(
                    "4px solid #288140"
                ),

                border_radius="10px",

                box_shadow=(
                    "0 12px 35px "
                    "rgba(0, 0, 0, 0.18)"
                ),

                backdrop_filter="blur(10px)",
            ),
        ),

        # ----------------------------------------------------
        # Erro
        # ----------------------------------------------------

        rx.cond(
            DashboardState.error_message != "",

            rx.box(
                rx.hstack(
                    rx.center(
                        rx.icon(
                            tag="triangle_alert",
                            size=18,
                            color="#EC2024",
                        ),

                        width="34px",
                        height="34px",
                        min_width="34px",

                        border_radius="50%",

                        background=(
                            "rgba(236, 32, 36, 0.10)"
                        ),
                    ),

                    rx.vstack(
                        rx.text(
                            "Erro na atualização",
                            color=primary_text(),
                            font_size=FONT_SIZE_SM,
                            font_weight=(
                                FONT_WEIGHT_SEMIBOLD
                            ),
                        ),

                        rx.text(
                            DashboardState.error_message,
                            color=secondary_text(),
                            font_size="0.78rem",
                            line_height="1.35",
                        ),

                        spacing="1",
                        align="start",
                        flex="1",
                    ),

                    rx.button(
                        rx.icon(
                            tag="x",
                            size=16,
                        ),

                        on_click=(
                            DashboardState
                            .clear_error_message
                        ),

                        background="transparent",
                        color=secondary_text(),

                        padding="0.3rem",
                        min_width="auto",
                        height="auto",

                        cursor="pointer",
                        border_radius="6px",

                        _hover={
                            "background":
                            "rgba(0, 0, 0, 0.06)",
                        },
                    ),

                    width="100%",
                    align="start",
                    spacing="3",
                ),

                width="390px",
                max_width="calc(100vw - 2rem)",

                padding="1rem",

                background=rx.color_mode_cond(
                    "rgba(255, 255, 255, 0.98)",
                    "rgba(25, 31, 56, 0.98)",
                ),

                border=(
                    "1px solid "
                    "rgba(236, 32, 36, 0.25)"
                ),

                border_left=(
                    "4px solid #EC2024"
                ),

                border_radius="10px",

                box_shadow=(
                    "0 12px 35px "
                    "rgba(0, 0, 0, 0.18)"
                ),

                backdrop_filter="blur(10px)",
            ),
        ),

        # ----------------------------------------------------
        # Posicionamento
        # ----------------------------------------------------

        position="fixed",

        top="88px",
        right="1.5rem",

        z_index="3000",

        display="flex",
        flex_direction="column",

        gap="0.75rem",

        pointer_events="auto",
    )


# ============================================================
# HEADER
# ============================================================


def header() -> rx.Component:
    """Cabeçalho principal da interface administrativa."""

    return rx.box(
        rx.hstack(
            # ------------------------------------------------
            # Logo
            # ------------------------------------------------

            rx.image(
                src="/svg/Logo_pdm_adm.svg",

                width="80px",
                height="auto",

                object_fit="contain",

                filter=rx.color_mode_cond(
                    "none",
                    "brightness(0) invert(1)",
                ),

                transition="filter 0.2s ease",

                flex_shrink="0",
            ),

            rx.spacer(),

            # ------------------------------------------------
            # Sincronização
            # ------------------------------------------------

            rx.hstack(
                rx.button(
                    rx.icon(
                        tag="refresh_cw",
                        size=15,
                    ),

                    rx.cond(
                        DashboardState.loading,
                        "Atualizando...",
                        "Atualizar",
                    ),

                    on_click=(
                        DashboardState.refresh_data
                    ),

                    background=PRIMARY,
                    color="white",

                    border_radius="7px",

                    padding_x="1rem",

                    height="36px",

                    cursor="pointer",

                    disabled=DashboardState.loading,

                    _hover={
                        "background": PRIMARY_HOVER,
                    },
                ),

                rx.vstack(
                    rx.text(
                        "Última atualização",

                        color=secondary_text(),

                        font_size="0.55rem",

                        font_weight=(
                            FONT_WEIGHT_SEMIBOLD
                        ),

                        text_transform="uppercase",

                        white_space="nowrap",
                    ),

                    rx.text(
                        DashboardState
                        .ultima_sincronizacao,

                        color=primary_text(),

                        font_size=FONT_SIZE_SM,

                        font_weight=(
                            FONT_WEIGHT_SEMIBOLD
                        ),

                        white_space="nowrap",
                    ),

                    spacing="0",
                    align="start",
                ),

                spacing="3",
                align="center",
            ),

            # ------------------------------------------------
            # Separador
            # ------------------------------------------------

            rx.box(
                width="1px",
                height="32px",

                background=header_border(),

                margin_x="0.4rem",
            ),

            # ------------------------------------------------
            # Notificações futuras
            # ------------------------------------------------

            rx.button(
                rx.icon(
                    tag="bell",
                    size=19,
                ),

                variant="ghost",

                color=secondary_text(),

                padding="0.45rem",

                min_width="auto",
                height="auto",

                border_radius="8px",

                cursor="pointer",
            ),

            # ------------------------------------------------
            # Usuário
            # ------------------------------------------------

            rx.hstack(
                rx.center(
                    rx.text(
                        "A",

                        font_weight=(
                            FONT_WEIGHT_SEMIBOLD
                        ),

                        font_size=FONT_SIZE_SM,

                        color="white",
                    ),

                    width="36px",
                    height="36px",

                    min_width="36px",

                    border_radius="50%",

                    background="#272361",
                ),

                rx.vstack(
                    rx.text(
                        "Administrador",

                        color=primary_text(),

                        font_size=FONT_SIZE_SM,

                        font_weight=(
                            FONT_WEIGHT_MEDIUM
                        ),

                        white_space="nowrap",
                    ),

                    rx.text(
                        "Painel administrativo",

                        color=secondary_text(),

                        font_size="0.72rem",

                        white_space="nowrap",
                    ),

                    spacing="0",
                    align="start",
                ),

                rx.icon(
                    tag="chevron_down",

                    size=16,

                    color=secondary_text(),
                ),

                align="center",
                spacing="3",
            ),

            width="100%",
            height="72px",

            padding_x="1.75rem",

            background=rx.color_mode_cond(
                HEADER_BACKGROUND,
                HEADER_BACKGROUND_DARK,
            ),

            border_bottom=rx.color_mode_cond(
                f"1px solid {BORDER}",
                f"1px solid {BORDER_DARK}",
            ),

            align="center",
            spacing="4",

            flex_shrink="0",
        ),

        # ESTE ERA O PEDAÇO QUE ESTAVA FALTANDO
        sync_notification(),

        width="100%",
        flex_shrink="0",

        # Carrega a informação do header em qualquer
        # tela administrativa.
        on_mount=DashboardState.load_summary,
    )