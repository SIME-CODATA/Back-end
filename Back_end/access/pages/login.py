import reflex as rx

from Back_end.access.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.vstack(
                    rx.heading(
                        "Programa de Metas",
                        size="8",
                    ),
                    rx.text(
                        "Painel Administrativo",
                        color_scheme="gray",
                    ),
                    spacing="2",
                    align="center",
                    width="100%",
                ),

                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="E-mail",
                            name="email",
                            type="email",
                            required=True,
                            width="100%",
                        ),

                        rx.input(
                            placeholder="Senha",
                            name="password",
                            type="password",
                            required=True,
                            width="100%",
                        ),

                        rx.button(
                            "Entrar",
                            type="submit",
                            width="100%",
                        ),

                        rx.cond(
                            AuthState.error_message != "",
                            rx.callout(
                                AuthState.error_message,
                                icon="triangle-alert",
                                color_scheme="red",
                                width="100%",
                            ),
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
            ),
            width="100%",
            max_width="420px",
            padding="32px",
        ),
        min_height="100vh",
        padding="24px",
    )