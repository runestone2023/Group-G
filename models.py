from pydantic import BaseModel

class MoveCmd(BaseModel):
    speed: int
    distance: int

class RotateCmd(BaseModel):
    angle: float
