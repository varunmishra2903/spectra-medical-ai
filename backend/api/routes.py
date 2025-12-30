from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import torch

from backend.ingestion.detect import detect_file_type
from backend.ingestion.validate import validate_file
from backend.ingestion.metadata import extract_metadata
from backend.runtime.workspace import create_case_workspace
from backend.gatekeeper.preprocess import preprocess_gatekeeper
from backend.gatekeeper.infer import infer_gatekeeper
from backend.router import route_case

from backend.brain.preprocess import preprocess_brain_case
from backend.chest.preprocess import preprocess_chest_image
from backend.bone.preprocess import preprocess_bone_image

from backend.brain.infer import infer_brain
from backend.chest.infer import infer_chest
from backend.bone.infer import infer_bone

from backend.postprocess.aggregate import (
    postprocess_brain_logits,
    postprocess_chest_probs,
    postprocess_bone_probs,
)

from backend.results.schema import (
    build_brain_result,
    build_chest_result,
    build_bone_result,
    result_to_dict,
)

from backend.core.logging import get_logger
from backend.core.config import (
    BRAIN_MODEL_VERSION,
    CHEST_MODEL_VERSION,
    BONE_MODEL_VERSION,
)

router = APIRouter()
logger = get_logger(__name__)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # -------------------------------------------------
    # Save uploaded file
    # -------------------------------------------------
    suffix = Path(file.filename).suffix
    temp_path = Path("runtime/tmp") / f"upload{suffix}"
    temp_path.parent.mkdir(parents=True, exist_ok=True)

    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # -------------------------------------------------
    # Ingestion
    # -------------------------------------------------
    detect_file_type(temp_path)
    validate_file(temp_path)
    case_info = extract_metadata(temp_path)

    case_dir = create_case_workspace(case_info, temp_path)
    logger.info(f"Case workspace created: {case_dir}")

    # -------------------------------------------------
    # Gatekeeper
    # -------------------------------------------------
    gate_tensor = preprocess_gatekeeper(case_dir)
    gate_pred, gate_conf = infer_gatekeeper(gate_tensor, DEVICE)

    route = route_case(gate_pred, gate_conf)
    logger.info(f"Route locked: {route}")

    # -------------------------------------------------
    # Specialist pipelines
    # -------------------------------------------------
    if route == "brain":
        volume = preprocess_brain_case(case_dir).unsqueeze(0)
        logits = infer_brain(volume, DEVICE)
        mask, conf = postprocess_brain_logits(logits)

        result = build_brain_result(
            case_id=case_info.case_id,
            confidence=conf,
            model_version=BRAIN_MODEL_VERSION,
            tumor_present=conf > 0.5,
        )

    elif route == "chest":
        tensor = preprocess_chest_image(temp_path).unsqueeze(0)
        probs = infer_chest(tensor, DEVICE)
        _, conf = postprocess_chest_probs(probs)

        result = build_chest_result(
            case_id=case_info.case_id,
            confidence=conf,
            model_version=CHEST_MODEL_VERSION,
            abnormal=conf > 0.5,
        )

    elif route == "bone":
        tensor = preprocess_bone_image(temp_path)
        probs = infer_bone(tensor, DEVICE)
        _, conf = postprocess_bone_probs(probs)

        result = build_bone_result(
            case_id=case_info.case_id,
            confidence=conf,
            model_version=BONE_MODEL_VERSION,
            fracture=conf > 0.5,
        )

    else:
        raise HTTPException(status_code=400, detail="Ambiguous case")

    return result_to_dict(result)
