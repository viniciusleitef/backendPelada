from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException

from models.pelada import Pelada
from models.pelada_scout import PeladaScout
from models.pelada_resultado import PeladaResultado
from models.player import Player
from schemas.pelada import PeladaCreate, PeladaUpdate
from api.controllers.pelada_scouts import create_scout_for_pelada
from api.controllers.pelada_resultados import create_resultado_totais_for_pelada

def list_peladas(db: Session) -> list[Pelada]:
    return db.query(Pelada).order_by(Pelada.id.desc()).all()

def create_pelada(payload: PeladaCreate, db: Session) -> Pelada:
    try:
        jogadores_input = payload.jogadores or []
        if len(jogadores_input) < 2:
            raise HTTPException(status_code=400, detail="A pelada deve ter pelo menos 2 jogadores")
        ids = []
        for j in jogadores_input:
            if not j.jogador_id or j.jogador_id <= 0:
                raise HTTPException(status_code=400, detail="Jogador inválido")
            ids.append(j.jogador_id)
        if len(set(ids)) != len(ids):
            raise HTTPException(status_code=400, detail="Lista de jogadores contém duplicados")

        inicio = payload.horario_inicio
        fim = payload.horario_fim
        if inicio and fim:
            horario_str = f"{inicio.strftime('%H:%M')} - {fim.strftime('%H:%M')}"
        elif inicio:
            horario_str = inicio.strftime('%H:%M')
        elif fim:
            horario_str = fim.strftime('%H:%M')
        else:
            horario_str = ""

        custo_do_campo = payload.custo_do_campo or 0
        custo_do_arbitro = (payload.custo_do_arbitro or 0) if payload.teve_arbitro else 0
        custo_adicional = payload.custo_adicional or 0
        custo_total = float(custo_do_campo) + float(custo_do_arbitro) + float(custo_adicional)

        item = Pelada(
            data=payload.data,
            horario=horario_str,
            local=payload.local or "",
            teve_arbitro=payload.teve_arbitro,
            comentarios=payload.comentarios,
            custo_do_campo=custo_do_campo,
            custo_do_arbitro=custo_do_arbitro,
            custo_adicional=custo_adicional,
            custo_total=custo_total,
        )
        db.add(item)
        db.flush()

        for j in jogadores_input:
            player = db.query(Player).get(j.jogador_id)
            if not player:
                raise HTTPException(status_code=404, detail="Jogador não encontrado")
            create_scout_for_pelada(
                pelada_id=item.id,
                jogador_id=player.id,
                gols=j.gols,
                assistencias=j.assistencias,
                desarmes=j.desarmes,
                defesas_dificeis=j.defesas_dificeis,
                faltas=j.faltas,
                db=db,
            )
            player.total_gols = (player.total_gols or 0) + (j.gols or 0)
            player.total_assistencias = (player.total_assistencias or 0) + (j.assistencias or 0)
            player.total_desarmes = (player.total_desarmes or 0) + (j.desarmes or 0)
            player.total_defesas_dificeis = (player.total_defesas_dificeis or 0) + (j.defesas_dificeis or 0)
            player.total_faltas = (player.total_faltas or 0) + (j.faltas or 0)
            player.total_partidas = (player.total_partidas or 0) + 1

        create_resultado_totais_for_pelada(item.id, db)

        db.commit()
        db.refresh(item)
        return item
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Conflito ao salvar pelada ou scouts")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno ao salvar pelada e scouts")

def delete_pelada(pelada_id: int, db: Session) -> None:
    try:
        pelada = db.query(Pelada).get(pelada_id)
        if not pelada:
            raise HTTPException(status_code=404, detail="Pelada não encontrada")

        scouts = db.query(PeladaScout).filter(PeladaScout.pelada_id == pelada_id).all()
        for s in scouts:
            player = db.query(Player).get(s.jogador_id)
            if player:
                player.total_gols = max(0, (player.total_gols or 0) - (s.gols or 0))
                player.total_assistencias = max(0, (player.total_assistencias or 0) - (s.assistencias or 0))
                player.total_desarmes = max(0, (player.total_desarmes or 0) - (s.desarmes or 0))
                player.total_defesas_dificeis = max(0, (player.total_defesas_dificeis or 0) - (s.defesas_dificeis or 0))
                player.total_faltas = max(0, (player.total_faltas or 0) - (s.faltas or 0))
                player.total_partidas = max(0, (player.total_partidas or 0) - 1)

        db.query(PeladaResultado).filter(PeladaResultado.pelada_id == pelada_id).delete()
        db.query(PeladaScout).filter(PeladaScout.pelada_id == pelada_id).delete()

        db.delete(pelada)
        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno ao excluir pelada")

def update_pelada(pelada_id: int, payload: PeladaUpdate, db: Session) -> Pelada:
    try:
        pelada = db.query(Pelada).get(pelada_id)
        if not pelada:
            raise HTTPException(status_code=404, detail="Pelada não encontrada")

        jogadores_input = payload.jogadores or []
        if len(jogadores_input) < 2:
            raise HTTPException(status_code=400, detail="A pelada deve ter pelo menos 2 jogadores")
        ids = []
        for j in jogadores_input:
            if not j.jogador_id or j.jogador_id <= 0:
                raise HTTPException(status_code=400, detail="Jogador inválido")
            ids.append(j.jogador_id)
        if len(set(ids)) != len(ids):
            raise HTTPException(status_code=400, detail="Lista de jogadores contém duplicados")

        inicio = payload.horario_inicio
        fim = payload.horario_fim
        if inicio and fim:
            horario_str = f"{inicio.strftime('%H:%M')} - {fim.strftime('%H:%M')}"
        elif inicio:
            horario_str = inicio.strftime('%H:%M')
        elif fim:
            horario_str = fim.strftime('%H:%M')
        else:
            horario_str = ""

        custo_do_campo = payload.custo_do_campo or 0
        custo_do_arbitro = (payload.custo_do_arbitro or 0) if payload.teve_arbitro else 0
        custo_adicional = payload.custo_adicional or 0
        custo_total = float(custo_do_campo) + float(custo_do_arbitro) + float(custo_adicional)

        old_scouts = db.query(PeladaScout).filter(PeladaScout.pelada_id == pelada_id).all()
        for s in old_scouts:
            player = db.query(Player).get(s.jogador_id)
            if player:
                player.total_gols = max(0, (player.total_gols or 0) - (s.gols or 0))
                player.total_assistencias = max(0, (player.total_assistencias or 0) - (s.assistencias or 0))
                player.total_desarmes = max(0, (player.total_desarmes or 0) - (s.desarmes or 0))
                player.total_defesas_dificeis = max(0, (player.total_defesas_dificeis or 0) - (s.defesas_dificeis or 0))
                player.total_faltas = max(0, (player.total_faltas or 0) - (s.faltas or 0))
                player.total_partidas = max(0, (player.total_partidas or 0) - 1)
        db.query(PeladaScout).filter(PeladaScout.pelada_id == pelada_id).delete()

        pelada.data = payload.data
        pelada.horario = horario_str
        pelada.local = payload.local or ""
        pelada.teve_arbitro = payload.teve_arbitro
        pelada.comentarios = payload.comentarios
        pelada.custo_do_campo = custo_do_campo
        pelada.custo_do_arbitro = custo_do_arbitro
        pelada.custo_adicional = custo_adicional
        pelada.custo_total = custo_total

        for j in jogadores_input:
            player = db.query(Player).get(j.jogador_id)
            if not player:
                raise HTTPException(status_code=404, detail="Jogador não encontrado")
            create_scout_for_pelada(
                pelada_id=pelada.id,
                jogador_id=player.id,
                gols=j.gols,
                assistencias=j.assistencias,
                desarmes=j.desarmes,
                defesas_dificeis=j.defesas_dificeis,
                faltas=j.faltas,
                db=db,
            )
            player.total_gols = (player.total_gols or 0) + (j.gols or 0)
            player.total_assistencias = (player.total_assistencias or 0) + (j.assistencias or 0)
            player.total_desarmes = (player.total_desarmes or 0) + (j.desarmes or 0)
            player.total_defesas_dificeis = (player.total_defesas_dificeis or 0) + (j.defesas_dificeis or 0)
            player.total_faltas = (player.total_faltas or 0) + (j.faltas or 0)
            player.total_partidas = (player.total_partidas or 0) + 1

        db.query(PeladaResultado).filter(PeladaResultado.pelada_id == pelada_id).delete()
        create_resultado_totais_for_pelada(pelada.id, db)

        db.commit()
        db.refresh(pelada)
        return pelada
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Conflito ao atualizar pelada ou scouts")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar pelada e scouts")
