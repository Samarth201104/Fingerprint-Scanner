import gradio as gr
import tempfile
import os

from pipeline.acquisition import load_image
from pipeline.roi_extraction import extract_roi
from pipeline.preprocessing import preprocess
from pipeline.gabor_enhancement import gabor_enhance
from pipeline.thresholding import adaptive_threshold
from pipeline.ridge_postprocess import postprocess
from utils.io_utils import save


def process_image_gradio(input_image):
    """
    Gradio-compatible wrapper for fingerprint processing
    """

    # Create temp files
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.png")
        output_path = r"D:\Fingerprint-Scanner\temp_output"
        output_path = os.path.join(output_path, "output.png")

        # Save uploaded image
        input_image.save(input_path)

        # --- Pipeline ---
        img = load_image(input_path)
        roi = extract_roi(img)
        _, norm = preprocess(roi)
        gabor = gabor_enhance(norm)
        binary = adaptive_threshold(gabor)
        final = postprocess(binary)
        print('file saved to:', output_path)
        save(final, output_path)
        print('file saved to:', output_path)

        return output_path


iface = gr.Interface(
    fn=process_image_gradio,
    inputs=gr.Image(type="pil", label="Upload Fingerprint Image"),
    outputs=gr.Image(type="filepath", label="Processed Output"),
    title="Fingerprint Enhancement Pipeline",
    description="Upload a fingerprint image to extract ROI, enhance ridges, and generate a clean binary output."
)

if __name__ == "__main__":
    iface.launch()
