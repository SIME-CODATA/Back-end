import reflex as rx

from Back_end.interface.layouts.admin_layout import admin_layout
from Back_end.site_cms.components.editor.editor_shell import (
    section_editor_content,
)
from Back_end.site_cms.modules.regionalization.components.form import (
    regionalization_form,
)


def regionalization_cms_page() -> rx.Component:
    return admin_layout(
        section_editor_content(
            section_key="regionalization",
            icon="map",
            form=regionalization_form(),
        )
    )
