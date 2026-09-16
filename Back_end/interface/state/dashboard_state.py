from datetime import timedelta, timezone

import reflex as rx

from Back_end.access_api.metas.services.dashboard_service import (
    get_dashboard_summary,
)

from Back_end.access_api.metas.services.sync_service import sync_metas

SAO_PAULO_TIMEZONE = timezone(timedelta(hours=-3))


class DashboardState(rx.State):
    """Controla os dados exibidos no dashboard."""

    total_metas: int = 0
    total_temas: int = 0
    metas_ativas: int = 0

    metas_por_eixo: list[dict[str, str | int]] = []

    ultima_sincronizacao: str = "Sem atualização"

    loading: bool = False
    error_message: str = ""
    sync_message: str = ""

    @rx.event
    def load_summary(self):
        """Carrega os dados resumidos do dashboard."""

        self.loading = True
        self.error_message = ""

        yield

        try:
            summary = get_dashboard_summary()

            self.total_metas = summary["total_metas"]
            self.total_temas = summary["total_temas"]
            self.metas_ativas = summary["metas_ativas"]

            self.metas_por_eixo = [
                {
                    "nome": eixo,
                    "quantidade": quantidade,
                }
                for eixo, quantidade in summary["metas_por_eixo"].items()
            ]

            synced_at = summary["ultima_sincronizacao"]

            if synced_at is not None:
                local_time = synced_at.astimezone(
                    SAO_PAULO_TIMEZONE
                )

                self.ultima_sincronizacao = local_time.strftime(
                    "%d/%m/%Y %H:%M"
                )
            else:
                self.ultima_sincronizacao = "Sem atualização"

        except Exception as error:
            print(f"Erro ao carregar dashboard: {error}")

            self.error_message = (
                "Não foi possível carregar os dados do dashboard."
            )

        finally:
            self.loading = False

    @rx.event
    def refresh_data(self):
        """Sincroniza os dados com o SMAE e atualiza o dashboard."""

        self.loading = True
        self.error_message = ""
        self.sync_message = ""

        yield

        try:
            result = sync_metas()

            summary = get_dashboard_summary()

            self.total_metas = summary["total_metas"]
            self.total_temas = summary["total_temas"]
            self.metas_ativas = summary["metas_ativas"]

            self.metas_por_eixo = [
                {
                    "nome": eixo,
                    "quantidade": quantidade,
                }
                for eixo, quantidade in summary["metas_por_eixo"].items()
            ]

            synced_at = summary["ultima_sincronizacao"]

            if synced_at is not None:
                local_time = synced_at.astimezone(
                    SAO_PAULO_TIMEZONE
                )

                self.ultima_sincronizacao = local_time.strftime(
                    "%d/%m/%Y %H:%M"
                )
            else:
                self.ultima_sincronizacao = "Sem atualização"

            self.sync_message = (
                f"Atualização concluída: "
                f"{result.inserted} novas, "
                f"{result.updated} atualizadas e "
                f"{result.unchanged} sem alterações."
            )

        except Exception as error:
            print(f"Erro ao sincronizar dashboard: {error}")

            self.error_message = (
                "Não foi possível atualizar os dados do SMAE."
            )

        finally:
            self.loading = False