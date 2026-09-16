import reflex as rx


class SidebarState(rx.State):
    """Controla o estado visual da barra lateral."""

    expanded: bool = True

    @rx.event
    def toggle_sidebar(self):
        self.expanded = not self.expanded