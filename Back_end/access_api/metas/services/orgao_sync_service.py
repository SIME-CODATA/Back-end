from dataclasses import dataclass

import reflex as rx
from sqlmodel import select

from Back_end.access_api.metas.models.meta import Meta
from Back_end.access_api.metas.models.meta_orgao import MetaOrgao
from Back_end.access_api.metas.models.meta_pessoa import MetaPessoa
from Back_end.access_api.metas.models.orgao import Orgao
from Back_end.access_api.metas.models.pessoa import Pessoa


@dataclass(frozen=True)
class OrgaoSyncResult:
    """Resultado da normalização de órgãos e pessoas."""

    metas_processadas: int

    orgaos_criados: int
    orgaos_atualizados: int
    vinculos_orgaos_criados: int
    vinculos_orgaos_atualizados: int
    vinculos_orgaos_removidos: int

    pessoas_criadas: int
    pessoas_atualizadas: int
    vinculos_pessoas_criados: int
    vinculos_pessoas_removidos: int


def sync_orgaos_from_raw_detail() -> OrgaoSyncResult:
    """
    Normaliza órgãos, participantes e coordenadores
    usando apenas metas.raw_detail.

    Não consulta o SMAE.
    """

    metas_processadas = 0

    orgaos_criados = 0
    orgaos_atualizados = 0
    vinculos_orgaos_criados = 0
    vinculos_orgaos_atualizados = 0
    vinculos_orgaos_removidos = 0

    pessoas_criadas = 0
    pessoas_atualizadas = 0
    vinculos_pessoas_criados = 0
    vinculos_pessoas_removidos = 0

    with rx.session() as session:
        metas = session.exec(
            select(Meta)
        ).all()

        existing_orgaos = session.exec(
            select(Orgao)
        ).all()

        orgaos_by_smae_id = {
            orgao.smae_id: orgao
            for orgao in existing_orgaos
        }

        existing_pessoas = session.exec(
            select(Pessoa)
        ).all()

        pessoas_by_smae_id = {
            pessoa.smae_id: pessoa
            for pessoa in existing_pessoas
        }

        for meta in metas:
            if meta.id is None:
                continue

            metas_processadas += 1

            raw_detail = meta.raw_detail or {}

            raw_orgaos = (
                raw_detail.get("orgaos_participantes")
                or []
            )

            desired_orgao_ids: set[int] = set()

            desired_pessoa_links: set[
                tuple[int, str]
            ] = set()

            # Órgãos e participantes
            for raw_meta_orgao in raw_orgaos:
                raw_orgao = (
                    raw_meta_orgao.get("orgao")
                    or {}
                )

                orgao_smae_id = raw_orgao.get("id")
                descricao = raw_orgao.get("descricao")
                sigla = raw_orgao.get("sigla")

                if (
                    orgao_smae_id is None
                    or not descricao
                ):
                    continue

                orgao = orgaos_by_smae_id.get(
                    orgao_smae_id
                )

                if orgao is None:
                    orgao = Orgao(
                        smae_id=orgao_smae_id,
                        sigla=sigla,
                        descricao=descricao,
                    )

                    session.add(orgao)
                    session.flush()

                    orgaos_by_smae_id[
                        orgao_smae_id
                    ] = orgao

                    orgaos_criados += 1

                else:
                    changed = False

                    if orgao.sigla != sigla:
                        orgao.sigla = sigla
                        changed = True

                    if orgao.descricao != descricao:
                        orgao.descricao = descricao
                        changed = True

                    if changed:
                        session.add(orgao)
                        orgaos_atualizados += 1

                if orgao.id is None:
                    raise RuntimeError(
                        f"Órgão SMAE "
                        f"{orgao_smae_id} "
                        "sem ID local."
                    )

                desired_orgao_ids.add(orgao.id)

                responsavel = bool(
                    raw_meta_orgao.get(
                        "responsavel",
                        False,
                    )
                )

                existing_link = session.exec(
                    select(MetaOrgao).where(
                        MetaOrgao.meta_id
                        == meta.id,
                        MetaOrgao.orgao_id
                        == orgao.id,
                    )
                ).first()

                if existing_link is None:
                    session.add(
                        MetaOrgao(
                            meta_id=meta.id,
                            orgao_id=orgao.id,
                            responsavel=responsavel,
                        )
                    )

                    vinculos_orgaos_criados += 1

                elif (
                    existing_link.responsavel
                    != responsavel
                ):
                    existing_link.responsavel = (
                        responsavel
                    )

                    session.add(existing_link)

                    vinculos_orgaos_atualizados += 1

                # Participantes vinculados ao órgão
                participantes = (
                    raw_meta_orgao.get(
                        "participantes"
                    )
                    or []
                )

                for raw_pessoa in participantes:
                    pessoa_smae_id = (
                        raw_pessoa.get("id")
                    )

                    nome = raw_pessoa.get(
                        "nome_exibicao"
                    )

                    if (
                        pessoa_smae_id is None
                        or not nome
                    ):
                        continue

                    pessoa = pessoas_by_smae_id.get(
                        pessoa_smae_id
                    )

                    if pessoa is None:
                        pessoa = Pessoa(
                            smae_id=pessoa_smae_id,
                            nome_exibicao=nome,
                        )

                        session.add(pessoa)
                        session.flush()

                        pessoas_by_smae_id[
                            pessoa_smae_id
                        ] = pessoa

                        pessoas_criadas += 1

                    elif (
                        pessoa.nome_exibicao
                        != nome
                    ):
                        pessoa.nome_exibicao = nome

                        session.add(pessoa)

                        pessoas_atualizadas += 1

                    if pessoa.id is None:
                        raise RuntimeError(
                            f"Pessoa SMAE "
                            f"{pessoa_smae_id} "
                            "sem ID local."
                        )

                    tipo = "participante_orgao"

                    desired_pessoa_links.add(
                        (pessoa.id, tipo)
                    )

                    existing_person_link = (
                        session.exec(
                            select(
                                MetaPessoa
                            ).where(
                                MetaPessoa.meta_id
                                == meta.id,
                                MetaPessoa.pessoa_id
                                == pessoa.id,
                                MetaPessoa.tipo
                                == tipo,
                            )
                        ).first()
                    )

                    if existing_person_link is None:
                        session.add(
                            MetaPessoa(
                                meta_id=meta.id,
                                pessoa_id=pessoa.id,
                                tipo=tipo,
                                orgao_id=orgao.id,
                            )
                        )

                        vinculos_pessoas_criados += 1

                    elif (
                        existing_person_link.orgao_id
                        != orgao.id
                    ):
                        existing_person_link.orgao_id = (
                            orgao.id
                        )

                        session.add(
                            existing_person_link
                        )

            # Coordenadores CP
            coordenadores = (
                raw_detail.get(
                    "coordenadores_cp"
                )
                or []
            )

            for raw_pessoa in coordenadores:
                pessoa_smae_id = raw_pessoa.get(
                    "id"
                )

                nome = raw_pessoa.get(
                    "nome_exibicao"
                )

                if (
                    pessoa_smae_id is None
                    or not nome
                ):
                    continue

                pessoa = pessoas_by_smae_id.get(
                    pessoa_smae_id
                )

                if pessoa is None:
                    pessoa = Pessoa(
                        smae_id=pessoa_smae_id,
                        nome_exibicao=nome,
                    )

                    session.add(pessoa)
                    session.flush()

                    pessoas_by_smae_id[
                        pessoa_smae_id
                    ] = pessoa

                    pessoas_criadas += 1

                elif pessoa.nome_exibicao != nome:
                    pessoa.nome_exibicao = nome

                    session.add(pessoa)

                    pessoas_atualizadas += 1

                if pessoa.id is None:
                    raise RuntimeError(
                        f"Pessoa SMAE "
                        f"{pessoa_smae_id} "
                        "sem ID local."
                    )

                tipo = "coordenador_cp"

                desired_pessoa_links.add(
                    (pessoa.id, tipo)
                )

                existing_person_link = session.exec(
                    select(MetaPessoa).where(
                        MetaPessoa.meta_id
                        == meta.id,
                        MetaPessoa.pessoa_id
                        == pessoa.id,
                        MetaPessoa.tipo
                        == tipo,
                    )
                ).first()

                if existing_person_link is None:
                    session.add(
                        MetaPessoa(
                            meta_id=meta.id,
                            pessoa_id=pessoa.id,
                            tipo=tipo,
                            orgao_id=None,
                        )
                    )

                    vinculos_pessoas_criados += 1

            # Remove órgãos que deixaram de pertencer à meta.
            existing_orgao_links = session.exec(
                select(MetaOrgao).where(
                    MetaOrgao.meta_id == meta.id
                )
            ).all()

            for link in existing_orgao_links:
                if (
                    link.orgao_id
                    not in desired_orgao_ids
                ):
                    session.delete(link)

                    vinculos_orgaos_removidos += 1

            # Remove vínculos de pessoas que não existem mais.
            existing_person_links = session.exec(
                select(MetaPessoa).where(
                    MetaPessoa.meta_id == meta.id
                )
            ).all()

            for link in existing_person_links:
                key = (
                    link.pessoa_id,
                    link.tipo,
                )

                if key not in desired_pessoa_links:
                    session.delete(link)

                    vinculos_pessoas_removidos += 1

        session.commit()

    return OrgaoSyncResult(
        metas_processadas=metas_processadas,

        orgaos_criados=orgaos_criados,
        orgaos_atualizados=orgaos_atualizados,
        vinculos_orgaos_criados=(
            vinculos_orgaos_criados
        ),
        vinculos_orgaos_atualizados=(
            vinculos_orgaos_atualizados
        ),
        vinculos_orgaos_removidos=(
            vinculos_orgaos_removidos
        ),

        pessoas_criadas=pessoas_criadas,
        pessoas_atualizadas=pessoas_atualizadas,
        vinculos_pessoas_criados=(
            vinculos_pessoas_criados
        ),
        vinculos_pessoas_removidos=(
            vinculos_pessoas_removidos
        ),
    )