from datetime import timedelta, timezone
from decimal import Decimal

import reflex as rx

from Back_end.access_api.metas.services.dashboard_service import (
    get_dashboard_summary,
)
from Back_end.access_api.metas.services.pdm_sync_service import (
    sync_pdm,
)


SAO_PAULO_TIMEZONE = timezone(
    timedelta(hours=-3)
)


SITUACAO_ORDER = [
    "Dentro do cronograma",
    "Risco baixo/médio",
    "Risco alto/muito alto",
    "Meta atingida",
    "Meta comprometida",
]


PRAZO_ORDER = [
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


def _format_brl(
    value: Decimal | int | float | None,
) -> str:
    """Formata um valor monetário no padrão brasileiro."""

    decimal_value = Decimal(
        str(value or 0)
    )

    formatted = (
        f"{decimal_value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    return f"R$ {formatted}"


class DashboardState(rx.State):
    """Controla os dados exibidos no dashboard."""

    # --------------------------------------------------
    # Indicadores básicos
    # --------------------------------------------------

    total_metas: int = 0
    total_temas: int = 0
    metas_ativas: int = 0

    ultima_sincronizacao: str = (
        "Sem atualização"
    )

    # --------------------------------------------------
    # Andamento
    # --------------------------------------------------

    metas_atingidas: int = 0
    metas_em_progresso: int = 0
    metas_em_planejamento: int = 0

    percentual_atingidas: float = 0.0
    percentual_em_progresso: float = 0.0
    percentual_em_planejamento: float = 0.0

    # --------------------------------------------------
    # Eixos
    # --------------------------------------------------

    metas_por_eixo: list[
        dict[str, str | int]
    ] = []

    eixos_resumo: list[
        dict[str, str | int | float]
    ] = []

    # --------------------------------------------------
    # Situação / prazo
    # --------------------------------------------------

    situacao_resumo: list[
        dict[str, str | int]
    ] = []

    prazo_resumo: list[
        dict[str, str | int]
    ] = []

    # --------------------------------------------------
    # Orçamento
    # --------------------------------------------------

    orcamento_previsao: str = "R$ 0,00"
    orcamento_empenhado: str = "R$ 0,00"
    orcamento_liquidado: str = "R$ 0,00"

    percentual_empenhado: float = 0.0
    percentual_liquidado: float = 0.0

    metas_com_previsao: int = 0
    metas_com_empenho: int = 0
    metas_com_liquidacao: int = 0

    # --------------------------------------------------
    # Interface
    # --------------------------------------------------

    loading: bool = False
    error_message: str = ""
    sync_message: str = ""

    def _apply_summary(
        self,
        summary: dict,
    ) -> None:
        """
        Aplica o resumo retornado pelo service
        ao estado da interface.
        """

        self.total_metas = summary[
            "total_metas"
        ]

        self.total_temas = summary[
            "total_temas"
        ]

        self.metas_ativas = summary[
            "metas_ativas"
        ]

        # ----------------------------------------------
        # Andamento
        # ----------------------------------------------

        self.metas_atingidas = summary[
            "metas_atingidas"
        ]

        self.metas_em_progresso = summary[
            "metas_em_progresso"
        ]

        self.metas_em_planejamento = summary[
            "metas_em_planejamento"
        ]

        self.percentual_atingidas = summary[
            "percentual_atingidas"
        ]

        self.percentual_em_progresso = summary[
            "percentual_em_progresso"
        ]

        self.percentual_em_planejamento = summary[
            "percentual_em_planejamento"
        ]

        # ----------------------------------------------
        # Eixos
        # ----------------------------------------------

        self.eixos_resumo = [
            {
                "nome": item["nome"],
                "quantidade": item[
                    "quantidade"
                ],
                "atingidas": item[
                    "atingidas"
                ],
                "em_progresso": item[
                    "em_progresso"
                ],
                "em_planejamento": item[
                    "em_planejamento"
                ],
                "percentual_atingidas": item[
                    "percentual_atingidas"
                ],
            }
            for item in summary[
                "eixos_resumo"
            ]
        ]

        # Mantemos enquanto o layout antigo existir.
        self.metas_por_eixo = [
            {
                "nome": eixo,
                "quantidade": quantidade,
            }
            for eixo, quantidade in summary[
                "metas_por_eixo"
            ].items()
        ]

        # ----------------------------------------------
        # Situação
        # ----------------------------------------------

        situacao = summary["situacao"]

        self.situacao_resumo = [
            {
                "nome": nome,
                "quantidade": situacao.get(
                    nome,
                    0,
                ),
            }
            for nome in SITUACAO_ORDER
        ]

        # ----------------------------------------------
        # Prazo
        # ----------------------------------------------

        prazo = summary["prazo"]

        self.prazo_resumo = [
            {
                "nome": nome,
                "quantidade": prazo.get(
                    nome,
                    0,
                ),
            }
            for nome in PRAZO_ORDER
        ]

        # ----------------------------------------------
        # Orçamento
        # ----------------------------------------------

        orcamento = summary["orcamento"]

        self.orcamento_previsao = _format_brl(
            orcamento["previsao"]
        )

        self.orcamento_empenhado = _format_brl(
            orcamento["empenhado"]
        )

        self.orcamento_liquidado = _format_brl(
            orcamento["liquidado"]
        )

        self.percentual_empenhado = orcamento[
            "percentual_empenhado"
        ]

        self.percentual_liquidado = orcamento[
            "percentual_liquidado"
        ]

        self.metas_com_previsao = orcamento[
            "metas_com_previsao"
        ]

        self.metas_com_empenho = orcamento[
            "metas_com_empenho"
        ]

        self.metas_com_liquidacao = orcamento[
            "metas_com_liquidacao"
        ]

        # ----------------------------------------------
        # Última sincronização
        # ----------------------------------------------

        synced_at = summary[
            "ultima_sincronizacao"
        ]

        if synced_at is not None:
            local_time = synced_at.astimezone(
                SAO_PAULO_TIMEZONE
            )

            self.ultima_sincronizacao = (
                local_time.strftime(
                    "%d/%m/%Y %H:%M"
                )
            )

        else:
            self.ultima_sincronizacao = (
                "Sem atualização"
            )

    @rx.event
    def load_summary(self):
        """Carrega os dados do dashboard."""

        self.loading = True
        self.error_message = ""

        yield

        try:
            summary = (
                get_dashboard_summary()
            )

            self._apply_summary(
                summary
            )

        except Exception as error:
            print(
                f"Erro ao carregar dashboard: "
                f"{error}"
            )

            self.error_message = (
                "Não foi possível carregar "
                "os dados do dashboard."
            )

        finally:
            self.loading = False

    @rx.event
    def refresh_data(self):
        """
        Executa a sincronização completa com o SMAE
        e recarrega os indicadores.
        """

        self.loading = True
        self.error_message = ""
        self.sync_message = ""

        yield

        try:
            result = sync_pdm()

            summary = (
                get_dashboard_summary()
            )

            self._apply_summary(
                summary
            )

            alteracoes_iniciativas = (
                result.iniciativas_criadas
                + result.iniciativas_atualizadas
            )

            alteracoes_orcamento = (
                result.orcamentos_criados
                + result.orcamentos_atualizados
            )

            self.sync_message = (
                "Atualização concluída: "
                f"{result.metas_novas} novas metas, "
                f"{result.metas_atualizadas} metas "
                "alteradas no catálogo, "
                f"{result.detalhes_atualizados} "
                "detalhes atualizados, "
                f"{alteracoes_orcamento} "
                "orçamentos alterados e "
                f"{alteracoes_iniciativas} "
                "iniciativas alteradas."
            )

        except Exception as error:
            print(
                f"Erro ao sincronizar dashboard: "
                f"{error}"
            )

            self.error_message = (
                "Não foi possível atualizar "
                "os dados do SMAE."
            )

        finally:
            self.loading = False