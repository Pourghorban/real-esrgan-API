import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import replicate
import requests
import os
import io

os.environ["REPLICATE_API_TOKEN"] = "r8_dfsE678NclJgm2y3ScNEuLQx2ZWa5rT2WPTtx"


# تابع برای اجرای مدل و نمایش نتیجه
def run_model(image_path):
    output = replicate.run(
        "jingyunliang/swinir:660d922d33153019e8c263a3bba265de882e7f4f70396546b6c9c8f9d47a021a",
        input={"image": open(image_path, "rb")}
    )

    response = requests.get(output)
    image = Image.open(io.BytesIO(response.content))
    image.show()


# تابع برای باز کردن و انتخاب عکس
def open_image():
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=(("Image Files", "*.png *.jpg *.jpeg"), ("All Files", "*.*"))
    )
    if file_path:
        # نمایش عکس در پنجره
        image = Image.open(file_path)
        image.thumbnail((300, 300))  # تغییر اندازه عکس برای نمایش در پنجره
        photo = ImageTk.PhotoImage(image)
        image_label.configure(image=photo)
        image_label.image = image  # تغییر این خط
        # اجرای مدل و نمایش نتیجه
        run_model(file_path)



def save_image():
    if image_label.image:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=(("PNG Files", "*.png"), ("All Files", "*.*"))
        )
        if file_path:
            image_label.image.save(file_path)



# ایجاد پنجره اصلی
root = tk.Tk()
root.title("Image Super Resolution")
root.geometry("400x450")

# ایجاد دکمه و برچسب برای نمایش عکس
open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack(pady=10)

image_label = tk.Label(root)
image_label.pack()

# ایجاد دکمه برای ذخیره عکس
save_button = tk.Button(root, text="Save Image", command=save_image)
save_button.pack(pady=10)

root.mainloop()
