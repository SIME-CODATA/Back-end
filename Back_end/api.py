from Back_end.site_cms.api.camadas_2026_11_19 import router as camadas_geo_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Back_end.access_api.metas.api import router as metas_router
from Back_end.site_cms.api.router import router as site_cms_router
from Back_end.site_cms.api.meta_router import router as site_metas_router
from Back_end.site_cms.modules.metas.fontes_api import fontes_router
from Back_end.media_library.api.api import router as media_router


api = FastAPI(
    title="Programa de Metas V2 API",
    version="1.0.0",
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_methods=["GET", "POST", "PUT", "OPTIONS"],
    allow_headers=["*"],
)

api.include_router(media_router)
api.include_router(metas_router)
api.include_router(site_metas_router)
site_cms_router.include_router(fontes_router)
api.include_router(site_cms_router)
api.include_router(media_router)
api.include_router(camadas_geo_router)
from Back_end.site_cms.api.camadas_ativas_router import router as camadas_geo_ativas_router
api.include_router(camadas_geo_ativas_router)
