import reflex as rx

from Back_end.access.states.auth_state import AuthState
from Back_end.interface.theme.semantic import (
    ACCENT,
    ACCENT_HOVER,
    BORDER,
    PAGE_BACKGROUND,
    PRIMARY,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    WHITE,
)
from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
    FONT_SIZE_MD,
    FONT_SIZE_SM,
    FONT_SIZE_XL,
    FONT_SIZE_2XL,
    FONT_WEIGHT_BOLD,
    FONT_WEIGHT_MEDIUM,
    FONT_WEIGHT_SEMIBOLD,
)


def visual_panel() -> rx.Component:
    """Painel com a capa oficial do Programa de Metas."""

    return rx.box(
        rx.image(
            src="/images/capa.jpg",
            width="100%",
            height="100%",
            object_fit="cover",
            object_position="center",
        ),

        width=["0%", "0%", "85%"],
        display=["none", "none", "block"],
        height="100vh",
        position="relative",
        overflow="hidden",
        background=PRIMARY,
    )


def map_decoration() -> rx.Component:
    """Área reservada para o mapa vetorial de São Paulo."""

    return rx.box(
        position="absolute",
        top="0",
        right="0",
        width="65%",
        height="45%",
        opacity="0.07",
        pointer_events="none",
        z_index="0",
    )


def login_form() -> rx.Component:
    """Formulário de autenticação."""

    return rx.vstack(
        rx.vstack(
            rx.image(
                src="/svg/prog_metas_logo_simp.svg",
                height="5rem",
                width="100%",
                align="center",
            ),

            rx.text(
                "Bem-vindo",
                color=TEXT_PRIMARY,
                font_size=FONT_SIZE_2XL,
                font_weight=FONT_WEIGHT_BOLD,
            ),

            rx.text(
                "Entre com suas credenciais para acessar o painel administrativo.",
                color=TEXT_SECONDARY,
                font_size=FONT_SIZE_SM,
                line_height="1.6",
            ),

            spacing="1",
            align="start",
            width="100%",
        ),

        rx.form(
            rx.vstack(
                rx.vstack(
                    rx.text(
                        "E-mail",
                        color=TEXT_PRIMARY,
                        font_size=FONT_SIZE_SM,
                        font_weight=FONT_WEIGHT_SEMIBOLD,
                    ),

                    rx.input(
                        name="email",
                        type="email",
                        placeholder="seu.email@prefeitura.sp.gov.br",
                        required=True,
                        width="100%",
                        height="48px",
                        border=f"1px solid {BORDER}",
                        border_radius="8px",
                        background=WHITE,
                        color=TEXT_PRIMARY,
                        padding_x="0.9rem",
                        _placeholder={
                            "color": "#8B92A0",
                            "opacity": "1",
                        },
                        _focus={
                            "border_color": "#0E7BA8",
                            "box_shadow": "0 0 0 2px rgba(14, 123, 168, 0.12)",
                        },
                    ),

                    align="start",
                    width="100%",
                    spacing="2",
                ),

                rx.vstack(
                    rx.text(
                        "Senha",
                        color=TEXT_PRIMARY,
                        font_size=FONT_SIZE_SM,
                        font_weight=FONT_WEIGHT_SEMIBOLD,
                    ),

                    rx.input(
                        name="password",
                        type="password",
                        placeholder="Digite sua senha",
                        required=True,
                        width="100%",
                        height="48px",
                        border=f"1px solid {BORDER}",
                        border_radius="8px",
                        background=WHITE,
                        color=TEXT_PRIMARY,
                        padding_x="0.9rem",
                        _placeholder={
                            "color": "#8B92A0",
                            "opacity": "1",
                        },
                        _focus={
                            "border_color": "#0E7BA8",
                            "box_shadow": "0 0 0 2px rgba(14, 123, 168, 0.12)",
                        },
                    ),

                    align="start",
                    width="100%",
                    spacing="2",
                ),

                rx.cond(
                    AuthState.error_message != "",
                    rx.box(
                        rx.text(
                            AuthState.error_message,
                            color="#EC2024",
                            font_size=FONT_SIZE_SM,
                        ),
                        width="100%",
                        padding="0.75rem",
                        border_radius="8px",
                        background="rgba(236, 32, 36, 0.08)",
                    ),
                ),

                rx.button(
                    "Entrar",
                    type="submit",
                    width="100%",
                    height="48px",
                    background=PRIMARY,
                    color=WHITE,
                    border_radius="8px",
                    font_weight=FONT_WEIGHT_SEMIBOLD,
                    cursor="pointer",
                    transition="all 0.2s ease",
                    _hover={
                        "background": ACCENT_HOVER,
                    },
                ),

                spacing="4",
                width="100%",
            ),

            on_submit=AuthState.login,
            reset_on_submit=False,
            width="100%",
        ),

        spacing="6",
        width="100%",
        max_width="420px",
        position="relative",
        z_index="1",
    )


def login_page() -> rx.Component:
    """Página de login da interface administrativa."""

    return rx.hstack(
        visual_panel(),

        rx.box(
            map_decoration(),

            rx.vstack(
                rx.center(
                    login_form(),
                    width="100%",
                    flex="1",
                ),

                login_footer(),

                width="100%",
                height="100%",
                min_height="100vh",
                padding=[
                    "2rem 1.5rem",
                    "2.5rem",
                    "3rem 4rem",
                ],
                position="relative",
                z_index="1",
            ),

            width=["100%", "100%", "48%"],
            min_height="100vh",
            background=PAGE_BACKGROUND,
            position="relative",
            overflow="hidden",
        ),

        width="100%",
        min_height="100vh",
        spacing="0",
        align="stretch",
        font_family=FONT_FAMILY_PRIMARY,
    )


def login_footer() -> rx.Component:
    """Rodapé institucional da tela de login."""

    return rx.vstack(
        rx.hstack(

            rx.image(
                src="/images/SEC_GOVERNO.png",
                height="6em",
                width="auto",
            ),
            rx.image(
                src="/images/SEC_PLANEJAMENTO_E _EFICIÊNCIA.png",
                height="6rem",
                width="auto",
            ),
            rx.image(
                src="/svg/logo_codata.svg",
                height="32px",
                width="auto",
            ),

            spacing="4",
            align="center",
            justify="center",
            width="100%",
        ),

        rx.text(
            "Copyleft © CODATA",
            color=TEXT_SECONDARY,
            font_size="0.72rem",
            text_align="center",
        ),

        spacing="3",
        width="100%",
        align="center",
    )