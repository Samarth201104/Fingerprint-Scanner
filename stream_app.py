import streamlit as st
import tempfile
import os
from PIL import Image

from pipeline.acquisition import load_image
from pipeline.roi_extraction import extract_roi
from pipeline.preprocessing import preprocess
from pipeline.gabor_enhancement import gabor_enhance
from pipeline.thresholding import adaptive_threshold
from pipeline.ridge_postprocess import postprocess
from utils.io_utils import save


st.set_page_config(
    page_title="Fingerprint Enhancement",
    layout="centered"
)

st.title("🖐️ Fingerprint Enhancement Pipeline")
st.write(
    "Upload a fingerprint image to extract ROI, enhance ridges, "
    "and generate a clean binary fingerprint."
)

uploaded_file = st.file_uploader(
    "Upload Fingerprint Image",
    type=["jpg", "jpeg", "png", "bmp"]
)

def process_image_streamlit(uploaded_image):
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.png")
        temp_dir = r"D:\Fingerprint-Scanner\temp_output"
        output_path = os.path.join(temp_dir, "output.png")

        # Save uploaded image
        image = Image.open(uploaded_image).convert("RGB")
        image.save(input_path)

        # ----- Pipeline -----
        img = load_image(input_path)
        roi = extract_roi(img)
        _, norm = preprocess(roi)
        gabor = gabor_enhance(norm)
        binary = adaptive_threshold(gabor)
        final = postprocess(binary)

        save(final, output_path)

        return output_path


if uploaded_file is not None:
    st.subheader("📥 Input Image")
    st.image(uploaded_file, use_container_width=True)

    if st.button("🔍 Process Fingerprint"):
        with st.spinner("Processing fingerprint..."):
            output_path = process_image_streamlit(uploaded_file)

        st.success("Processing completed!")

        st.subheader("📤 Processed Output")
        st.image(output_path, use_container_width=True)
