"""
Inicialização compatível da Visão Geral.

Para instalações novas cria a seção com a carga inicial.
Para a instalação atual, em que a seção já foi criada vazia,
use repair_overview.
"""

from Back_end.site_cms.modules.metas.overview_service import (
    ensure_overview_section,
)


def main() -> None:
    section = ensure_overview_section()

    print(
        "[CMS VISÃO GERAL] Inicialização concluída."
    )
    print(
        f"section_id={section.id}"
    )

    print(
        "\nSe a seção já existia vazia por causa da versão anterior, rode:"
    )
    print(
        "uv run python -m "
        "Back_end.site_cms.modules.metas.repair_overview"
    )


if __name__ == "__main__":
    main()
