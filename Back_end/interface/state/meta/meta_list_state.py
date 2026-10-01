import reflex as rx

from Back_end.access_api.metas.services.meta_list_service import (
    list_metas,
)


class MetaListState(rx.State):
    """Controla a listagem e a pesquisa de metas."""

    metas: list[dict[str, str]] = []
    search_text: str = ""

    loading: bool = False
    error_message: str = ""

    @rx.var
    def metas_filtradas(self) -> list[dict[str, str]]:
        """Filtra as metas por código ou título."""

        termo = self.search_text.strip().casefold()

        if not termo:
            return self.metas

        return [
            meta
            for meta in self.metas
            if (
                termo in meta["codigo"].casefold()
                or termo in meta["titulo"].casefold()
            )
        ]

    @rx.event
    def update_search_text(self, value: str):
        self.search_text = value

    @rx.event
    def load_metas(self):
        self.loading = True
        self.error_message = ""

        yield

        try:
            self.metas = list_metas()

        except Exception as error:
            print(f"Erro ao listar metas: {error}")
            self.error_message = (
                "Não foi possível carregar a lista de metas."
            )

        finally:
            self.loading = False