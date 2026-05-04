# Modul Simulasi Tempat Kedudukan Akar (*Root Locus*)
**Sistem Kontrol — Teknik Elektro**

---

## 🚀 Mulai Cepat

### Notebook

| | File | Keterangan |
|--|------|-----------|
| [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/isrunej/Modul_Root_Locus/blob/main/01_demo_root_locus.ipynb) | `01_demo_root_locus.ipynb` | Tutorial & demo fungsi simulasi |
| [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/isrunej/Modul_Root_Locus/blob/main/02_tugas_mahasiswa.ipynb) | `02_tugas_mahasiswa.ipynb` | Template tugas mahasiswa |

> Tidak perlu instalasi — semua berjalan langsung di browser via Google Colab.

### Simulasi Interaktif (Browser)

[![Buka Simulator](https://img.shields.io/badge/🎛️%20Buka%20Simulator%20Root%20Locus-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white)](https://isrunej.github.io/Modul_Root_Locus/rlocus-simulator.html)

Simulasi berbasis JavaScript — jalankan langsung di browser tanpa instalasi apapun.

---

## 📁 Isi Repositori

| File | Untuk | Deskripsi |
|------|-------|-----------|
| `01_demo_root_locus.ipynb` | Dosen / mahasiswa | Tutorial interaktif: 4 demo lengkap |
| `02_tugas_mahasiswa.ipynb` | Mahasiswa | Template tugas dengan `???` yang diisi |
| `rlocus-simulator.html` | Semua | Simulator root locus berbasis JS |
| `rubrik_penilaian.md` | Dosen | Rubrik penilaian lengkap + kunci jawaban |
| `root_locus_simulasi.py` | Referensi | Versi script Python (opsional) |

---

## 📓 Isi Notebook

### `01_demo_root_locus.ipynb` — Tutorial (24 sel)

Jalankan sel dari atas ke bawah. Instalasi library otomatis di sel pertama.

- **Demo 1** — Sistem orde-2: root locus, variasi K, parameter transien
- **Demo 2** — Sistem orde-3: dashboard 4-panel (RL + Step + Bode + Tabel)
- **Demo 3** — Perbandingan visual efek penambahan zero
- **Demo 4** — Pencarian K kritis otomatis + plot Re(poles) vs K
- **Fungsi eksplorasi** — `analisis_cepat(num, den, K)` untuk sistem bebas

### `02_tugas_mahasiswa.ipynb` — Tugas (45 sel)

Mahasiswa mengisi bagian `???` dan menjawab pertanyaan di sel Markdown.

| Soal | Topik | Poin |
|------|-------|------|
| 1 | Sistem orde-2: G(s) = K/[s(s+4)] | 25 |
| 2 | Sistem orde-3 + K kritis (Routh-Hurwitz) | 25 |
| 3 | Desain K dari spesifikasi %OS dan ts | 25 |
| 4 *(pengayaan)* | Efek penambahan pole & zero | 25 |

---

## 🌐 Halaman Web

Semua materi juga dapat diakses di:
**[https://isrunej.github.io/Modul_Root_Locus/](https://isrunej.github.io/Modul_Root_Locus/)**

---

*Referensi: Ogata K., Modern Control Engineering, 5th ed.*
