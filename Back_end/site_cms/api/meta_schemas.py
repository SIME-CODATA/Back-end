from __future__ import annotations

from pydantic import BaseModel, Field


class MetaSearchRequest(BaseModel):
    """Filtros da pesquisa pública de Metas.

    POST é usado porque a combinação de filtros pode crescer sem transformar
    a URL em um contrato frágil. A operação continua sendo somente leitura.
    """

    texto: str = ""
    eixos: list[str] = Field(default_factory=list)
    orgaos: list[str] = Field(default_factory=list)
    monitoramento: list[str] = Field(default_factory=list)
    subprefeituras: list[str] = Field(default_factory=list)
    regioes: list[str] = Field(default_factory=list)
    tipos_obra: list[str] = Field(default_factory=list)
    equipamentos: list[str] = Field(default_factory=list)
    com_obras: bool | None = None
    regionalizada: bool | None = None
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1, le=132)
