from pathlib import Path
import pydicom
import nibabel as nib
import numpy as np

from backend.core.logging import get_logger

logger = get_logger(__name__)


class ImageVolume:
    """
    Lazy medical image loader.
    Pixels are loaded only when requested.
    """

    def __init__(self, path: Path, file_type: str):
        self.path = path
        self.file_type = file_type
        self._pixels = None
        self._meta = None

        self._load_header()

    def _load_header(self):
        if self.file_type == "dicom":
            ds = pydicom.dcmread(self.path, stop_before_pixels=True)
            self._meta = {
                "rows": ds.Rows,
                "cols": ds.Columns,
                "spacing": getattr(ds, "PixelSpacing", None),
            }

        elif self.file_type == "nifti":
            img = nib.load(str(self.path))
            self._meta = {
                "shape": img.shape,
                "spacing": img.header.get_zooms(),
                "affine": img.affine,
            }

        else:
            raise ValueError(f"Unsupported volume type: {self.file_type}")

        logger.info(f"Header loaded for {self.file_type}")

    @property
    def metadata(self):
        return self._meta

    def load_pixels(self) -> np.ndarray:
        if self._pixels is not None:
            return self._pixels

        if self.file_type == "dicom":
            ds = pydicom.dcmread(self.path)
            self._pixels = ds.pixel_array

        elif self.file_type == "nifti":
            img = nib.load(str(self.path))
            self._pixels = img.get_fdata()

        logger.info("Pixel data loaded into memory")
        return self._pixels

