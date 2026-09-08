from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Back_end.metas.api import router as metas_router


api = FastAPI(
    title="Programa de Metas V2 API",
    version="1.0.0",
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
)

api.include_router(metas_router)