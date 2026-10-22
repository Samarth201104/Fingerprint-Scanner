import argparse
from pathlib import Path

from backend.app.services.fingerprint_service import fingerprint_service
from backend.pipeline.acquisition import load_image
from backend.utils.io_utils import save


VALID_EXT = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


def process_image(input_path, output_path):
    image = load_image(str(input_path))
    import cv2
    ok, encoded = cv2.imencode(Path(input_path).suffix or ".png", image)
    if not ok:
        raise ValueError("Could not encode input image")
    result = fingerprint_service.process_bytes(encoded.tobytes(), Path(input_path).name, "cli")
    from backend.app.core.config import DATA_DIR
    final = cv2.imread(str(DATA_DIR / result["job_id"] / "final.png"), cv2.IMREAD_GRAYSCALE)
    save(final, str(output_path))


def main():
    parser = argparse.ArgumentParser(description="Process fingerprint images with the shared CV pipeline")
    parser.add_argument("path", help="Image file or folder to process")
    parser.add_argument("--output", default="backend/data/outputs", help="Output directory (default: backend/data/outputs)")
    args = parser.parse_args()
    input_path = Path(args.path)

    # ---------- CASE 1: SINGLE IMAGE ----------
    if input_path.is_file():
        if input_path.suffix.lower() not in VALID_EXT:
            parser.error("Unsupported file type")
        output_path = Path(args.output) / input_path.name
        print(f"Processing image: {input_path.name}")
        process_image(input_path, output_path)
        print(f"Saved: {output_path}")

    # ---------- CASE 2: FOLDER ----------
    elif input_path.is_dir():
        output_dir = Path(args.output) / input_path.name
        print(f"Processing folder: {input_path}")
        for source in input_path.iterdir():
            if not source.is_file() or source.suffix.lower() not in VALID_EXT:
                continue
            out_file = output_dir / source.name
            try:
                process_image(source, out_file)
                print(f"Saved: {out_file}")
            except Exception as e:
                print(f"Failed {source.name}: {e}")

    else:
        parser.error("Invalid path provided")


if __name__ == "__main__":
    main()
