import pydantic as pd

class DesktopEntry(pd.BaseModel):
    name: str
    exec: str
    icon: str
    type: str
    categories: list[str]
