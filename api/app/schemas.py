from typing import Any, List, Optional

from pydantic import BaseModel


class PredictionRequest(BaseModel):
    DV_R: int
    DA_R: int
    AV_R: int
    AA_R: int
    PM_R: int


class MultipleDataInputs(BaseModel):
    inputs: List[PredictionRequest]

    class Config:
        schema_extra = {
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


class PredictionResponse(BaseModel):
    prediction: int
    probability: List[float]


class PredictionResults(BaseModel):
    predictions: List[int]
    probabilities: List[List[float]]
    version: str
    errors: Optional[Any]