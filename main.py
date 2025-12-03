from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.session import Base, engine
import models
from api.routers.users import router as users_router
from api.routers.players import router as players_router
from api.routers.peladas import router as peladas_router
from api.routers.pelada_scouts import router as pelada_scouts_router
from api.routers.pelada_resultados import router as pelada_resultados_router
from api.routers.inicio import router as inicio_router
from api.routers.auth import router as auth_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)
app.include_router(users_router)
app.include_router(players_router)
app.include_router(peladas_router)
app.include_router(pelada_scouts_router)
app.include_router(pelada_resultados_router)
app.include_router(inicio_router)
app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8080, reload=True)
