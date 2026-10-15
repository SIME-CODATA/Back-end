import reflex as rx

from Back_end.interface.pages.dashboard import dashboard_page


def admin_page() -> rx.Component:
    """Página inicial da área administrativa."""

    return dashboard_page()