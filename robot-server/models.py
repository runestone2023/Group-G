from pydantic import BaseModel

class MoveCmd(BaseModel):
    speed: int

class MoveDistCmd(BaseModel):
    speed: int
    distance: float

class RotateCmd(BaseModel):
    angle: float

class ClawCmd(BaseModel):
    grab: bool

class LearnCmd(BaseModel):
    iters: int
