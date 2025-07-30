from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    DV_R: Union[int, float] = Field(..., description="Доходы от продаж")
    DA_R: Union[int, float] = Field(..., description="Дебиторская задолженность")
    AV_R: Union[int, float] = Field(..., description="Активы")
    AA_R: Union[int, float] = Field(..., description="Оборотные активы")
    PM_R: Union[int, float] = Field(..., description="Прибыль")


class MultipleDataInputs(BaseModel):
    inputs: List[PredictionRequest] = Field(..., description="Список входных данных для предсказания")

    class Config:
        json_schema_extra = {
            "example": {
                "inputs": [
                    {
                        "DV_R": 318,
                        "DA_R": 7798,
                        "AV_R": 365,
                        "AA_R": 7177,
                        "PM_R": 9507
                    }
                ]
            }
        }


class SingleDataInput(BaseModel):
    """Схема для одиночного запроса предсказания"""
    DV_R: Union[int, float] = Field(..., description="Доходы от продаж")
    DA_R: Union[int, float] = Field(..., description="Дебиторская задолженность")
    AV_R: Union[int, float] = Field(..., description="Активы")
    AA_R: Union[int, float] = Field(..., description="Оборотные активы")
    PM_R: Union[int, float] = Field(..., description="Прибыль")

    class Config:
        json_schema_extra = {
            "example": {
                "DV_R": 318,
                "DA_R": 7798,
                "AV_R": 365,
                "AA_R": 7177,
                "PM_R": 9507
            }
        }


class PredictionResponse(BaseModel):
    prediction: int
    probability: List[float]


class PredictionResults(BaseModel):
    predictions: List[int]
    probabilities: List[List[float]]
    version: str
    errors: Optional[Any] = None