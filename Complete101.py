
import cv2
import pytesseract
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# ตั้งค่าพาธเพื่อให้ ocr หาโมเดล pytesseracct เจอ
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    # แปลงเป็นโทนสีเทาเพื่อประมวลผลรูปภาพให้มีประสิทธิภาพที่ดียิ่งขึ้น ทำให้มีจุดเล็กๆน้อยลง พื้นหลังสะอาดและข้อความคมชัดกว่าภาพสี
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur เพื่อลดการรบกวนและเพิ่มความถูกต้องของ ocr
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # เพื่อแยกแยะระหว่าง ข้อความกับพื้นหลัง
    _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)

    return thresh

def ocr_thai_text(image):
    # แปลงภาพเป็นขาวดำ ปรับคุณภาพของภาพ
    preprocessed_image = preprocess_image(image)
    
    # ปรับขนาดให้ใหฯ่เพื่อที่ OCR นั้นจะทำงานได้แม่นยำมากขึ้น
    img_resized = cv2.resize(preprocessed_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # แปลงภาพเป็นรูปแบบ PIL เพื่อที่จะรองรับไลเบอรี่ pytesseract
    pil_image = Image.fromarray(img_resized)
    
    # ทำให้ OCR อ่านค่าภาษาไทย และทำให้ข้อความนั้นเป็นข้อความเดียว 
    # สามารถเปลี่ยนภาษาได้ที่ส่วนนี้
    text = pytesseract.image_to_string(pil_image, lang='tha', config='--psm 6')
    print("OCR Text:", text)  # แสดงข้อความที่ OCR ได้
    
    return text

    # แปลงภาษาไทยในภาพให้เป็นข้อความตัวอักษร
def thai_ocr_pipeline(image):
    print("Starting Thai OCR pipeline...")
    thresh_image = preprocess_image(image)  # รับภาพที่ผ่านการปรับแก้ไขแล้ว
    plt.imshow(thresh_image, cmap='gray')  # แสดงภาพที่ปรับแก้ไข
    plt.show()  # แสดงภาพนั้น
    text = ocr_thai_text(image)
    print("OCR Complete.")
    return text

def display_processed_image(image):
    """Displays the processed image in Streamlit."""
    preprocessed_image = preprocess_image(image)
    if preprocessed_image is None:
        return

def main():
    """Main function for Streamlit app."""
    st.title("Thai Text OCR by Nong-Khao")
    st.subheader("*What is OCR?*")
    st.write("*OCR stands for Optical Character Recognition. It's a technology that enables computers to recognize and extract text from images or scanned documents.*")
    st.markdown("---")
    # Upload ไฟล์
    uploaded_file = st.file_uploader("Upload an Image (Not PDF)", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        # อ่านไฟล์ที่Upload
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        st.subheader("Original Image")
        st.image(image, channels="BGR")
        
        # ดำเนินการOCRและแสดงผล
        extracted_text = ocr_thai_text(image)
        if extracted_text:
            st.success("OCR Complete!")
            st.subheader("Extracted Text (Thai)")
            st.write(extracted_text)
            display_processed_image(image)
        else:
            st.warning("OCR failed. Please try a different image or adjust preprocessing parameters.")
main()
