from typing import Literal
from pydantic import BaseModel, Field


class CalcInput(BaseModel):
    expression: str = Field(
        ...,
        description="Expression arithmétique simple, par exemple '(1200 * 0.1) + 300'"
    )


class WeatherInput(BaseModel):
    ville: str = Field(..., description="Nom de la ville")


class WebSearchInput(BaseModel):
    question: str = Field(
        ...,
        description="Question de recherche juridique récente ou externe au corpus local"
    )


class TodoInput(BaseModel):
    action: Literal["ajouter", "lister", "supprimer"] = Field(
        ...,
        description="Action à effectuer sur la todo locale"
    )
    item: str = Field(default="", description="Élément concerné si nécessaire")


class EmptyInput(BaseModel):
    pass