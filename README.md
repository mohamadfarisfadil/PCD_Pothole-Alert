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

Pelatihan Model (Training)
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
