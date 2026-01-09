import os
import sys

from pipeline.acquisition import load_image
from pipeline.roi_extraction import extract_roi
from pipeline.preprocessing import preprocess
from pipeline.gabor_enhancement import gabor_enhance
from pipeline.thresholding import adaptive_threshold
from pipeline.ridge_postprocess import postprocess
from utils.io_utils import save


VALID_EXT = (".jpg", ".jpeg", ".png", ".bmp")


def process_image(input_path, output_path):
    img = load_image(input_path)
    roi = extract_roi(img)
    _,norm = preprocess(roi)
    gabor = gabor_enhance(norm)
    binary = adaptive_threshold(gabor)
    final = postprocess(binary)
    save(final, output_path)


def main():
    if len(sys.argv) < 2:
        print("❌ Provide image or folder path")
        print("👉 Usage:")
        print("   python main.py input/finger.jpg")
        print("   python main.py input/demo")
        sys.exit(1)

    input_path = sys.argv[1]

    # ---------- CASE 1: SINGLE IMAGE ----------
    if os.path.isfile(input_path):
        if not input_path.lower().endswith(VALID_EXT):
            print("❌ Unsupported file type")
            sys.exit(1)

        os.makedirs("output", exist_ok=True)

        filename = os.path.basename(input_path)
        output_path = os.path.join("output", filename)

        print(f"🔍 Processing image: {filename}")
        process_image(input_path, output_path)
        print(f"✅ Saved → {output_path}")

    # ---------- CASE 2: FOLDER ----------
    elif os.path.isdir(input_path):
        folder_name = os.path.basename(os.path.normpath(input_path))

        output_dir = os.path.join("output", folder_name)
        os.makedirs(output_dir, exist_ok=True)

        print(f"\n📂 Processing folder: {input_path}\n")

        for file in os.listdir(input_path):
            if not file.lower().endswith(VALID_EXT):
                continue

            in_file = os.path.join(input_path, file)
            out_file = os.path.join(output_dir, file)

            print(f"🔍 Processing: {file}")
            try:
                process_image(in_file, out_file)
                print(f"✅ Saved → {out_file}")
            except Exception as e:
                print(f"❌ Failed {file}: {e}")

        print("\n🎉 Folder processing completed")

    else:
        print("❌ Invalid path provided")


if __name__ == "__main__":
    main()
