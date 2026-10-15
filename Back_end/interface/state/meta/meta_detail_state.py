from typing import TypedDict

import reflex as rx

from Back_end.access_api.metas.services.meta_detail_service import (
    get_meta_detail_by_codigo,
    list_meta_print_options,
)


# ============================================================
# TIPAGEM
# ============================================================

class MetaObraItem(TypedDict):
    codigo: str
    nome: str
    status: str
    percentual: str
    tipo: str
    equipamento: str
    subprefeituras: str


class MetaProjetoItem(TypedDict):
    codigo: str
    nome: str
    portfolio: str
    etapa: str


class MetaPrintOption(TypedDict):
    codigo: str
    titulo: str
    selected: bool


# ============================================================
# HELPERS
# ============================================================

def format_percentual(
    value,
) -> str:
    if (
        value is None
        or value == ""
    ):
        return "Não informado"

    text = str(value).strip()

    if text.endswith("%"):
        return text

    return f"{text}%"


def format_meta_obra(
    obra: dict,
) -> MetaObraItem:

    tipo = (
        obra.get(
            "tipo_intervencao"
        )
        or {}
    )

    if not isinstance(
        tipo,
        dict,
    ):
        tipo = {}

    equipamento = (
        obra.get(
            "equipamento"
        )
        or {}
    )

    if not isinstance(
        equipamento,
        dict,
    ):
        equipamento = {}

    subprefeituras_raw = (
        obra.get(
            "subprefeituras"
        )
        or []
    )

    subprefeituras: list[str] = []

    for subprefeitura in (
        subprefeituras_raw
    ):
        if not isinstance(
            subprefeitura,
            dict,
        ):
            continue

        descricao = (
            subprefeitura.get(
                "descricao"
            )
        )

        if descricao:
            subprefeituras.append(
                str(descricao)
            )

    return {
        "codigo": str(
            obra.get("codigo")
            or ""
        ),

        "nome": str(
            obra.get("nome")
            or "Obra sem nome"
        ),

        "status": str(
            obra.get("status")
            or "Não informado"
        ),

        "percentual": (
            format_percentual(
                obra.get(
                    "percentual_concluido"
                )
            )
        ),

        "tipo": str(
            tipo.get("nome")
            or "Não informado"
        ),

        "equipamento": str(
            equipamento.get("nome")
            or "Não informado"
        ),

        "subprefeituras": (
            ", ".join(
                sorted(
                    set(subprefeituras),
                    key=str.casefold,
                )
            )
            or "Não informado"
        ),
    }


def format_meta_projeto(
    projeto: dict,
) -> MetaProjetoItem:

    portfolio = (
        projeto.get("portfolio")
        or {}
    )

    if not isinstance(
        portfolio,
        dict,
    ):
        portfolio = {}

    etapa = (
        projeto.get(
            "projeto_etapa"
        )
        or {}
    )

    if not isinstance(
        etapa,
        dict,
    ):
        etapa = {}

    return {
        "codigo": str(
            projeto.get("codigo")
            or ""
        ),

        "nome": str(
            projeto.get("nome")
            or "Projeto sem nome"
        ),

        "portfolio": str(
            portfolio.get("titulo")
            or "Não informado"
        ),

        "etapa": str(
            etapa.get("descricao")
            or "Não informado"
        ),
    }


def format_meta_relacionada(
    relacao: dict,
) -> str:

    codigo = str(
        relacao.get(
            "meta_codigo"
        )
        or ""
    )

    titulo = str(
        relacao.get(
            "meta_titulo"
        )
        or ""
    )

    if codigo and titulo:
        return (
            f"Meta {codigo} | "
            f"{titulo}"
        )

    if titulo:
        return titulo

    if codigo:
        return f"Meta {codigo}"

    return "Meta relacionada"


# ============================================================
# STATE
# ============================================================

class MetaDetailState(rx.State):
    """Controla a Ficha da Meta."""

    # ========================================================
    # META
    # ========================================================

    codigo_atual: str = ""
    smae_id: int = 0

    titulo: str = ""
    eixo: str = ""
    contexto: str = ""

    # ========================================================
    # NAVEGAÇÃO
    # ========================================================

    codigo_anterior: str = ""
    codigo_proximo: str = ""

    # ========================================================
    # STATUS
    # ========================================================

    andamento: str = ""
    situacao: str = ""
    prazo: str = ""

    # ========================================================
    # CLASSIFICAÇÕES
    # ========================================================

    orgaos: list[str] = []
    ods: list[str] = []
    tags: list[str] = []

    # ========================================================
    # INICIATIVAS
    # ========================================================

    iniciativas: list[str] = []

    # ========================================================
    # ORÇAMENTO
    # ========================================================

    previsao: str = "Não informado"
    empenhado: str = "Não informado"
    liquidado: str = "Não informado"

    # ========================================================
    # REGIONALIZAÇÃO
    # ========================================================

    regioes: list[str] = []
    subprefeituras: list[str] = []

    # ========================================================
    # RELACIONADOS
    # ========================================================

    obras: list[MetaObraItem] = []
    projetos: list[MetaProjetoItem] = []
    metas_relacionadas: list[str] = []

    # ========================================================
    # INTERFACE
    # ========================================================

    loading: bool = True
    ficha_encontrada: bool = False
    error_message: str = ""

    # ========================================================
    # BUSCA
    # ========================================================

    search_open: bool = False
    search_codigo: str = ""
    search_error: str = ""

    # ========================================================
    # SELETOR DE IMPRESSÃO
    # ========================================================

    print_selector_open: bool = False

    print_options: list[
        MetaPrintOption
    ] = []

    print_search_text: str = ""

    print_error: str = ""

    # ========================================================
    # OPÇÕES FILTRADAS
    # ========================================================

    @rx.var
    def print_options_filtradas(
        self,
    ) -> list[MetaPrintOption]:
        """Filtra metas do seletor de impressão."""

        termo = (
            self.print_search_text
            .strip()
            .casefold()
        )

        if not termo:
            return self.print_options

        return [
            option
            for option in self.print_options
            if (
                termo
                in option["codigo"].casefold()

                or termo
                in option["titulo"].casefold()
            )
        ]

    @rx.var
    def print_selected_count(
        self,
    ) -> int:
        """Quantidade de fichas selecionadas."""

        return sum(
            1
            for option in self.print_options
            if option["selected"]
        )

    # ========================================================
    # CARREGAMENTO
    # ========================================================

    @rx.event
    def load_meta(self):
        self.loading = True
        self.ficha_encontrada = False
        self.error_message = ""

        self.codigo_anterior = ""
        self.codigo_proximo = ""

        self.titulo = ""
        self.eixo = ""
        self.contexto = ""

        self.andamento = ""
        self.situacao = ""
        self.prazo = ""

        self.orgaos = []
        self.ods = []
        self.tags = []

        self.iniciativas = []

        self.regioes = []
        self.subprefeituras = []

        self.obras = []
        self.projetos = []
        self.metas_relacionadas = []

        self.previsao = "Não informado"
        self.empenhado = "Não informado"
        self.liquidado = "Não informado"

        yield

        try:
            codigo = (
                self.router.url.path
                .rstrip("/")
                .rsplit("/", 1)[-1]
            )

            self.codigo_atual = codigo

            ficha = (
                get_meta_detail_by_codigo(
                    codigo
                )
            )

            if ficha is None:
                return

            self.codigo_atual = (
                ficha["codigo"]
            )

            self.smae_id = (
                ficha["smae_id"]
                or 0
            )

            self.titulo = (
                ficha["titulo"]
            )

            self.eixo = (
                ficha["eixo"]
            )

            self.contexto = (
                ficha["contexto"]
            )

            self.codigo_anterior = (
                ficha.get(
                    "codigo_anterior"
                )
                or ""
            )

            self.codigo_proximo = (
                ficha.get(
                    "codigo_proximo"
                )
                or ""
            )

            self.andamento = (
                ficha["andamento"]
                or ""
            )

            self.situacao = (
                ficha["situacao"]
                or ""
            )

            self.prazo = (
                ficha["prazo"]
                or ""
            )

            self.orgaos = [
                (
                    orgao["sigla"]
                    or orgao["descricao"]
                )
                for orgao
                in ficha["orgaos"]
            ]

            self.ods = (
                ficha["ods"]
                or []
            )

            self.tags = (
                ficha["tags"]
                or []
            )

            self.iniciativas = [
                (
                    f"{iniciativa['codigo']} | "
                    f"{iniciativa['titulo']}"
                )
                for iniciativa
                in ficha["iniciativas"]
            ]

            orcamento = (
                ficha["orcamento"]
                or {}
            )

            self.previsao = (
                orcamento.get(
                    "previsao"
                )
                or "Não informado"
            )

            self.empenhado = (
                orcamento.get(
                    "empenhado"
                )
                or "Não informado"
            )

            self.liquidado = (
                orcamento.get(
                    "liquidado"
                )
                or "Não informado"
            )

            self.regioes = (
                ficha.get(
                    "regioes"
                )
                or []
            )

            self.subprefeituras = [
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
            ]

            self.obras = [
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
            ]

            self.projetos = [
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
            ]

            self.metas_relacionadas = [
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
            ]

            self.ficha_encontrada = True

        except Exception as error:
            print(
                "Erro ao carregar ficha: "
                f"{error}"
            )

            self.error_message = (
                "Não foi possível carregar "
                "a ficha da meta."
            )

        finally:
            self.loading = False

    # ========================================================
    # BUSCA
    # ========================================================

    @rx.event
    def open_search(self):
        self.search_codigo = ""
        self.search_error = ""
        self.search_open = True


    @rx.event
    def close_search(self):
        self.search_open = False


    @rx.event
    def go_to_meta(self):
        codigo = (
            self.search_codigo
            .strip()
        )

        if not codigo.isdigit():
            self.search_error = (
                "Digite o número da meta."
            )
            return

        self.search_open = False

        return rx.redirect(
            f"/admin/metas/"
            f"{codigo.zfill(3)}"
        )


    @rx.event
    def update_search_codigo(
        self,
        value: str,
    ):
        self.search_codigo = value
        self.search_error = ""

    # ========================================================
    # NAVEGAÇÃO
    # ========================================================

    @rx.event
    def go_to_previous_meta(self):
        if not self.codigo_anterior:
            return

        return rx.redirect(
            f"/admin/metas/"
            f"{self.codigo_anterior}"
        )


    @rx.event
    def go_to_next_meta(self):
        if not self.codigo_proximo:
            return

        return rx.redirect(
            f"/admin/metas/"
            f"{self.codigo_proximo}"
        )

    # ========================================================
    # SELETOR DE IMPRESSÃO
    # ========================================================

    @rx.event
    def open_print_selector(self):
        """Abre seleção das fichas para impressão."""

        self.print_search_text = ""
        self.print_error = ""

        options = (
            list_meta_print_options()
        )

        self.print_options = [
            {
                "codigo": option["codigo"],
                "titulo": option["titulo"],
                "selected": (
                    option["codigo"]
                    == self.codigo_atual
                ),
            }
            for option in options
        ]

        self.print_selector_open = True


    @rx.event
    def close_print_selector(self):
        self.print_selector_open = False
        self.print_error = ""


    @rx.event
    def update_print_search(
        self,
        value: str,
    ):
        self.print_search_text = value


    @rx.event
    def set_print_meta_selected(
        self,
        codigo: str,
        selected: bool,
    ):
        """Marca ou desmarca uma ficha."""

        novos: list[
            MetaPrintOption
        ] = []

        for option in self.print_options:

            item: MetaPrintOption = {
                "codigo": option["codigo"],
                "titulo": option["titulo"],
                "selected": option["selected"],
            }

            if (
                item["codigo"]
                == codigo
            ):
                item["selected"] = (
                    selected
                )

            novos.append(item)

        self.print_options = novos

        self.print_error = ""


    @rx.event
    def select_all_print_metas(self):
        self.print_options = [
            {
                "codigo": option["codigo"],
                "titulo": option["titulo"],
                "selected": True,
            }
            for option in self.print_options
        ]

        self.print_error = ""


    @rx.event
    def clear_print_selection(self):
        self.print_options = [
            {
                "codigo": option["codigo"],
                "titulo": option["titulo"],
                "selected": False,
            }
            for option in self.print_options
        ]

        self.print_error = ""


    @rx.event
    def open_print_document(self):
        """
        Abre um documento único contendo
        todas as fichas selecionadas.
        """

        codigos = [
            option["codigo"]
            for option in self.print_options
            if option["selected"]
        ]

        if not codigos:
            self.print_error = (
                "Selecione pelo menos uma ficha."
            )
            return

        caminho = ",".join(
            codigos
        )

        self.print_selector_open = False

        return rx.call_script(
            "window.open("
            f"'/imprimir/metas/{caminho}', "
            "'_blank'"
            ");"
        )