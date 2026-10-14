import reflex as rx

from Back_end.interface.layouts.admin_layout import ( admin_layout,)
from Back_end.interface.state.meta.meta_list_state import ( MetaListState,)
from Back_end.access_api.metas.services.meta_list_service import ( MetaListItem,)
from Back_end.interface.components.meta.meta_filter_dock import ( meta_filter_dock,)
from Back_end.interface.theme.semantic import ( TEXT_PRIMARY, TEXT_PRIMARY_DARK, TEXT_SECONDARY, TEXT_SECONDARY_DARK, COLOR_UNIVERSO, COLOR_VIVER, COLOR_CIDADE, COLOR_CAPITAL,)
from Back_end.interface.theme.typography import ( FONT_FAMILY_PRIMARY, FONT_FAMILY_SECUNDARY, FONT_WEIGHT_SEMIBOLD,)

# ============================================================
# CORES
# ============================================================

CARD_TEXT = rx.color_mode_cond( TEXT_PRIMARY, TEXT_PRIMARY_DARK,)
CARD_TEXT_SECONDARY = rx.color_mode_cond( TEXT_SECONDARY, TEXT_SECONDARY_DARK,)
META_TAB_BACKGROUND = rx.color_mode_cond("#FFFFFF","#F7F8FC",)

# ============================================================
# COR POR EIXO
# ============================================================

def get_eixo_color( eixo: rx.Var[str], ):
    """Retorna a cor correspondente ao eixo da meta."""
    return rx.cond(
        eixo == "Universo SP",
        COLOR_UNIVERSO,
        rx.cond( eixo == "Viver São Paulo", COLOR_VIVER,
            rx.cond( eixo == "Cidade Empreendedora", COLOR_CIDADE,
                rx.cond( eixo == "Capital do Futuro", COLOR_CAPITAL, "#288140",),
            ),
        ),
    )

# ============================================================
# CABEÇALHO SIMPLES
# ============================================================

def meta_list_intro() -> rx.Component:
    """
    Mantém somente a identificação da página.  Os controles vivem no dock flutuante.
    """
    return rx.vstack(
        rx.text( "METAS", color=CARD_TEXT, font_family=FONT_FAMILY_SECUNDARY, font_size={ "initial": "2rem", "md": "2.4rem", }, line_height="1", ),
        rx.text( "Pesquise e selecione uma meta " "para visualizar sua ficha.", color=CARD_TEXT_SECONDARY, font_family=FONT_FAMILY_PRIMARY, font_size="0.82rem", ), spacing="2", align="start", width="100%",
        # ====================================================
        # ÂNCORA PARA VOLTAR AO TOPO
        # ====================================================
        id="meta-list-top",
        scroll_margin_top="1rem",
    )


# ============================================================
# CARD DA META
# ============================================================

def meta_list_item(meta: rx.Var[ MetaListItem],) -> rx.Component:
    """
    Card clicável inspirado no layout oficial
    das metas do Programa de Metas.

    Metas atingidas recebem uma marca d'água
    utilizando o SVG meta-atingida.svg.
    """

    eixo_color = (get_eixo_color( meta["eixo"]))

    return rx.link(
        rx.box(

            # =================================================
            # MARCA D'ÁGUA
            # =================================================

            rx.cond( meta["status"] == "Atingida/Concluída", rx.image( src="/svg/meta-atingida.svg", position="absolute", right="2px", bottom="0px", width="140px", height="150px", object_fit="contain", opacity="0.16", pointer_events="none", user_select="none", z_index="1",),
            ),
            # =================================================
            # ABA BRANCA DA META
            # =================================================

            rx.center(
                rx.text( "META ", meta["codigo"], color=eixo_color, font_family=( FONT_FAMILY_SECUNDARY), font_size="1.3rem", line_height="1", white_space="nowrap",), position="absolute", left="0", top="22px", width="108px", height="62px", background=( META_TAB_BACKGROUND), border_radius=( "0 0 24px 0" ), # Acima da marca d'água 
                z_index="3",
            ),
            # =================================================
            # CONTEÚDO
            # =================================================

            rx.vstack(

                # ------------------------------------------------
                # TÍTULO
                # ------------------------------------------------

                rx.text( meta["titulo"], color="#FFFFFF", font_family=( FONT_FAMILY_PRIMARY), font_size={ "initial": "0.88rem", "xl": "0.94rem",}, font_weight=( FONT_WEIGHT_SEMIBOLD), line_height="1.3", width="100%", ),

                # ------------------------------------------------
                # EIXO
                # ------------------------------------------------

                rx.hstack(
                    rx.icon( tag="layers", size=13, color=( "rgba(" "255,255,255,0.85" ")"),),

                    rx.text(meta["eixo"], color=("rgba(" "255,255,255,0.92" ")"), font_family=(FONT_FAMILY_PRIMARY), font_size="0.72rem", font_weight="500",), spacing="2", align="center", width="fit-content", background=("rgba(""255,255,255,0.14"")"), padding=("0.28rem 0.55rem"), border_radius="999px", margin_top="auto",),

                spacing="3", align="start", margin_left="126px", padding_top="1rem", padding_right="2.8rem", padding_bottom="1rem", min_height="133px", width=( "calc(100% - 126px)" ),

                # ---------------------------------------------
                # Mantém textos acima da marca d'água
                # ---------------------------------------------
                position="relative", z_index="2",
            ),

            # =================================================
            # CARD
            # =================================================
             position="relative", width="100%", height="100%", background=eixo_color, border_radius="0 56px 0 0",

            # Também corta qualquer parte do SVG
            # que ultrapasse o card.
            overflow="hidden",
            box_shadow=rx.color_mode_cond( ( "0 3px 10px " "rgba(26, 44, 70, 0.08)" ), ( "0 3px 14px " "rgba(0, 0, 0, 0.22)" ), ),
            transition=( "transform 0.2s ease, " "filter 0.2s ease, " "box-shadow 0.2s ease"),
            _hover={"transform": ("translateY(-3px)" ), "filter": ("brightness(1.04)" ), "box_shadow": ("0 7px 18px " "rgba(20, 34, 60, 0.16)"),},
        ),
        href=meta["url"],
        flex={"initial": "1 1 100%", "md": (  "1 1 calc(50% - 0.5rem)" ),},
        max_width={"initial": "100%", "md": (  "calc(50% - 0.5rem)" ),}, min_width="0", display="block", text_decoration="none", cursor="pointer",
    )


# ============================================================
# ESTADO VAZIO
# ============================================================

def empty_result() -> rx.Component:
    """
    Mensagem exibida quando os filtros
    não encontram metas.
    """

    return rx.center(
        rx.vstack(
            rx.center(
                rx.icon(tag="search-x", size=22, color=(  CARD_TEXT_SECONDARY ),), width="44px", height="44px", border_radius="50%", background=(rx.color_mode_cond( "#EEF3F7", "#202844",)),
            ),
            rx.text("Nenhuma meta encontrada", color=CARD_TEXT, font_family=(FONT_FAMILY_PRIMARY), font_weight=(FONT_WEIGHT_SEMIBOLD),),
            rx.text("Tente alterar a pesquisa " "ou limpar os filtros.", color=(CARD_TEXT_SECONDARY), font_family=(FONT_FAMILY_PRIMARY), font_size="0.85rem",), spacing="2", align="center",
        ),
        width="100%", padding="3rem 1rem",
    )


# ============================================================
# RESULTADOS
# ============================================================

def meta_list_results() -> rx.Component:
    """Lista filtrada de metas."""

    return rx.vstack(
        rx.hstack(
            rx.text(MetaListState .metas_filtradas .length(), " meta(s) encontrada(s)", color=(CARD_TEXT_SECONDARY), font_family=(FONT_FAMILY_PRIMARY), font_size="0.82rem",), width="100%", align="center",
        ),

        rx.cond(MetaListState .metas_filtradas .length() > 0,
            rx.grid(
                rx.foreach(MetaListState .metas_filtradas, meta_list_item,),
                columns={"initial": "1", "md": "2", "xl": "3",},spacing="4",width="100%",align_items="stretch",
            ), empty_result(),
        ), spacing="3", align="stretch", width="100%",
    )


# ============================================================
# LOADING
# ============================================================

def meta_list_loading() -> rx.Component:
    """Estado de carregamento da listagem."""

    return rx.center(
        rx.vstack(
            rx.spinner(size="3",),
            rx.text("Carregando metas...", color=(CARD_TEXT_SECONDARY), font_family=(FONT_FAMILY_PRIMARY),),
            spacing="3", align="center",
        ),
        width="100%", padding="4rem 1rem",
    )


# ============================================================
# ERRO
# ============================================================

def meta_list_error() -> rx.Component:
    """Erro de carregamento."""

    return rx.box(
        rx.hstack(
            rx.icon( tag="triangle-alert", size=18, color="#C62828",),
            rx.text( MetaListState .error_message, color="#C62828", font_family=(FONT_FAMILY_PRIMARY), font_size="0.9rem",),
            spacing="3", align="center",
        ),
        width="100%", padding="1rem", background=(rx.color_mode_cond("rgba(198, 40, 40, 0.06)","rgba(236, 32, 36, 0.10)",)), border_radius="10px",
    )

# ============================================================
# CONTEÚDO
# ============================================================

def meta_list_content() -> rx.Component:
    """Página de pesquisa e seleção das metas."""
    return rx.box(
        # ====================================================
        # DOCK FIXO
        # ====================================================
        meta_filter_dock(),
        # ====================================================
        # CONTEÚDO DA PÁGINA
        # ====================================================
        rx.vstack(
            meta_list_intro(),
            rx.cond( MetaListState.loading, meta_list_loading(),
                rx.cond( MetaListState .error_message != "", meta_list_error(), meta_list_results(),),
            ),
            spacing="5", align="stretch", width="100%",
        ),
        width="100%",
    )


# ============================================================
# PÁGINA
# ============================================================

def meta_list_page() -> rx.Component:
    """Página administrativa com a lista de metas."""

    return admin_layout(
        meta_list_content()
    )