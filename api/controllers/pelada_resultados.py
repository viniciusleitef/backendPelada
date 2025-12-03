from sqlalchemy.orm import Session

from models.pelada_resultado import PeladaResultado
from models.pelada_scout import PeladaScout
from schemas.pelada_resultado import PeladaResultadoCreate

def list_resultados(db: Session) -> list[PeladaResultado]:
    return db.query(PeladaResultado).order_by(PeladaResultado.id.desc()).all()

def create_resultado(payload: PeladaResultadoCreate, db: Session) -> PeladaResultado:
    item = PeladaResultado(
        pelada_id=payload.pelada_id,
        quantidade_de_jogadores=payload.quantidade_de_jogadores,
        total_de_gols=payload.total_de_gols,
        total_assistencias=payload.total_assistencias,
        total_desarmes=payload.total_desarmes,
        total_defesas_dificeis=payload.total_defesas_dificeis,
        total_faltas=payload.total_faltas,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def create_resultado_totais_for_pelada(pelada_id: int, db: Session) -> PeladaResultado:
    scouts = db.query(PeladaScout).filter(PeladaScout.pelada_id == pelada_id).all()
    quantidade_de_jogadores = len({s.jogador_id for s in scouts})
    total_de_gols = sum(s.gols for s in scouts)
    total_assistencias = sum(s.assistencias for s in scouts)
    total_desarmes = sum(s.desarmes for s in scouts)
    total_defesas_dificeis = sum(s.defesas_dificeis for s in scouts)
    total_faltas = sum(s.faltas for s in scouts)

    item = PeladaResultado(
        pelada_id=pelada_id,
        quantidade_de_jogadores=quantidade_de_jogadores,
        total_de_gols=total_de_gols,
        total_assistencias=total_assistencias,
        total_desarmes=total_desarmes,
        total_defesas_dificeis=total_defesas_dificeis,
        total_faltas=total_faltas,
    )
    db.add(item)
    db.flush()
    return item
