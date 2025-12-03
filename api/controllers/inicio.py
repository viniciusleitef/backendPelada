from sqlalchemy.orm import Session
from sqlalchemy import func

from models.pelada import Pelada
from models.player import Player
from models.pelada_resultado import PeladaResultado
from schemas.inicio import InicioResumo

def get_inicio_resumo(db: Session) -> InicioResumo:
    total_peladas = db.query(func.count(Pelada.id)).scalar() or 0
    jogadores_ativos = db.query(func.count(Player.id)).scalar() or 0
    total_gols = db.query(func.coalesce(func.sum(PeladaResultado.total_de_gols), 0)).scalar() or 0
    return InicioResumo(
        total_peladas=int(total_peladas),
        jogadores_ativos=int(jogadores_ativos),
        total_gols=int(total_gols),
    )

