from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from models.player import Player
from schemas.player import PlayerCreate, PlayerRead, PlayerUpdate

def list_players(db: Session) -> list[Player]:
    return db.query(Player).order_by(Player.id.desc()).all()

def create_player(payload: PlayerCreate, db: Session) -> Player:
    name = payload.nome.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Nome do jogador é obrigatório")
    existing = db.query(Player).filter(Player.nome.ilike(name)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Jogador com este nome já existe")
    item = Player(
        nome=name,
        total_gols=payload.total_gols,
        total_assistencias=payload.total_assistencias,
        total_desarmes=payload.total_desarmes,
        total_defesas_dificeis=payload.total_defesas_dificeis,
        total_faltas=payload.total_faltas,
        total_partidas=payload.total_partidas,
    )
    db.add(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Jogador com este nome já existe")
    db.refresh(item)
    return item

def update_player(player_id: int, payload: PlayerUpdate, db: Session) -> Player:
    item = db.query(Player).get(player_id)
    if not item:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    name = payload.nome.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Nome do jogador é obrigatório")
    existing = (
        db.query(Player)
        .filter(Player.nome.ilike(name), Player.id != player_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Jogador com este nome já existe")
    item.nome = name
    item.total_gols = payload.total_gols
    item.total_assistencias = payload.total_assistencias
    item.total_desarmes = payload.total_desarmes
    item.total_defesas_dificeis = payload.total_defesas_dificeis
    item.total_faltas = payload.total_faltas
    item.total_partidas = payload.total_partidas
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Jogador com este nome já existe")
    db.refresh(item)
    return item
