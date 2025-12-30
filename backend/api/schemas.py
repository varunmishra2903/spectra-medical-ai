from pydantic import BaseModel
from typing import Optional, Dict, Any


class AnalyzeResponse(BaseModel):
    case_id: str
    route: str
    prediction: str
    confidence: float
    model_version: str
    timestamp: str
    details: Optional[Dict[str, Any]] = None
