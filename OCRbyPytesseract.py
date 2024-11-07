import cv2
import pytesseract
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# ตั้งค่า่พาธเพื่อให้ ocr หาโมเดล pytesseracct เจอ
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    # อ่านภาพ
    img = cv2.imread(image_path)

    # แปลงเป็นโทนสีเทาเพื่อประมวลผลรูปภาพให้มีประสิทธิภาพที่ดียิ่งขึ้น ทำให้มีจุดเล็กๆน้อยลง พื้นหลังสะอาดและข้อความคมชัดกว่าภาพสี
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur เพื่อลดการรบกวนและเพิ่มความถูกต้องของ ocr
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


    # เพื่อแยกแยะระหว่าง ข้อความกับพื้นหลัง
    _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)

    return thresh

def ocr_thai_text(image_path):
    # แปลงภาพเป็นขาวดำ ปรับคุณภาพของภาพ
    preprocessed_image = preprocess_image(image_path)
    
    # ปรับขนาดให้ใหฯ่เพื่อที่ OCR นั้นจะทำงานได้แม่นยำมากขึ้น
    img_resized = cv2.resize(preprocessed_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # แปลงภาพเป็นรูปแบบ PIL เพื่อที่จะรองรับไลเบอรี่ pytesseract
    pil_image = Image.fromarray(img_resized)
    
    # ทำให้ OCR อ่านค่าภาษาไทย และทำให้ข้อความนั้นเป็นข้อความเดียว 
    # สามารถเปลี่ยนภาษาได้ที่ส่วนนี้
    text = pytesseract.image_to_string(pil_image, lang='tha', config='--psm 6')
    print("OCR Text:", text)  # แสดงข้อความที่ OCR ได้
    
    return text

    # แปลงภาษาไทยในภาพให้เป็นขเอความตัวอักษร
def thai_ocr_pipeline(image_path):
    print("Starting Thai OCR pipeline...")
    thresh_image = preprocess_image(image_path)  # รับภาพที่ผ่านการปรับแก้ไขแล้ว
    plt.imshow(thresh_image, cmap='gray')  # แสดงภาพที่ปรับแก้ไข
    plt.show()  # แสดงภาพนั้น
    text = ocr_thai_text(image_path)
    print("OCR Complete.")
    return text

image_path = 'sample4.png'
extracted_text = thai_ocr_pipeline(image_path)
print("Extracted Text:", extracted_text)
