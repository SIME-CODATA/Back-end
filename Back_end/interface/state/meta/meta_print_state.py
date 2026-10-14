from typing import TypedDict

import reflex as rx

from Back_end.access_api.metas.services.meta_detail_service import (
    get_meta_detail_by_codigo,
)

from Back_end.interface.state.meta.meta_detail_state import (
    MetaObraItem,
    MetaProjetoItem,
    format_meta_obra,
    format_meta_projeto,
    format_meta_relacionada,
)


class MetaPrintFichaItem(TypedDict):
    codigo: str

    titulo: str
    eixo: str
    contexto: str

    andamento: str
    situacao: str
    prazo: str

    orgaos: list[str]
    ods: list[str]
    outras_tags: list[str]

    previsao: str
    empenhado: str
    liquidado: str

    iniciativas: list[str]

    regioes: list[str]
    subprefeituras: list[str]

    obras: list[MetaObraItem]
    projetos: list[MetaProjetoItem]

    metas_relacionadas: list[str]


def _build_print_ficha(
    ficha: dict,
) -> MetaPrintFichaItem:
    """Transforma a ficha completa em documento."""

    orcamento = (
        ficha.get(
            "orcamento"
        )
        or {}
    )

    todas_tags = (
        ficha.get(
            "tags"
        )
        or []
    )

    return {
        "codigo": (
            ficha["codigo"]
        ),

        "titulo": (
            ficha["titulo"]
            or ""
        ),

        "eixo": (
            ficha["eixo"]
            or ""
        ),

        "contexto": (
            ficha["contexto"]
            or ""
        ),

        "andamento": (
            ficha["andamento"]
            or ""
        ),

        "situacao": (
            ficha["situacao"]
            or ""
        ),

        "prazo": (
            ficha["prazo"]
            or ""
        ),

        "orgaos": [
            (
                orgao["sigla"]
                or orgao["descricao"]
            )
            for orgao
            in ficha["orgaos"]
        ],

        "ods": (
            ficha.get("ods")
            or []
        ),

        "outras_tags": [
            tag
            for tag in todas_tags
            if not str(tag).startswith(
                "ODS "
            )
        ],

        "previsao": (
            orcamento.get(
                "previsao"
            )
            or "Não informado"
        ),

        "empenhado": (
            orcamento.get(
                "empenhado"
            )
            or "Não informado"
        ),

        "liquidado": (
            orcamento.get(
                "liquidado"
            )
            or "Não informado"
        ),

        "iniciativas": [
            (
                f"{iniciativa['codigo']} | "
                f"{iniciativa['titulo']}"
            )
            for iniciativa
            in (
                ficha.get(
                    "iniciativas"
                )
                or []
            )
        ],

        "regioes": (
            ficha.get(
                "regioes"
            )
            or []
        ),

        "subprefeituras": [
            str(
                subprefeitura.get(
                    "descricao",
                    "",
                )
            )
            for subprefeitura
            in (
                ficha.get(
                    "subprefeituras"
                )
                or []
            )
            if (
                subprefeitura.get(
                    "descricao"
                )
            )
        ],

        "obras": [
            format_meta_obra(
                obra
            )
            for obra
            in (
                ficha.get("obras")
                or []
            )
            if isinstance(
                obra,
                dict,
            )
        ],

        "projetos": [
            format_meta_projeto(
                projeto
            )
            for projeto
            in (
                ficha.get(
                    "projetos"
                )
                or []
            )
            if isinstance(
                projeto,
                dict,
            )
        ],

        "metas_relacionadas": [
            format_meta_relacionada(
                relacao
            )
            for relacao
            in (
                ficha.get(
                    "metas_relacionadas"
                )
                or []
            )
            if isinstance(
                relacao,
                dict,
            )
        ],
    }


class MetaPrintState(rx.State):
    """Estado do documento imprimível."""

    fichas: list[
        MetaPrintFichaItem
    ] = []

    codigos_solicitados: list[str] = []

    detail_url: str = ""

    loading: bool = True

    ficha_encontrada: bool = False

    error_message: str = ""

    @rx.event
    def load_meta(self):
        """Carrega uma ou várias fichas."""

        self.loading = True

        self.ficha_encontrada = False

        self.error_message = ""

        self.fichas = []

        self.codigos_solicitados = []

        self.detail_url = ""

        yield

        try:
            trecho_url = (
                self.router.url.path
                .rstrip("/")
                .rsplit("/", 1)[-1]
            )

            codigos: list[str] = []

            for valor in trecho_url.split(","):

                codigo = (
                    valor
                    .strip()
                )

                if not codigo:
                    continue

                if codigo.isdigit():
                    codigo = (
                        codigo.zfill(3)
                    )

                if codigo not in codigos:
                    codigos.append(
                        codigo
                    )

            self.codigos_solicitados = (
                codigos
            )

            fichas: list[
                MetaPrintFichaItem
            ] = []

            for codigo in codigos:

                ficha = (
                    get_meta_detail_by_codigo(
                        codigo
                    )
                )

                if ficha is None:
                    continue

                fichas.append(
                    _build_print_ficha(
                        ficha
                    )
                )

            self.fichas = fichas

            if fichas:

                self.detail_url = (
                    "/admin/metas/"
                    f"{fichas[0]['codigo']}"
                )

                self.ficha_encontrada = (
                    True
                )

        except Exception as error:

            print(
                "Erro ao carregar documento "
                f"de impressão: {error}"
            )

            self.error_message = (
                "Não foi possível carregar "
                "as fichas para impressão."
            )

        finally:
            self.loading = False


    @rx.event
    def trigger_print(self):
        return rx.call_script(
            "window.print()"
        )


    @rx.event
    def close_window(self):
        return rx.call_script(
            "window.close()"
        )