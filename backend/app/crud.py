from sqlalchemy.orm import Session

from . import models, schemas


# Team
def get_team_info(db: Session):
    return db.query(models.Team).first()


def update_team_info(
    db: Session,
    team_info_update: schemas.TeamUpdate,
):
    team_info = db.query(models.Team)

    team_info.name = team_info_update.name
    team_info.image = team_info_update.image
    team_info.region = team_info_update.region
    team_info.category = team_info_update.category
    team_info.league = team_info_update.league
    team_info.sns_accounts = team_info_update.sns_accounts

    db.commit()
    db.refresh(team_info)
    return team_info


# Match
def get_matches(db: Session):
    return db.query(models.Match).all()


def create_match(db: Session, match: schemas.MatchCreate):
    db_match = models.Match(
        opponent=match.opponent,
        date=match.date,
        time=match.time,
        venue=match.venue,
        my_team_score=match.my_team_score,
        opponent_score=match.opponent_score,
    )
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


# Player
def get_players(db: Session):
    return db.query(models.Player).all()


def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = models.Player(
        position=player.position,
        namae=player.namae,
        name=player.name,
        number=player.number,
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def update_player(db: Session, player_id: int, player_update: schemas.PlayerUpdate):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if not player:
        return None

    player.position = player_update.position
    player.number = player_update.number
    player.namae = player_update.namae
    player.name = player_update.name

    db.commit()
    db.refresh(player)
    return player


def delete_player(db: Session, player_id: int):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if player is None:
        return None
    db.delete(player)
    db.commit()
    return player
