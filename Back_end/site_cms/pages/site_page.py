import reflex as rx

from Back_end.interface.layouts.admin_layout import admin_layout


TEXT_PRIMARY = rx.color_mode_cond(
    "#1B263B",
    "#F4F7FF",
)

TEXT_MUTED = rx.color_mode_cond(
    "#6C7890",
    "#B8C4DA",
)

CARD_BG = rx.color_mode_cond(
    "#FFFFFF",
    "#18243E",
)

CARD_BORDER = rx.color_mode_cond(
    "rgba(22, 37, 63, 0.10)",
    "rgba(255, 255, 255, 0.10)",
)


def _module_card(
    *,
    title: str,
    description: str,
    href: str,
    icon: str,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(
                rx.icon(
                    tag=icon,
                    size=22,
                    color="#1281AA",
                ),
                width="46px",
                height="46px",
                display="flex",
                align_items="center",
                justify_content="center",
                border_radius="12px",
                background=rx.color_mode_cond(
                    "#EAF7FC",
                    "#203B54",
                ),
            ),
            rx.heading(
                title,
                size="4",
                color=TEXT_PRIMARY,
            ),
            rx.text(
                description,
                color=TEXT_MUTED,
                font_size="0.8rem",
                line_height="1.45",
            ),
            rx.spacer(),
            rx.link(
                rx.button(
                    "Gerenciar",
                    rx.icon(
                        tag="arrow_right",
                        size=14,
                    ),
                    size="2",
                    variant="soft",
                    cursor="pointer",
                ),
                href=href,
                text_decoration="none",
            ),
            spacing="3",
            align="start",
            height="100%",
            width="100%",
        ),
        width="100%",
        min_height="215px",
        padding="1.1rem",
        background=CARD_BG,
        border=f"1px solid {CARD_BORDER}",
        border_radius="14px",
    )


def site_cms_content() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.text(
                "SITE",
                font_size="0.76rem",
                font_weight="700",
                letter_spacing="0.12em",
                color="#1281AA",
            ),
            rx.heading(
                "Conteúdo do site",
                size="7",
                color=TEXT_PRIMARY,
            ),
            rx.text(
                (
                    "Cada página do site possui seu próprio módulo. "
                    "Notícias e Eixos permanecem dentro da Página Inicial."
                ),
                color=TEXT_MUTED,
                font_size="0.95rem",
            ),
            spacing="2",
            align="start",
        ),

        rx.grid(
            _module_card(
                title="Página Inicial",
                description="Carta do prefeito, Notícias e Eixos.",
                href="/admin/site/home",
                icon="house",
            ),
            _module_card(
                title="Sobre o PdM",
                description="Apresentação institucional, objetivos e metodologia.",
                href="/admin/site/sobre",
                icon="info",
            ),
            _module_card(
                title="Histórico",
                description="Ciclos anteriores, imagens e documentos.",
                href="/admin/site/historico",
                icon="history",
            ),
            _module_card(
                title="Metas",
                description=(
                    "Fichas públicas, dados do SMAE, "
                    "personalizações e conflitos de sincronização."
                ),
                href="/admin/site/metas",
                icon="target",
            ),
            _module_card(
                title="Regionalização",
                description="Textos, arquivo e dashboard.",
                href="/admin/site/regionalizacao",
                icon="map",
            ),
            _module_card(
                title="Transparência e Monitoramento",
                description="Textos, recursos, botões e links.",
                href="/admin/site/transparencia",
                icon="shield_check",
            ),
            columns={
                "initial": "1",
                "md": "2",
                "xl": "3",
            },
            spacing="4",
            width="100%",
        ),

        spacing="6",
        align="stretch",
        width="100%",
        max_width="1180px",
        margin="0 auto",
    )


def site_cms_page() -> rx.Component:
    return admin_layout(
        site_cms_content()
    )
