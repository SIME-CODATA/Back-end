from dataclasses import dataclass

from Back_end.access_api.metas.services.equipe_sync_service import ( sync_equipes_from_raw_detail,)
from Back_end.access_api.metas.services.iniciativa_sync_service import ( sync_iniciativas,)
from Back_end.access_api.metas.services.orgao_sync_service import ( sync_orgaos_from_raw_detail,)
from Back_end.access_api.metas.services.sync_service import ( sync_all_meta_details, sync_metas,)
from Back_end.access_api.metas.services.tag_sync_service import ( sync_tags_from_raw_detail,)


@dataclass(frozen=True)
class PdmSyncResult:
    """Resumo da sincronização completa do PDM."""

    metas_novas: int
    metas_atualizadas: int

    detalhes_atualizados: int

    orcamentos_criados: int
    orcamentos_atualizados: int

    tags_criadas: int
    vinculos_tags_criados: int

    orgaos_criados: int
    vinculos_orgaos_criados: int

    vinculos_equipes_criados: int

    iniciativas_criadas: int
    iniciativas_atualizadas: int


def sync_pdm() -> PdmSyncResult:
    """
    Executa a sincronização completa do Programa de Metas.

    Ordem:
    1. catálogo de metas;
    2. detalhes completos;
    3. tags;
    4. órgãos;
    5. equipes;
    6. iniciativas.
    """

    metas_result = sync_metas()

    details_result = sync_all_meta_details()

    tags_result = sync_tags_from_raw_detail()

    orgaos_result = sync_orgaos_from_raw_detail()

    equipes_result = sync_equipes_from_raw_detail()

    iniciativas_result = sync_iniciativas()

    return PdmSyncResult(
        metas_novas=metas_result.inserted,
        metas_atualizadas=metas_result.updated,

        detalhes_atualizados=( details_result.metas_updated ),

        orcamentos_criados=( details_result.budgets_created ),
        orcamentos_atualizados=( details_result.budgets_updated ),

        tags_criadas=( tags_result.tags_criadas ),
        vinculos_tags_criados=( tags_result.vinculos_criados ),

        orgaos_criados=( orgaos_result.orgaos_criados ),
        vinculos_orgaos_criados=( orgaos_result.vinculos_orgaos_criados ),

        vinculos_equipes_criados=( equipes_result.vinculos_criados ),

        iniciativas_criadas=( iniciativas_result.iniciativas_criadas ),
        iniciativas_atualizadas=( iniciativas_result.iniciativas_atualizadas ),
    )