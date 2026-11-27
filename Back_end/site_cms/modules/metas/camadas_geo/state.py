"""CMS de versões das camadas GEO, sem vínculo com o importador Excel."""
from __future__ import annotations

from datetime import date
from pathlib import Path
import reflex as rx

from Back_end.access.states.auth_state import AuthState
from Back_end.access.core.permissions import Permission
from Back_end.access.core.guards import can_access
from Back_end.site_cms.api import camadas_versions_service as service


class CamadasGeoState(AuthState):
    versoes: list[dict[str, str]] = []
    versao_ativa: str = ''
    versao_selecionada: str = ''
    data_referencia: str = ''
    descricao_versao: str = ''
    mensagem: str = ''
    erro: str = ''
    enviando: bool = False
    confirmar_retiradas: bool = False
    total_ativo: int = 0
    total_publicavel: int = 0
    resumo_ativo: str = ''

    @rx.var
    def pode_editar_geo(self) -> bool:
        return can_access(self.current_user_role, Permission.SITE_EDIT)

    @rx.var
    def pode_publicar_geo(self) -> bool:
        return can_access(self.current_user_role, Permission.SITE_PUBLISH)

    def _refresh(self):
        rows = service.list_versions()
        self.versoes = [
            {
                'id': str(r['id']),
                'data': str(r['data_referencia']),
                'descricao': str(r.get('descricao') or '(sem descrição)'),
                'status': 'PUBLICADA' if r.get('ativa') else 'ARQUIVADA / RASCUNHO',
                'geojson': str(r['arquivo_geojson']),
                'gpkg': str(r.get('arquivo_gpkg') or 'Não anexado'),
                'resumo': str((r.get('resumo') or {}).get('publicaveis', '?')) + ' registros publicáveis',
            }
            for r in rows
        ]
        self.versao_ativa = service.active_id()
        if not self.versao_selecionada or self.versao_selecionada not in {r['id'] for r in rows}:
            self.versao_selecionada = self.versao_ativa
        # As estatísticas públicas sempre refletem a versão ATIVA.
        info = service.public_info()
        self.total_ativo = int(info['total_na_fonte'])
        self.total_publicavel = int(info['total_publicavel'])
        self.resumo_ativo = ', '.join(f'{k}: {v}' for k, v in info['camadas_publicaveis'].items())

    @rx.event
    def load_page(self):
        redirect = self._require_permission(Permission.SITE_VIEW)
        if redirect is not None:
            return redirect
        self.mensagem = ''
        self.erro = ''
        self.data_referencia = date.today().isoformat()
        try:
            self._refresh()
        except Exception as exc:
            self.erro = f'Não foi possível carregar as camadas: {exc}'

    @rx.event
    def set_confirmar_retiradas(self, value: bool):
        self.confirmar_retiradas = value

    @rx.event
    def set_data_referencia(self, value: str):
        self.data_referencia = value

    @rx.event
    def set_descricao_versao(self, value: str):
        self.descricao_versao = value

    @rx.event
    def selecionar(self, version_id: str):
        redirect = self._require_permission(Permission.SITE_VIEW)
        if redirect is not None:
            return redirect
        if version_id in {v['id'] for v in self.versoes}:
            self.versao_selecionada = version_id
            self.mensagem = ''
            self.erro = ''

    @rx.event
    async def importar(self, files: list[rx.UploadFile]):
        redirect = self._require_permission(Permission.SITE_EDIT)
        if redirect is not None:
            yield redirect
            return
        self.erro = ''
        self.mensagem = ''
        if not files or len(files) > 2:
            self.erro = 'Envie um arquivo .geojson e, opcionalmente, um .gpkg correspondente.'
            return
        extensions = {Path(f.name or '').suffix.casefold() for f in files}
        if len(extensions) != len(files) or '.geojson' not in extensions or extensions - {'.geojson', '.gpkg'}:
            self.erro = 'Selecione exatamente um .geojson e, opcionalmente, um .gpkg.'
            return
        self.enviando = True
        yield
        try:
            blobs = {}
            for file in files:
                ext = Path(file.name or '').suffix.casefold()
                limit = service.MAX_JSON_BYTES if ext == '.geojson' else service.MAX_GPKG_BYTES
                content = await file.read(limit + 1)
                if len(content) > limit:
                    raise ValueError(f'Arquivo {ext} acima do limite permitido.')
                blobs[ext] = content
            draft = service.create_draft(
                geojson_bytes=blobs['.geojson'], gpkg_bytes=blobs.get('.gpkg'),
                data_referencia=self.data_referencia, descricao=self.descricao_versao,
                actor_id=self.current_user_id,
            )
            self.versao_selecionada = draft['id']
            self.mensagem = ('Versão recebida e validada. NÃO está pública. '
                             'Confira os dados e clique em Publicar versão para ativar.')
            self.descricao_versao = ''
            self._refresh()
            self._audit(action='CAMADAS_GEO_IMPORT', entity_type='camadas_geo',
                        entity_id=draft['id'], description='Nova versão GEO enviada para revisão.')
        except Exception as exc:
            self.erro = f'Upload recusado: {exc}'
        finally:
            self.enviando = False
            yield

    @rx.event
    def publicar_selecionada(self):
        redirect = self._require_permission(Permission.SITE_PUBLISH)
        if redirect is not None:
            return redirect
        self.erro = ''
        self.mensagem = ''
        try:
            if not self.versao_selecionada:
                raise ValueError('Selecione uma versão antes de publicar.')
            meta = service.publish(self.versao_selecionada, self.current_user_id,
                                   allow_missing=self.confirmar_retiradas)
            self._refresh()
            self.confirmar_retiradas = False
            self._audit(action='CAMADAS_GEO_PUBLISH', entity_type='camadas_geo',
                        entity_id=meta['id'], description='Versão GEO ativada no mapa público.')
            self.mensagem = ('Versão publicada! A API agora entrega ' + meta['id']
                             + '. O histórico anterior foi preservado.')
        except Exception as exc:
            self.erro = f'Publicação cancelada: {exc}'
