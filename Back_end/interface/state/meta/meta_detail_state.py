import reflex as rx

from Back_end.access_api.metas.services.meta_detail_service import (
    get_meta_detail_by_codigo,
)


class MetaDetailState(rx.State):
    """Controla os dados da ficha exibida na página."""

    codigo_atual: str = ""
    titulo: str = ""
    eixo: str = ""
    contexto: str = ""

    andamento: str = ""
    situacao: str = ""
    prazo: str = ""

    orgaos: list[str] = []
    ods: list[str] = []
    iniciativas: list[str] = []

    previsao: str = "Não informado"
    empenhado: str = "Não informado"
    liquidado: str = "Não informado"

    loading: bool = True
    ficha_encontrada: bool = False
    error_message: str = ""
    
    search_open: bool = False
    search_codigo: str = ""
    search_error: str = ""

    @rx.event
    def load_meta(self):
        """Carrega a meta correspondente ao código da URL."""

        self.loading = True
        self.ficha_encontrada = False
        self.error_message = ""

        yield

        try:
            # Exemplo: /metas/001 → 001
            codigo = (
                self.router.url.path
                .rstrip("/")
                .rsplit("/", 1)[-1]
            )

            ficha = get_meta_detail_by_codigo(codigo)

            if ficha is None:
                self.codigo_atual = codigo
                return

            self.codigo_atual = ficha["codigo"]
            self.titulo = ficha["titulo"]
            self.eixo = ficha["eixo"]
            self.contexto = ficha["contexto"]

            self.andamento = ficha["andamento"]
            self.situacao = ficha["situacao"]
            self.prazo = ficha["prazo"]

            self.orgaos = [
                orgao["sigla"] or orgao["descricao"]
                for orgao in ficha["orgaos"]
            ]

            self.ods = ficha["ods"]

            self.iniciativas = [
                (
                    f"{iniciativa['codigo']} | "
                    f"{iniciativa['titulo']}"
                )
                for iniciativa in ficha["iniciativas"]
            ]

            orcamento = ficha["orcamento"] or {}

            self.previsao = (
                orcamento.get("previsao")
                or "Não informado"
            )

            self.empenhado = (
                orcamento.get("empenhado")
                or "Não informado"
            )

            self.liquidado = (
                orcamento.get("liquidado")
                or "Não informado"
            )

            self.ficha_encontrada = True

        except Exception as error:
            print(f"Erro ao carregar ficha: {error}")

            self.error_message = (
                "Não foi possível carregar a ficha da meta."
            )

        finally:
            self.loading = False
            
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
        codigo = self.search_codigo.strip()

        if not codigo.isdigit():
            self.search_error = "Digite o número da meta."
            return

        self.search_open = False

        return rx.redirect(f"/metas/{codigo.zfill(3)}")
    
    @rx.event
    def update_search_codigo(self, value: str):
        self.search_codigo = value
        self.search_error = ""