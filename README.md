# PCD_Pothole-Alert
# 🕳️ PotholeAlert: Deteksi Lubang Jalan Berbasis Citra Drone dengan YOLOv5

**PotholeAlert** adalah aplikasi berbasis Python GUI yang menggunakan model deep learning YOLOv5 untuk mendeteksi lubang jalan dari citra drone. Aplikasi ini memanfaatkan kemampuan deteksi objek dari YOLO (You Only Look Once) dan dirancang agar mudah digunakan melalui antarmuka grafis (GUI).

---

## 🖼️ Fitur Utama

- Deteksi lubang jalan secara otomatis dari gambar.
- Antarmuka pengguna sederhana menggunakan Tkinter.
- Hasil deteksi divisualisasikan dan disimpan otomatis.
- Melatih model sendiri berdasarkan dataset kustom.

---

## 🗂️ Struktur Proyek
     ├── README.md
     yolov5/
     ├── dataset/
     │ ├── images/
     │ │ ├── train/
     │ │ └── val/
     │ └── labels/
     │ ├── train/
     │ └── val/
     ├── pothole.yaml
     ├── pothole_alert_gui.py
     ├── runs/
     │ └── train/
     │ └── pothole_detect/
     │ └── weights/
     │ └── best.pt
     ├── train.py
     ├── detect.py
     └── ...


---

## 🛠️ Instalasi

1. **Clone YOLOv5**

       git clone https://github.com/ultralytics/yolov5
       cd yolov5

2. **Install dependency**

       pip install -r requirements.txt
   
Tambahan jika belum terinstal:

     pip install pillow opencv-python tkinter


# 🏷️ Membuat Label YOLO (Anotasi)

Untuk membuat file label .txt dari gambar .jpg/.png kamu bisa gunakan website:

    👉 https://www.makesense.ai/

Langkah-langkah:

    Buka https://www.makesense.ai.

Klik "Get Started" → Upload gambar citra lubang jalan.

Pilih "Object Detection" → masukkan nama label (misalnya pothole).

Gambar bounding box di setiap lubang jalan.

Setelah selesai, klik Export → Pilih format YOLO.

Download hasil .txt dan letakkan di folder:


    dataset/labels/train/
    dataset/labels/val/

# Pelatihan Model (Training)

Siapkan dataset seperti ini:

    dataset/
    ├── images/
    │   ├── train/
    │   └── val/
    └── labels/
        ├── train/
        └── val/
Buat file konfigurasi pothole.yaml:

     train: dataset/images/train
     val: dataset/images/val
     nc: 1 <- itu jumlah gambar yang bisa di deteksi (jangan lupa di ganti)
     names: ['pothole']
Jalankan training:

     python train.py --img 640 --batch 16 --epochs 50 --data pothole.yaml --weights yolov5s.pt --project runs/train --name pothole_detect

Hasil model akan ada di:

     runs/train/pothole_detect/weights/best.pt

Buat yolov5/pothole_alert_gui.py:
     
    import tkinter as tk
    from tkinter import filedialog
    from PIL import Image, ImageTk
    import torch
    import cv2
    import os

    # Load model hasil training
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='runs/train/pothole_detect/weights/best.pt', force_reload=True)

    latest_result_path = None
    cap = None
    webcam_running = False

    def detect_pothole(image_path):
       global latest_result_path
       results = model(image_path)
       results.save()
    
       detect_dir = 'runs/detect'
       folders = [os.path.join(detect_dir, f) for f in os.listdir(detect_dir) if os.path.isdir(os.path.join(detect_dir, f))]
       latest_folder = max(folders, key=os.path.getmtime)
       result_files = [f for f in os.listdir(latest_folder) if f.lower().endswith(('.jpg', '.png'))]
    if result_files:
        latest_result_path = os.path.join(latest_folder, result_files[0])
        return results
    else:
        latest_result_path = None
        return None

    def show_result():
       if not latest_result_path:
          return
       img = cv2.imread(latest_result_path)
       img = cv2.resize(img, (480, 360))
       img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
       img_pil = Image.fromarray(img)
       photo = ImageTk.PhotoImage(img_pil)
       panel.config(image=photo)
       panel.image = photo

       detections = model(latest_result_path)
       df = detections.pandas().xyxy[0]
       count = len(df)
       label_result.config(text=f"Lubang terdeteksi: {count}")

    def browse_image():
       file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if file_path:
        stop_webcam()
        detect_pothole(file_path)
        show_result()

    def update_frame():
      global cap
    if cap is None or not webcam_running:
        return
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (480, 360))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        panel.imgtk = imgtk
        panel.config(image=imgtk)
    panel.after(10, update_frame)

    def start_webcam(device_id=0):
      global cap, webcam_running
      stop_webcam()
      cap = cv2.VideoCapture(device_id)
    if not cap.isOpened():
        label_result.config(text=f"Error: Tidak bisa membuka webcam device {device_id}")
        return
    webcam_running = True
    label_result.config(text=f"Webcam device {device_id} aktif. Klik 'Capture Foto' untuk deteksi.")
    update_frame()

    def stop_webcam():
       global cap, webcam_running
       webcam_running = False
    if cap:
        cap.release()
    # Clear panel
    panel.config(image='')
    panel.image = None

    def capture_photo():
       global cap, webcam_running
    if not webcam_running or cap is None:
        label_result.config(text="Webcam belum aktif!")
        return
    ret, frame = cap.read()
    if ret:
        temp_path = "temp_capture.jpg"
        cv2.imwrite(temp_path, frame)
        detect_pothole(temp_path)
        show_result()
        label_result.config(text="Foto di-capture dan diproses.")
    else:
        label_result.config(text="Gagal capture foto.")

    # Fungsi cari webcam yang tersedia (cek device 0 sampai 4)
    def find_available_cameras(max_test=5):
      available = []
       for i in range(max_test):
        test_cap = cv2.VideoCapture(i)
        if test_cap.isOpened():
            available.append(i)
            test_cap.release()
    return available

    root = tk.Tk()
    root.title("PotholeAlert - Deteksi Lubang Jalan")
    root.geometry("540x650")
    root.configure(bg="white")

    btn_file = tk.Button(root, text="Pilih Gambar & Deteksi", command=browse_image,
                     bg="#0a84ff", fg="white", font=("Helvetica", 12, "bold"))
    btn_file.pack(pady=10)

    # Dropdown untuk pilih device webcam
     available_cams = find_available_cameras()
     selected_cam = tk.IntVar(value=available_cams[0] if available_cams else 0)

    cam_frame = tk.Frame(root, bg="white")
    cam_frame.pack(pady=5)
    tk.Label(cam_frame, text="Pilih Kamera:", bg="white", font=("Helvetica", 12)).pack(side=tk.LEFT)

    cam_dropdown = tk.OptionMenu(cam_frame, selected_cam, *available_cams)
    cam_dropdown.config(font=("Helvetica", 12))
    cam_dropdown.pack(side=tk.LEFT, padx=5)

    btn_start_cam = tk.Button(root, text="Aktifkan Webcam", command=lambda: start_webcam(selected_cam.get()),
                          bg="#10ac84", fg="white", font=("Helvetica", 12, "bold"))
    btn_start_cam.pack(pady=10)

    btn_capture = tk.Button(root, text="Capture Foto", command=capture_photo,
                        bg="#ff6b6b", fg="white", font=("Helvetica", 12, "bold"))
    btn_capture.pack(pady=10)

    panel = tk.Label(root)
    panel.pack()

    label_result = tk.Label(root, text="", font=("Helvetica", 12), bg="white")
    label_result.pack(pady=5)

    root.protocol("WM_DELETE_WINDOW", lambda: (stop_webcam(), root.destroy()))
    root.mainloop()

▶️ Menjalankan Aplikasi GUI

Setelah file best.pt tersedia, jalankan GUI:

     python pothole_alert_gui.py
     
Langkah:

Klik tombol "Pilih Gambar & Deteksi".

Pilih gambar dari citra drone.

Hasil akan ditampilkan di jendela aplikasi dan disimpan otomatis ke folder runs/detect/.

❗ Catatan Penting

Pastikan folder dataset dan file .yaml tidak typo.

Gunakan dataset dengan anotasi format YOLO (.txt) untuk setiap gambar.

Semakin banyak variasi citra lubang jalan, semakin baik akurasi model.

👤 Author

Nama: Mohamad Faris Fadil

Judul Proyek: PotholeAlert – Aplikasi Deteksi Lubang Jalan Berbasis Citra Drone

📄 Lisensi

Proyek ini dibuat untuk keperluan pembelajaran dan penelitian. Bebas digunakan untuk keperluan non-komersial.

# Dokumentasi Video Bisa di lihat disini:

[![Watch the video](https://img.youtube.com/vi/8GUCpbSxczg/maxresdefault.jpg)](https://youtu.be/8GUCpbSxczg)

### [Watch this video on YouTube](https://youtu.be/8GUCpbSxczg)
