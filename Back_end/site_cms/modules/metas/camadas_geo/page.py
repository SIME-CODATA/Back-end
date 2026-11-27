"""Tela de upload, histórico e publicação das camadas GEO separadas do Excel."""
import reflex as rx
from Back_end.interface.layouts.admin_layout import admin_layout
from Back_end.site_cms.modules.metas.camadas_geo.state import CamadasGeoState as S


def _version_row(item):
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.hstack(rx.text(item['data'], weight='bold'), rx.badge(item['status'], variant='soft'),
                          spacing='2', align='center'),
                rx.text(item['descricao'], font_size='0.82rem'),
                rx.text(item['id'], font_size='0.72rem', color='gray'),
                rx.text('GeoJSON: ', item['geojson'], ' | GPKG: ', item['gpkg'], font_size='0.7rem', color='gray'),
                align='start', spacing='1', flex='1',
            ),
            rx.button('Selecionar', on_click=S.selecionar(item['id']), variant='outline', size='2'),
            width='100%', align='center',
        ),
        border='1px solid #D7DEE7', padding='12px', border_radius='10px', width='100%',
    )


def camadas_geo_admin_page() -> rx.Component:
    return admin_layout(rx.vstack(
        rx.vstack(
            rx.text('SITE / CAMADAS GEO', font_size='0.72rem', color='#1281AA', font_weight='700'),
            rx.heading('Atualizações do mapa geográfico', size='6'),
            rx.text('Linhas e polígonos independentes da planilha Excel e do banco de metas.',
                    size='2', color='gray'),
            align='start', spacing='1', width='100%',
        ),
        rx.callout('O upload cria uma nova versão em revisão. A API pública só muda após a publicação. '
                   'Nenhuma versão anterior é excluída.', color_scheme='blue'),
        rx.hstack(
            rx.badge('Versão ativa: ', S.versao_ativa, color_scheme='green', size='2'),
            rx.badge('Registros: ', S.total_ativo, variant='soft', size='2'),
            rx.badge('Publicáveis: ', S.total_publicavel, variant='soft', size='2'),
            wrap='wrap', spacing='3',
        ),
        rx.text(S.resumo_ativo, size='2', color='gray'),
        rx.cond(S.erro != '', rx.callout(S.erro, color_scheme='red'), rx.box()),
        rx.cond(S.mensagem != '', rx.callout(S.mensagem, color_scheme='green'), rx.box()),
        rx.cond(S.pode_editar_geo,
            rx.vstack(
                rx.heading('Enviar nova versão', size='4'),
                rx.text('Data de referência (AAAA-MM-DD)', font_weight='600', size='2'),
                rx.input(type='date', value=S.data_referencia,
                         on_change=S.set_data_referencia, width='240px'),
                rx.text('Descrição das alterações', font_weight='600', size='2'),
                rx.text_area(value=S.descricao_versao, on_change=S.set_descricao_versao,
                             placeholder='Ex.: novos trechos e polígonos validados',
                             width='100%', max_length=500),
                rx.upload(
                    rx.vstack(rx.icon(tag='cloud_upload', size=28),
                              rx.text('Selecione o GeoJSON e, se houver, o GeoPackage correspondente'),
                              rx.text('GeoJSON até 30 MiB; GPKG até 120 MiB', color='gray', font_size='0.76rem'),
                              rx.hstack(rx.foreach(rx.selected_files('camadas_geo_upload'), rx.text),
                                        wrap='wrap', spacing='2'),
                              align='center', spacing='2', width='100%'),
                    id='camadas_geo_upload', multiple=True, max_files=2,
                    accept={
                        'application/geo+json': ['.geojson'],
                        'application/geopackage+sqlite3': ['.gpkg'],
                        'application/octet-stream': ['.gpkg', '.geojson'],
                    },
                    width='100%', padding='22px', border='1px dashed #64748B',
                    border_radius='10px',
                ),
                rx.button('Validar e guardar como rascunho',
                          on_click=S.importar(rx.upload_files(upload_id='camadas_geo_upload')),
                          loading=S.enviando, disabled=S.enviando, color_scheme='blue'),
                rx.text('O Excel e os endpoints anteriores não são modificados pelo upload.',
                        color='gray', font_size='0.76rem'),
                spacing='3', align='stretch', width='100%', padding='18px',
                border='1px solid #D7DEE7', border_radius='12px',
            ), rx.box(),
        ),
        rx.vstack(
            rx.heading('Histórico e publicação', size='4'),
            rx.text('Selecionada: ', S.versao_selecionada, size='2'),
            rx.cond(S.pode_publicar_geo,
                rx.vstack(
                    rx.checkbox('Confirmo a retirada de registros ausentes nesta versão, se houver',
                                checked=S.confirmar_retiradas,
                                on_change=S.set_confirmar_retiradas),
                    rx.button('Publicar versão selecionada (ou restaurar a anterior)',
                          on_click=S.publicar_selecionada, color_scheme='green'),
                    align='start', spacing='2',
                ),
                rx.text('Seu perfil pode visualizar os arquivos, mas não publicar.', color='gray'),
            ),
            rx.foreach(S.versoes, _version_row),
            align='stretch', spacing='3', width='100%',
        ),
        rx.link('Ver GeoJSON público da versão ativa',
                href='/api/site/camadas/metas', is_external=True),
        align='stretch', width='100%', spacing='4', padding_bottom='4rem',
    ))
