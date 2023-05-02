
from pydantic import BaseModel

class MoveCmd(BaseModel):
    speed: int

class RotateCmd(BaseModel):
    angle: float

class ClawCmd(BaseModel):
    grab: bool