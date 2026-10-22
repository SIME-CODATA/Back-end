import reflex as rx

from Back_end.interface.layouts.admin_layout import admin_layout
from Back_end.site_cms.components.editor.editor_shell import (
    section_editor_content,
)
from Back_end.site_cms.modules.transparency.components.form import (
    transparency_form,
)


def transparency_cms_page() -> rx.Component:
    return admin_layout(
        section_editor_content(
            section_key="transparency",
            icon="shield_check",
            form=transparency_form(),
        )
    )
