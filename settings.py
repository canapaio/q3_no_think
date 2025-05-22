from cat.mad_hatter.decorators import plugin
from pydantic import BaseModel, Field, field_validator


class MySettings(BaseModel):
    No_Think: bool = True
    Remove_Think: bool = True

@plugin
def settings_model():
    return MySettings