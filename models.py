from pydantic import BaseModel

class MoveCmd(BaseModel):
    speed: int

class RotateCmd(BaseModel):
    angle: float