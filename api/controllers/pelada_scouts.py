from sqlalchemy.orm import Session

from models.pelada_scout import PeladaScout
from schemas.pelada_scout import PeladaScoutCreate

def list_scouts(db: Session) -> list[PeladaScout]:
    return db.query(PeladaScout).order_by(PeladaScout.id.desc()).all()

def create_scout(payload: PeladaScoutCreate, db: Session) -> PeladaScout:
    item = PeladaScout(
        pelada_id=payload.pelada_id,
        jogador_id=payload.jogador_id,
        gols=payload.gols,
        assistencias=payload.assistencias,
        desarmes=payload.desarmes,
        defesas_dificeis=payload.defesas_dificeis,
        faltas=payload.faltas,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def create_scout_for_pelada(
    *,
    pelada_id: int,
    jogador_id: int,
    gols: int = 0,
    assistencias: int = 0,
    desarmes: int = 0,
    defesas_dificeis: int = 0,
    faltas: int = 0,
    db: Session,
) -> PeladaScout:
    item = PeladaScout(
        pelada_id=pelada_id,
        jogador_id=jogador_id,
        gols=gols,
        assistencias=assistencias,
        desarmes=desarmes,
        defesas_dificeis=defesas_dificeis,
        faltas=faltas,
    )
    db.add(item)
    db.flush()
    return item

def list_scouts_by_pelada(pelada_id: int, db: Session) -> list[PeladaScout]:
    return db.query(PeladaScout).where(PeladaScout.pelada_id == pelada_id).order_by(PeladaScout.id.asc()).all()
