## 🐐 BerbagiQurban
**BerbagiQurban** adalah aplikasi web yang memudahkan masyarakat muslim untuk berpartisipasi dalam ibadah kurban secara digital. Aplikasi ini juga membantu panitia kurban atau organisasi masjid dalam mengelola voucher kurban secara efisien dan transparan.

## 🙌 Kontributor
Proyek ini dibuat dengan ❤️ untuk memenuhi tugas praktikum **Pengembangan Perangkat Lunak (PPL)**.

- 👩‍💻 Nama:**Cut Sula Fathia Rahma**
           **Fathiya namira fardhi**
           **Iwani Khairina**
---
## 📌 Fitur Utama

## Untuk Masyarakat (User)
- Registrasi dan Login
- Melihat daftar voucher hewan kurban
- Filter berdasarkan lokasi, jenis hewan, harga
- Klaim voucher kurban dengan mengisi form
- Menerima informasi lokasi dan jadwal kurban

## Untuk Panitia / Admin
- Login admin
- Tambah dan edit data voucher hewan kurban
- Kelola slot, harga, waktu, dan lokasi penyembelihan
- Melihat daftar peserta yang sudah mengklaim
---
## ⚙️ Teknologi yang Digunakan

- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Backend**: Django (Python)
- **Database**: SQLite (default) / PostgreSQL (opsional)
- **Desain UI/UX**: Figma
Link : https://www.figma.com/design/wMaQR5FLJFYuBJrmPtAZ4B/berbagiqurban?node-id=1-2&t=UPsR4SMuAHobUEs8-1
```bash 
Frontend (HTML, css, JS)
↓
Backend API (Django)
↓
Database (SQLite / PostgreSQL)
```

---
## 🚀 Instalasi & Setup

## 1. Clone Repository
```bash
git clone https://github.com/namamu/berbagiqurban.git](https://github.com/iwanikhairina/Kelompok6-PPL-UAS
cd berbagiqurban
```
##2. Install Dependency Python
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows

pip install -r requirements.txt
```
##3. Migrasi Database
```bash
python manage.py migrate
```
##4. Jalankan Server
```bash
python manage.py runserver
```

##🔐 Role Pengguna
Role	Deskripsi
User	Masyarakat yang ingin klaim kurban
Admin	Panitia Kurban/Masjid yang mengelola voucher

##🧪 Pengujian
1. Manual Testing: Semua fitur diuji dengan interaksi langsung.
2. User Testing: Feedback dari calon pengguna komunitas.
3. Hasil: Sistem berjalan baik pada klaim, login, dan manajemen voucher.

###🙏 Terima Kasih
Semoga aplikasi ini membantu memperluas kebermanfaatan kurban di era digital.
#BerbagiQurban #DigitalIbadah #KurbanMudah



