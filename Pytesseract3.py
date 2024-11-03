import cv2
import pytesseract
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# ตั้งค่า่พาธเพื่อให้ ocr หาโมเดล pytesseracct เจอ
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    # Read image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and improve OCR accuracy
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


    # Apply thresholding for binarization
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)

    return thresh

def ocr_thai_text(image_path):
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)
    
    # Resize image for better OCR accuracy
    img_resized = cv2.resize(preprocessed_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # Convert image to PIL format for pytesseract
    pil_image = Image.fromarray(img_resized)
    
    # OCR with Thai language and configuration
    text = pytesseract.image_to_string(pil_image, lang='tha', config='--psm 6')
    print("OCR Text:", text)  # แสดงข้อความที่ OCR ได้
    
    return text


def thai_ocr_pipeline(image_path):
    print("Starting Thai OCR pipeline...")
    thresh_image = preprocess_image(image_path)  # Get the processed image
    plt.imshow(thresh_image, cmap='gray')  # Show the processed image
    plt.show()  # Display the image
    text = ocr_thai_text(image_path)
    print("OCR Complete.")
    return text

image_path = 'sample3.png'
extracted_text = thai_ocr_pipeline(image_path)
print("Extracted Text:", extracted_text)

# Testing with English language OCR
# You can use this line to test with a separate image or the same one
# Make sure to replace 'img_0.png' with the path to an image that contains English text if needed
# text = pytesseract.image_to_string(Image.open(image_path), lang='eng')  
# print("Extracted English Text:", text)
