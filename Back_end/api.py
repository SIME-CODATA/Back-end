from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Back_end.access_api.metas.api import router as metas_router
from Back_end.site_cms.api.router import router as site_cms_router
from Back_end.site_cms.api.meta_router import router as site_metas_router


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

api.include_router(metas_router)
api.include_router(site_cms_router)
api.include_router(site_metas_router)
