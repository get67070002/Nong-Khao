import streamlit as st
import pytesseract
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Khaul\OneDrive\Documents\Project complete\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    """Preprocesses an image for improved OCR accuracy."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    kernel = np.ones((2, 2), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    return thresh

def ocr_thai_text(image):
    """Performs Thai text OCR using Tesseract."""
    preprocessed_image = preprocess_image(image)
    if preprocessed_image is None:
        return None

    img_resized = cv2.resize(preprocessed_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    pil_image = Image.fromarray(img_resized)

    try:
        text = pytesseract.image_to_string(pil_image, lang='tha', config='--psm 6')
        return text
    except Exception as e:
        st.error(f"Error during OCR: {e}")
        return None

def display_processed_image(image):
    """Displays the processed image in Streamlit."""
    preprocessed_image = preprocess_image(image)
    if preprocessed_image is None:
        return

def main():
    """Main function for Streamlit app."""
    st.title("Thai Text OCR by Nong-Khao")
    st.subheader("*What is OCR?*")
    st.write("*OCR stands for Optical Character Recognition. It's a technology that enables computers to recognize and extract text from images or scanned documents. This means you can take a scanned document, a photo of a document, or even a handwritten note, and convert it into editable text.*")
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload an Image (Not PDF)", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        st.subheader("Original Image")
        st.image(image, channels="BGR")
        extracted_text = ocr_thai_text(image)
        if extracted_text:
            st.success("OCR Complete!")
            st.subheader("Extracted Text (Thai)")
            st.write(extracted_text)
            display_processed_image(image)
        else:
            st.warning("OCR failed. Please try a different image or adjust preprocessing parameters.")
main()
