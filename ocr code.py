import cv2
import pytesseract
from pytesseract import Output
from tkinter import Tk, Label, Text, Scrollbar, Button, Frame, filedialog, Scale,  VERTICAL 
from PIL import Image, ImageTk
import re

# تحديد مسار Tesseract (لو بتستخدم Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image_path = None  # تعريف متغير لمسار الصورة

# *دالة لاختيار الصورة من الجهاز*
def select_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    if image_path:
        process_image()

# *دالة لتحليل الصورة وعرض النص*
def process_image():
    global image_path
    if not image_path:
        text_box.delete("1.0", "end")
        text_box.insert("1.0", "Error: No image selected.")
        return

    # تحميل الصورة
    image = cv2.imread(image_path)
    if image is None:
        text_box.delete("1.0", "end")
        text_box.insert("1.0", "Error: Unable to load image.")
        return

    # استخراج النص من الصورة الأصلية
    extracted_text = pytesseract.image_to_string(image, lang='ara+eng')

    # تعريف الدالة لاستخراج القيم
    def extract_values(text):
        data = {}
        patterns = {
            "pH": r"pH\s*:\s*(\d+\.?\d*)",
            "Specific Gravity": r"Specific Gravity\s*:\s*(\d+)",
            "Pus Cells": r"Pus Cells\s*:\s*(\d+-\d+)",
            "R.B.Cs": r"R\.B\.Cs\s*:\s*(\d+-\d+)",
            "Crystals": r"Crystals\s*:\s*(\w+\s?\+*)"
        }
        for key, pattern in patterns.items():
            match = re.search(pattern, text)
            if match:
                data[key] = match.group(1)
        return data

    # استخراج القيم من النص المستخرج
    result = extract_values(extracted_text)
    print("Extracted Values:")
    print(result)

    # عرض الصورة الأصلية في واجهة Tkinter
    img = Image.open(image_path)
    img = img.resize((400, 400), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    img_label.config(image=img_tk)
    img_label.image = img_tk

    # عرض النص المستخرج في مربع النصوص
    text_box.delete("1.0", "end")
    text_box.insert("1.0", extracted_text)

# *دالة لحفظ النص المعدل*
def save_text():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_box.get("1.0", "end").strip())

# *واجهة Tkinter*
root = Tk()
root.title("OCR Analyzer")

# إطار لعرض الصورة
image_frame = Frame(root, width=400, height=400, bg="gray")
image_frame.grid(row=0, column=0, padx=10, pady=10)

img_label = Label(image_frame, text="Original Image will be displayed here", bg="gray")
img_label.pack(expand=True, fill="both")

# إطار لعرض النص
text_frame = Frame(root)
text_frame.grid(row=0, column=1, padx=10, pady=10)

text_box = Text(text_frame, wrap="word", width=50, height=20)
text_box.pack(side="left", fill="both", expand=True)

scrollbar = Scrollbar(text_frame, command=text_box.yview)
scrollbar.pack(side="right", fill="y")
text_box.config(yscrollcommand=scrollbar.set)

# أزرار التحكم
button_frame = Frame(root)
button_frame.grid(row=1, column=0, columnspan=2, pady=10)

btn_select = Button(button_frame, text="Select Image", command=select_image)
btn_select.pack(side="left", padx=5)

btn_process = Button(button_frame, text="Process Image", command=process_image)
btn_process.pack(side="left", padx=5)

btn_save = Button(button_frame, text="Save Text", command=save_text)
btn_save.pack(side="left", padx=5)

# تشغيل التطبيق
root.mainloop()
