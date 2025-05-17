import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import torch
import cv2
import os

# Load model hasil training kamu (pastikan path ini benar)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='runs/train/pothole_detect/weights/best.pt', force_reload=False)

# Fungsi deteksi lubang jalan
def detect_pothole(image_path):
    results = model(image_path)
    results.save()  # simpan hasil deteksi (gambar dengan kotak) di runs/detect/exp
    return results

# Fungsi untuk menampilkan hasil deteksi ke GUI
def show_result():
    latest_folder = sorted(os.listdir('runs/detect'), reverse=True)[0]
    folder_path = os.path.join('runs/detect', latest_folder)
    
    # Ambil nama file hasil
    result_file = os.listdir(folder_path)[0]
    result_path = os.path.join(folder_path, result_file)

    # Tampilkan dengan OpenCV + PIL
    img = cv2.imread(result_path)
    img = cv2.resize(img, (480, 360))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img)
    photo = ImageTk.PhotoImage(img_pil)

    panel.config(image=photo)
    panel.image = photo

    # Tambahkan jumlah deteksi ke label
    detections = model(result_path)
    df = detections.pandas().xyxy[0]
    count = len(df)
    label_result.config(text=f"Lubang terdeteksi: {count}")

# Fungsi saat klik tombol
def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if file_path:
        detect_pothole(file_path)
        show_result()

# GUI Tkinter
root = tk.Tk()
root.title("PotholeAlert - Deteksi Lubang Jalan")
root.geometry("520x500")
root.configure(bg="white")

btn = tk.Button(root, text="Pilih Gambar & Deteksi", command=browse_image,
                bg="#0a84ff", fg="white", font=("Helvetica", 12, "bold"))
btn.pack(pady=10)

panel = tk.Label(root)
panel.pack()

label_result = tk.Label(root, text="", font=("Helvetica", 12), bg="white")
label_result.pack(pady=5)

root.mainloop()
