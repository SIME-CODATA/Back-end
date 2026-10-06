import reflex as rx

from Back_end.access_api.metas.services.meta_list_service import ( list_metas, MetaListItem,)




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
    regiao_filter: str = ""

    # ========================================================
    # INTERFACE
    # ========================================================

    loading: bool = False
    error_message: str = ""

    # ========================================================
    # OPÇÕES DOS FILTROS
    # ========================================================

    @rx.var
    def eixos_disponiveis( self,) -> list[str]:
        """Retorna todos os eixos presentes nas metas."""
        valores = {
            str(meta.get("eixo","",)).strip()
            for meta in self.metas
            if str(meta.get("eixo","",)).strip()
        }
        return sorted( valores, key=str.casefold, )

    @rx.var
    def orgaos_disponiveis( self,) -> list[str]:
        """Retorna todos os órgãos presentes nas metas."""

        valores: set[str] = set()
        for meta in self.metas:
            orgaos = meta.get("orgaos",[],)

            if not isinstance(orgaos,list,):
                continue

            for orgao in orgaos:
                if orgao:
                    valores.add(str(orgao))

        return sorted(valores,key=str.casefold,)

    @rx.var
    def temas_disponiveis( self,) -> list[str]:
        """Retorna os temas das metas."""

        valores: set[str] = set()
        for meta in self.metas:
            temas = meta.get("temas",[],)
            if not isinstance(temas, list,):
                continue

            for tema in temas:
                if tema:
                    valores.add(str(tema))

        return sorted(valores,key=str.casefold,)

    @rx.var
    def regioes_disponiveis( self,) -> list[str]:
        """Retorna as regiões encontradas nas metas."""

        valores: set[str] = set()
        for meta in self.metas:
            regioes = meta.get("regioes",[],)

            if not isinstance(regioes,list,):
                continue

            for regiao in regioes:
                if regiao:
                    valores.add(str(regiao))

        return sorted(valores,key=str.casefold,)

    # ========================================================
    # RESULTADO DOS FILTROS
    # ========================================================

    @rx.var
    def metas_filtradas( self,) -> list[MetaListItem]:
        """
        Combina pesquisa textual com os quatro filtros.
        """

        termo = ( self.search_text .strip() .casefold() )
        resultado: list [ MetaListItem] = []

        for meta in self.metas:
            codigo = str (meta.get("codigo","",))
            titulo = str (meta.get("titulo","",))
            eixo = str (meta.get("eixo","",))
            orgaos = meta.get ("orgaos",[],)
            temas = meta.get ("temas",[],)
            regioes = meta.get ("regioes",[],)
            if not isinstance(orgaos,list,):
                orgaos = []

            if not isinstance(temas,list,):
                temas = []

            if not isinstance(regioes,list,):
                regioes = []

            # ----------------------------------------------
            # Pesquisa por código ou título
            # ----------------------------------------------

            if termo:
                encontrou_texto = (
                    termo
                    in codigo.casefold()

                    or termo
                    in titulo.casefold()
                )

                if not encontrou_texto:
                    continue

            # ----------------------------------------------
            # Eixo
            # ----------------------------------------------

            if ( self.eixo_filter and eixo != self.eixo_filter ):
                continue

            # ----------------------------------------------
            # Órgão
            # ----------------------------------------------

            if ( self.orgao_filter and self.orgao_filter not in orgaos ):
                continue

            # ----------------------------------------------
            # Tema
            # ----------------------------------------------

            if ( self.tema_filter and self.tema_filter not in temas ):
                continue

            # ----------------------------------------------
            # Região
            # ----------------------------------------------

            if ( self.regiao_filter and self.regiao_filter not in regioes ):
                continue

            resultado.append( meta )

        return resultado

    # ========================================================
    # EVENTOS DE BUSCA
    # ========================================================

    @rx.event
    def update_search_text( self, value: str, ):
        self.search_text = value

    # ========================================================
    # EVENTOS DOS FILTROS
    # ========================================================

    @rx.event
    def update_eixo_filter( self, value: str, ):
        self.eixo_filter = value

    @rx.event
    def update_orgao_filter(self,value: str, ):
        self.orgao_filter = value

    @rx.event
    def update_tema_filter(self,value: str,):
        self.tema_filter = value

    @rx.event
    def update_regiao_filter(self,value: str,):
        self.regiao_filter = value

    @rx.event
    def clear_filters(self):
        """Limpa pesquisa e filtros selecionados."""

        self.search_text = ""

        self.eixo_filter = ""
        self.orgao_filter = ""
        self.tema_filter = ""
        self.regiao_filter = ""

    # ========================================================
    # CARREGAMENTO
    # ========================================================

    @rx.event
    def load_metas(self):
        """Carrega as metas disponíveis no banco local."""

        self.loading = True
        self.error_message = ""

        # Ao entrar novamente na página,
        # iniciamos com os filtros limpos.
        self.search_text = ""
        self.eixo_filter = ""
        self.orgao_filter = ""
        self.tema_filter = ""
        self.regiao_filter = ""

        yield

        try:
            self.metas = list_metas()

        except Exception as error:
            print("Erro ao listar metas: "f"{error}")
            self.error_message = ( "Não foi possível carregar " "a lista de metas.")

        finally:
            self.loading = False