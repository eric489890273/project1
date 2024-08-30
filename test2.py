import pytesseract
from PIL import Image

# 設定Tesseract的安裝路徑（視您的安裝路徑而定）
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 讀取圖片
image = Image.open(r"C:\Users\user\Desktop\STlight.RptWordAcceptance\photo\UploadFiles\LightLog\404832_1.jpg")

# 使用Tesseract OCR進行文字識別
text = pytesseract.image_to_string(image, config='--psm 6')

print(f'識別的文字: {text}')
