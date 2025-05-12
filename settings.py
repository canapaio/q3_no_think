from cat.mad_hatter.decorators import plugin
from pydantic import BaseModel, Field, field_validator


class Think(Enum):
    on = "No Think on"
    off = "No Think off"

class RemoveThink(Enum):
    on = "Remove <Think> on"
    off = "Remove <Think> off"


class MySettings(BaseModel):
    Think: Think = Think.on
    RemoveThink: RemoveThink = RemoveThink.on