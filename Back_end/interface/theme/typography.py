"""Tipografia da interface administrativa do Programa de Metas."""
import reflex as rx
app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap",
        "https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap"
    ],
)


# Família tipográfica
FONT_FAMILY_PRIMARY = "Roboto, Helvetica, sans-serif"
FONT_FAMILY_SECUNDARY = "Bebas Neue, sans-serif"
FONT_FAMILY_DISPLAY = FONT_FAMILY_PRIMARY


# Pesos
FONT_WEIGHT_REGULAR = "400"
FONT_WEIGHT_MEDIUM = "500"
FONT_WEIGHT_SEMIBOLD = "600"
FONT_WEIGHT_BOLD = "700"


# Tamanhos
FONT_SIZE_XS = "0.75rem"      # 12px
FONT_SIZE_SM = "0.875rem"     # 14px
FONT_SIZE_MD = "1rem"         # 16px
FONT_SIZE_LG = "1.125rem"     # 18px
FONT_SIZE_XL = "1.5rem"       # 24px
FONT_SIZE_2XL = "2rem"        # 32px
FONT_SIZE_3XL = "2.5rem"      # 40px


# Altura de linha
LINE_HEIGHT_TIGHT = "1.2"
LINE_HEIGHT_NORMAL = "1.5"
LINE_HEIGHT_RELAXED = "1.7"