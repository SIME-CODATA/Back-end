import reflex as rx


def admin_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading(
                "Programa de Metas",
                size="8",
            ),

            rx.text(
                "Área Administrativa",
                size="5",
            ),

            rx.text(
                "Sessão autenticada com sucesso.",
                color_scheme="gray",
            ),

            rx.button(
                "Sair",
                on_click=rx.redirect("/logout"),
                variant="soft",
            ),

            spacing="4",
            align="center",
        ),
        min_height="100vh",
    )