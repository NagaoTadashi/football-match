from pydantic import BaseModel
from typing import Optional
from datetime import date, time


# Match
class MatchBase(BaseModel):
    opponent: str
    date: date
    time: time
    venue: str
    my_team_score: Optional[int]
    opponent_score: Optional[int]


class MatchCreate(MatchBase):
    pass


class Match(MatchBase):
    id: int

    class Config:
        orm_mode = True


# Player
class PlayerBase(BaseModel):
    position: str
    namae: str
    name: str
    number: int


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int

    class Config:
        orm_mode = True
