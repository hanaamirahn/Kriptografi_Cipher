# Aplikasi Enkripsi dan Dekripsi Cipher

Aplikasi ini memungkinkan pengguna untuk mengenkripsi dan mendekripsi teks menggunakan tiga metode cipher: **Vigenere Cipher**, **Playfair Cipher**, dan **Hill Cipher**. Program ini menggunakan antarmuka grafis berbasis Tkinter untuk interaksi pengguna.

## Fitur

- **Enkripsi dan Dekripsi** teks menggunakan tiga metode cipher:
  - Vigenere Cipher
  - Playfair Cipher
  - Hill Cipher
- Mengunggah teks dari file `.txt`.
- Menyediakan input teks dan kunci secara manual.
- Menampilkan hasil enkripsi dan dekripsi di area output.

## Persyaratan

- Python 3.x
- Pustaka Python:
  - `tkinter` (untuk GUI)
  - `numpy` (untuk operasi matematika)

## Cara Menjalankan Program

### Langkah 1: Install Dependencies

Pastikan Python 3.x telah terinstal di komputer Anda. Kemudian, instal `numpy` dengan menggunakan pip:

```bash
pip install numpy
```

### Langkah 2: Jalankan Program

- Unduh dan simpan file Python **`cipher_gui.py`** ke dalam folder di komputer Anda.
- Jalankan program dengan perintah berikut:
  ```
  python cipher_gui.py
  ```
- Antarmuka Pengguna akan muncul, di mana Anda dapat memasukkan teks atau mengunggah file teks dan memasukkan kunci untuk melakukan enkripsi atau dekripsi.


### Langkah 3: Menggunakan Program

- Masukkan teks yang ingin dienkripsi atau didekripsi pada bagian "Input Text / File".
  - Anda dapat menulis teks secara langsung di area input.
  - Atau, klik tombol "Upload File" untuk mengunggah file teks.
- Masukkan kunci pada bagian "Key (min 12 chars)". Kunci harus terdiri dari minimal 12 karakter.
- Pilih metode cipher:
  - Vigenere
  - Playfair
  - Hill
- Pilih tindakan:
  - Klik tombol **Encrypt** untuk mengenkripsi teks.
  - Klik tombol **Decrypt** untuk mendekripsi teks.
- Lihat hasilnya di bagian "Output".
