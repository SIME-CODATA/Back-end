import reflex as rx


def logout_page() -> rx.Component:
    """Página exibida enquanto a sessão é encerrada."""

    return rx.center(
        rx.vstack(
            rx.spinner(
                size="3",
            ),
            rx.text(
                "Encerrando sessão...",
                color_scheme="gray",
            ),
            spacing="4",
            align="center",
        ),
        min_height="100vh",
    )