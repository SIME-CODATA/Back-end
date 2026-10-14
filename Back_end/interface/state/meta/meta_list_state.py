import reflex as rx

from Back_end.access_api.metas.services.meta_list_service import (
    list_metas,
    MetaListItem,
)


# ============================================================
# ORDENAÇÃO DOS FILTROS
# ============================================================

STATUS_ORDER = [
    "Em planejamento",
    "Em progresso",
    "Atingida/Concluída",
    "Não informado",
]


PROJECAO_ORDER = [
    "1º sem/2025",
    "2º sem/2025",
    "1º sem/2026",
    "2º sem/2026",
    "1º sem/2027",
    "2º sem/2027",
    "1º sem/2028",
    "2º sem/2028",
    "Sem previsão",
]


# ============================================================
# STATE
# ============================================================

class MetaListState(rx.State):
    """Controla listagem, pesquisa e filtros das metas."""

    # ========================================================
    # DADOS
    # ========================================================

    metas: list[MetaListItem] = []

    # ========================================================
    # BUSCA
    # ========================================================

    search_text: str = ""

    # ========================================================
    # FILTROS
    # ========================================================

    eixo_filter: str = ""

    orgao_filter: str = ""

    tema_filter: str = ""

    status_filter: str = ""

    projecao_filter: str = ""

    regiao_filter: str = ""

    # ========================================================
    # INTERFACE
    # ========================================================

    loading: bool = False

    error_message: str = ""

    filter_panel_open: bool = False

    more_filters_open: bool = False

    # ========================================================
    # OPÇÕES DOS FILTROS
    # ========================================================

    @rx.var
    def eixos_disponiveis(
        self,
    ) -> list[str]:
        """Retorna todos os eixos presentes nas metas."""

        valores = {
            str(
                meta.get(
                    "eixo",
                    "",
                )
            ).strip()

            for meta in self.metas

            if str(
                meta.get(
                    "eixo",
                    "",
                )
            ).strip()
        }

        return sorted(
            valores,
            key=str.casefold,
        )

    # --------------------------------------------------------
    # ÓRGÃOS
    # --------------------------------------------------------

    @rx.var
    def orgaos_disponiveis(
        self,
    ) -> list[str]:
        """Retorna todos os órgãos presentes nas metas."""

        valores: set[str] = set()

        for meta in self.metas:

            orgaos = meta.get(
                "orgaos",
                [],
            )

            if not isinstance(
                orgaos,
                list,
            ):
                continue

            for orgao in orgaos:

                if orgao:
                    valores.add(
                        str(orgao)
                    )

        return sorted(
            valores,
            key=str.casefold,
        )

    # --------------------------------------------------------
    # TEMAS
    # --------------------------------------------------------

    @rx.var
    def temas_disponiveis(
        self,
    ) -> list[str]:
        """Retorna os temas das metas."""

        valores: set[str] = set()

        for meta in self.metas:

            temas = meta.get(
                "temas",
                [],
            )

            if not isinstance(
                temas,
                list,
            ):
                continue

            for tema in temas:

                if tema:
                    valores.add(
                        str(tema)
                    )

        return sorted(
            valores,
            key=str.casefold,
        )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    @rx.var
    def status_disponiveis(
        self,
    ) -> list[str]:
        """Retorna os status de andamento existentes."""

        valores = {
            str(
                meta.get(
                    "status",
                    "",
                )
            ).strip()

            for meta in self.metas

            if str(
                meta.get(
                    "status",
                    "",
                )
            ).strip()
        }

        ordenados = [
            status

            for status
            in STATUS_ORDER

            if status in valores
        ]

        extras = sorted(
            valores
            - set(
                STATUS_ORDER
            ),
            key=str.casefold,
        )

        return (
            ordenados
            + extras
        )

    # --------------------------------------------------------
    # PROJEÇÃO
    # --------------------------------------------------------

    @rx.var
    def projecoes_disponiveis(
        self,
    ) -> list[str]:
        """Retorna as projeções de entrega existentes."""

        valores = {
            str(
                meta.get(
                    "projecao",
                    "",
                )
            ).strip()

            for meta in self.metas

            if str(
                meta.get(
                    "projecao",
                    "",
                )
            ).strip()
        }

        ordenados = [
            projecao

            for projecao
            in PROJECAO_ORDER

            if projecao in valores
        ]

        extras = sorted(
            valores
            - set(
                PROJECAO_ORDER
            ),
            key=str.casefold,
        )

        return (
            ordenados
            + extras
        )

    # --------------------------------------------------------
    # REGIÕES
    # --------------------------------------------------------

    @rx.var
    def regioes_disponiveis(
        self,
    ) -> list[str]:
        """Retorna as regiões encontradas nas metas."""

        valores: set[str] = set()

        for meta in self.metas:

            regioes = meta.get(
                "regioes",
                [],
            )

            if not isinstance(
                regioes,
                list,
            ):
                continue

            for regiao in regioes:

                if regiao:
                    valores.add(
                        str(regiao)
                    )

        return sorted(
            valores,
            key=str.casefold,
        )

    # ========================================================
    # CONTADOR DE FILTROS
    # ========================================================

    @rx.var
    def active_filter_count(
        self,
    ) -> int:
        """
        Quantidade de filtros ativos.

        A pesquisa textual não entra no contador.
        """

        filtros = [
            self.eixo_filter,
            self.orgao_filter,
            self.tema_filter,
            self.status_filter,
            self.projecao_filter,
            self.regiao_filter,
        ]

        return sum(
            1
            for filtro in filtros
            if filtro
        )

    # ========================================================
    # RESULTADO DOS FILTROS
    # ========================================================

    @rx.var
    def metas_filtradas(
        self,
    ) -> list[MetaListItem]:
        """
        Combina pesquisa textual com todos
        os filtros disponíveis.
        """

        termo = (
            self.search_text
            .strip()
            .casefold()
        )

        resultado: list[
            MetaListItem
        ] = []

        for meta in self.metas:

            codigo = str(
                meta.get(
                    "codigo",
                    "",
                )
            )

            titulo = str(
                meta.get(
                    "titulo",
                    "",
                )
            )

            eixo = str(
                meta.get(
                    "eixo",
                    "",
                )
            )

            status = str(
                meta.get(
                    "status",
                    "",
                )
            )

            projecao = str(
                meta.get(
                    "projecao",
                    "",
                )
            )

            orgaos = meta.get(
                "orgaos",
                [],
            )

            temas = meta.get(
                "temas",
                [],
            )

            regioes = meta.get(
                "regioes",
                [],
            )

            if not isinstance(
                orgaos,
                list,
            ):
                orgaos = []

            if not isinstance(
                temas,
                list,
            ):
                temas = []

            if not isinstance(
                regioes,
                list,
            ):
                regioes = []

            # =================================================
            # PESQUISA POR CÓDIGO OU TÍTULO
            # =================================================

            if termo:

                encontrou_texto = (
                    termo
                    in codigo.casefold()

                    or termo
                    in titulo.casefold()
                )

                if not encontrou_texto:
                    continue

            # =================================================
            # EIXO
            # =================================================

            if (
                self.eixo_filter
                and eixo
                != self.eixo_filter
            ):
                continue

            # =================================================
            # ÓRGÃO
            # =================================================

            if (
                self.orgao_filter
                and self.orgao_filter
                not in orgaos
            ):
                continue

            # =================================================
            # TEMA
            # =================================================

            if (
                self.tema_filter
                and self.tema_filter
                not in temas
            ):
                continue

            # =================================================
            # STATUS
            # =================================================

            if (
                self.status_filter
                and status
                != self.status_filter
            ):
                continue

            # =================================================
            # PROJEÇÃO
            # =================================================

            if (
                self.projecao_filter
                and projecao
                != self.projecao_filter
            ):
                continue

            # =================================================
            # REGIÃO
            # =================================================

            if (
                self.regiao_filter
                and self.regiao_filter
                not in regioes
            ):
                continue

            resultado.append(
                meta
            )

        return resultado

    # ========================================================
    # PESQUISA
    # ========================================================

    @rx.event
    def update_search_text(
        self,
        value: str,
    ):
        """Atualiza a pesquisa textual."""

        self.search_text = value

    # ========================================================
    # EVENTOS DOS FILTROS
    # ========================================================

    @rx.event
    def update_eixo_filter(
        self,
        value: str,
    ):
        self.eixo_filter = value


    @rx.event
    def update_orgao_filter(
        self,
        value: str,
    ):
        self.orgao_filter = value


    @rx.event
    def update_tema_filter(
        self,
        value: str,
    ):
        self.tema_filter = value


    @rx.event
    def update_status_filter(
        self,
        value: str,
    ):
        self.status_filter = value


    @rx.event
    def update_projecao_filter(
        self,
        value: str,
    ):
        self.projecao_filter = value


    @rx.event
    def update_regiao_filter(
        self,
        value: str,
    ):
        self.regiao_filter = value

    # ========================================================
    # PAINEL
    # ========================================================

    @rx.event
    def toggle_filter_panel(
        self,
    ):
        """Abre ou fecha o painel principal."""

        self.filter_panel_open = (
            not self.filter_panel_open
        )


    @rx.event
    def toggle_more_filters(
        self,
    ):
        """Abre ou fecha os filtros secundários."""

        self.more_filters_open = (
            not self.more_filters_open
        )

    # ========================================================
    # LIMPAR FILTROS
    # ========================================================

    @rx.event
    def clear_filters(
        self,
    ):
        """Limpa pesquisa e filtros selecionados."""

        self.search_text = ""

        self.eixo_filter = ""

        self.orgao_filter = ""

        self.tema_filter = ""

        self.status_filter = ""

        self.projecao_filter = ""

        self.regiao_filter = ""

    # ========================================================
    # VOLTAR AO TOPO
    # ========================================================

    @rx.event
    def scroll_to_top( self, ):
        """Retorna ao topo da listagem suavemente."""

        return rx.call_script(
            """
            const target = document.getElementById('meta-list-top');

            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
            """
    )

    # ========================================================
    # CARREGAMENTO
    # ========================================================

    @rx.event
    def load_metas(
        self,
    ):
        """Carrega as metas disponíveis no banco local."""

        self.loading = True

        self.error_message = ""

        # ----------------------------------------------------
        # Limpeza
        # ----------------------------------------------------

        self.search_text = ""

        self.eixo_filter = ""

        self.orgao_filter = ""

        self.tema_filter = ""

        self.status_filter = ""

        self.projecao_filter = ""

        self.regiao_filter = ""

        self.filter_panel_open = False

        self.more_filters_open = False

        yield

        try:
            self.metas = (
                list_metas()
            )

        except Exception as error:

            print(
                "Erro ao listar metas: "
                f"{error}"
            )

            self.error_message = (
                "Não foi possível carregar "
                "a lista de metas."
            )

        finally:
            self.loading = False