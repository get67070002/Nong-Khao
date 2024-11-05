import cv2
import pytesseract
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import re
import streamlit as st

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def adjust_file(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)
    return thresh

def ocr_reading(image):
    preprocessed_image = adjust_file(image)
    img_resized = cv2.resize(preprocessed_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    pil_image = Image.fromarray(img_resized)
    text = pytesseract.image_to_string(pil_image, lang='tha', config='--psm 6')
    text_processed = re.sub(r'(?<=[\u0E00-\u0E7F])\s(?=[\u0E00-\u0E7F])', '', text)
    text_final = re.sub(r'\s{2,}', ' ', text_processed).strip()
    return text_final

def starting_ocr(image):
    print("Starting Thai OCR pipeline...")
    thresh_image = adjust_file(image)
    plt.imshow(thresh_image, cmap='gray')
    plt.show()
    text = ocr_reading(image)
    print("OCR Complete.")
    return text

def display_processed_image(image):
    preprocessed_image = adjust_file(image)
    if preprocessed_image is not None:
        st.image(preprocessed_image, caption="Processed Image", channels="GRAY")

def main():
    st.title("Thai Text OCR by Nong-Khao")
    st.subheader("*What is OCR?*")
    st.write("*OCR คือเทคโนโลยีที่ช่วยให้คอมพิวเตอร์สามารถจดจำและดึงข้อความจากรูปภาพหรือเอกสารที่ถูกสแกนได้*")
    st.markdown("---")
    
    uploaded_file = st.file_uploader("Upload an Image (Not PDF)", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        st.subheader("Original Image")
        st.image(image, channels="BGR")
        
        extracted_text = ocr_reading(image)
        if extracted_text:
            st.success("OCR Complete!")
            st.subheader("Extracted Text (Thai)")
            st.write(extracted_text)
        else:
            st.warning("OCR failed. Please try a different image or adjust preprocessing parameters.")

main()
