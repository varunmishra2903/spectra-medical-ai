from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any

# -------------------------------------------------
# Unified Result Schema
# -------------------------------------------------

@dataclass(frozen=True)
class ResultSchema:
    case_id: str
    route: str                  # brain | chest | bone
    prediction: str             # model-level label
    confidence: float            # final confidence (0–1)
    model_version: str
    timestamp: str
    details: Optional[Dict[str, Any]] = None


# -------------------------------------------------
# Builders (one per route)
# -------------------------------------------------

def build_brain_result(
    case_id: str,
    confidence: float,
    model_version: str,
    tumor_present: bool,
    extra: Optional[Dict[str, Any]] = None
) -> ResultSchema:
    return ResultSchema(
        case_id=case_id,
        route="brain",
        prediction="tumor_detected" if tumor_present else "no_tumor",
        confidence=confidence,
        model_version=model_version,
        timestamp=_now(),
        details=extra,
    )


def build_chest_result(
    case_id: str,
    confidence: float,
    model_version: str,
    abnormal: bool,
    extra: Optional[Dict[str, Any]] = None
) -> ResultSchema:
    return ResultSchema(
        case_id=case_id,
        route="chest",
        prediction="abnormal" if abnormal else "normal",
        confidence=confidence,
        model_version=model_version,
        timestamp=_now(),
        details=extra,
    )


def build_bone_result(
    case_id: str,
    confidence: float,
    model_version: str,
    fracture: bool,
    extra: Optional[Dict[str, Any]] = None
) -> ResultSchema:
    return ResultSchema(
        case_id=case_id,
        route="bone",
        prediction="fracture" if fracture else "normal",
        confidence=confidence,
        model_version=model_version,
        timestamp=_now(),
        details=extra,
    )


# -------------------------------------------------
# Utilities
# -------------------------------------------------

def result_to_dict(result: ResultSchema) -> Dict[str, Any]:
    """
    Convert ResultSchema to JSON-serializable dict.
    """
    return asdict(result)


def _now() -> str:
    return datetime.utcnow().isoformat() + "Z"
