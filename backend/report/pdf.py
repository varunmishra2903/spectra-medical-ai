from pathlib import Path
from typing import List
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from backend.results.schema import ResultSchema
from backend.core.logging import get_logger

logger = get_logger(__name__)

PAGE_WIDTH, PAGE_HEIGHT = A4


def generate_pdf_report(
    output_path: Path,
    result: ResultSchema,
    image_paths: List[Path],
):
    """
    Generate a clinician-readable PDF report.

    Parameters
    ----------
    output_path : Path
        Where to save PDF
    result : ResultSchema
        Normalized result object
    image_paths : List[Path]
        Representative images / overlays to include
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output_path), pagesize=A4)

    _draw_header(c, result)
    _draw_summary(c, result)
    _draw_images(c, image_paths)

    c.showPage()
    c.save()

    logger.info(f"PDF report generated: {output_path}")


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def _draw_header(c: canvas.Canvas, result: ResultSchema):
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, PAGE_HEIGHT - 50, "S.P.E.C.T.R.A. Medical AI Report")

    c.setFont("Helvetica", 10)
    c.drawString(
        40,
        PAGE_HEIGHT - 70,
        f"Generated: {datetime.utcnow().isoformat()}Z"
    )


def _draw_summary(c: canvas.Canvas, result: ResultSchema):
    y = PAGE_HEIGHT - 120

    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Case Summary")

    c.setFont("Helvetica", 10)
    y -= 20
    c.drawString(40, y, f"Case ID: {result.case_id}")
    y -= 15
    c.drawString(40, y, f"Route: {result.route}")
    y -= 15
    c.drawString(40, y, f"Prediction: {result.prediction}")
    y -= 15
    c.drawString(40, y, f"Confidence: {result.confidence:.3f}")
    y -= 15
    c.drawString(40, y, f"Model Version: {result.model_version}")
    y -= 15
    c.drawString(40, y, f"Timestamp: {result.timestamp}")


def _draw_images(c: canvas.Canvas, image_paths: List[Path]):
    if not image_paths:
        return

    y = PAGE_HEIGHT - 300
    x = 40
    max_width = 240
    max_height = 240

    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y + 20, "Representative Images")

    for idx, img_path in enumerate(image_paths):
        if not img_path.exists():
            continue

        img = ImageReader(str(img_path))
        c.drawImage(
            img,
            x,
            y - max_height,
            width=max_width,
            height=max_height,
            preserveAspectRatio=True,
            mask="auto"
        )

        x += max_width + 20
        if x + max_width > PAGE_WIDTH:
            x = 40
            y -= max_height + 40
