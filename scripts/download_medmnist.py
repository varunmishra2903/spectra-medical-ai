import medmnist
from medmnist import INFO
import os
from PIL import Image
import numpy as np

# Config
OUTPUT_DIR = "data/gatekeeper"
DATASETS = ['pneumoniamnist', 'organamnist', 'fracturemnist3d']


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def save_images(dataset_name):
    print(f"⬇️ Downloading {dataset_name}...")
    info = INFO[dataset_name]
    DataClass = getattr(medmnist, info['python_class'])

    # Download dataset
    data = DataClass(split='train', download=True)

    # Output folder
    save_path = os.path.join(OUTPUT_DIR, dataset_name)
    ensure_dir(save_path)

    print(f"📸 Saving sample images to {save_path}...")

    num_samples = min(50, len(data))

    for i in range(num_samples):
        img, target = data[i]

        # Convert to numpy array
        arr = np.array(img)

        # -----------------------------------
        # SHAPE HANDLING (UNIVERSAL)
        # -----------------------------------

        # Case 1: True 3D volume (D, H, W)
        if arr.ndim == 3:
            depth = arr.shape[0]
            arr = arr[depth // 2]

        # Case 2: Extra singleton dimensions (e.g., 1x1xHxW)
        elif arr.ndim == 4:
            arr = arr.squeeze()

            if arr.ndim == 3:
                depth = arr.shape[0]
                arr = arr[depth // 2]

        # At this point arr must be (H, W)
        if arr.ndim != 2:
            raise ValueError(
                f"Unexpected image shape after processing: {arr.shape}"
            )

        # -----------------------------------
        # NORMALIZATION (CRITICAL)
        # -----------------------------------
        if arr.dtype != np.uint8:
            arr = arr.astype(np.float32)
            arr = 255 * (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)
            arr = arr.astype(np.uint8)

        # Convert to PIL Image (grayscale)
        img = Image.fromarray(arr, mode='L')

        # Save
        img.save(os.path.join(save_path, f"sample_{i}.png"))


if __name__ == "__main__":
    ensure_dir(OUTPUT_DIR)

    for ds in DATASETS:
        try:
            save_images(ds)
        except Exception as e:
            print(f"⚠️ Error processing {ds}: {e}")

    print("✅ Done! Data is ready in data/gatekeeper/")