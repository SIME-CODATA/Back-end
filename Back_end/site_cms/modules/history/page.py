import reflex as rx

from Back_end.interface.layouts.admin_layout import admin_layout
from Back_end.site_cms.components.editor.editor_shell import (
    section_editor_content,
)
from Back_end.site_cms.modules.history.components.form import (
    history_form,
)


def history_cms_page() -> rx.Component:
    return admin_layout(
        section_editor_content(
            section_key="history",
            icon="history",
            form=history_form(),
        )
    )
