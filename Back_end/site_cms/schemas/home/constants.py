HOME_PAGE_KEY = "home"
HOME_PAGE_TITLE = "Página Inicial"

HOME_SECTIONS = [
    {
        "key": "about_pdm",
        "name": "Seção Carta do prefeito",
        "section_type": "about_pdm",
        "position": 10,
    },
    {
        "key": "news",
        "name": "Notícias",
        "section_type": "news",
        "position": 20,
    },
    {
        "key": "axes",
        "name": "Eixos",
        "section_type": "axes",
        "position": 30,
    },
]

HOME_SECTION_EDITOR_META = {
    "about_pdm": {
        "name": "Seção Carta do prefeito",
        "route": "/admin/site/home/carta-prefeito",
        "description": (
            "Carta institucional, autoria, textos de apresentação "
            "e recursos relacionados."
        ),
    },
    "news": {
        "name": "Notícias",
        "route": "/admin/site/home/noticias",
        "description": (
            "Notícias exibidas na Página Inicial, links, datas e prioridade."
        ),
    },
    "axes": {
        "name": "Eixos",
        "route": "/admin/site/home/eixos",
        "description": (
            "Conteúdo editorial dos eixos, cores, destaques e recursos visuais."
        ),
    },
}
