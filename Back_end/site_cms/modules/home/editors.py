import reflex as rx

from Back_end.interface.layouts.admin_layout import admin_layout
from Back_end.site_cms.components.editor.editor_shell import (
    section_editor_content,
)
from Back_end.site_cms.modules.home.components.letter_form import (
    about_form,
)
from Back_end.site_cms.modules.home.components.news_form import (
    news_form,
)
from Back_end.site_cms.modules.home.components.axes_form import (
    axes_form,
)


def mayor_letter_page() -> rx.Component:
    return admin_layout(
        section_editor_content(
            section_key="about_pdm",
            icon="file_text",
            form=about_form(),
        )
    )


def news_cms_page() -> rx.Component:
    return admin_layout(
        section_editor_content(
            section_key="news",
            icon="newspaper",
            form=news_form(),
        )
    )


def axes_cms_page() -> rx.Component:
    return admin_layout(
        section_editor_content(
            section_key="axes",
            icon="layers",
            form=axes_form(),
        )
    )
