"""
Compatibilidade com o comando antigo.

O conteúdo da API legada agora é distribuído para as páginas corretas
do CMS. Este wrapper mantém o comando antigo funcionando.
"""

from Back_end.site_cms.importers.legacy_site_importer import main


if __name__ == "__main__":
    main()
