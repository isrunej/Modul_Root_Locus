# RUBRIK PENILAIAN TUGAS PRAKTIKUM
## Topik: Tempat Kedudukan Akar (Root Locus)
### Sistem Kontrol — Program Studi Teknik Elektro

---

**Bobot Total:** 100 poin
**Waktu Pengerjaan:** 1 minggu (take-home + sesi praktikum 2 × 50 menit)
**Format Pengumpulan:** File `.py` + semua gambar `.png` dalam satu folder ZIP

---

## RINGKASAN BOBOT PER SOAL

| Soal | Topik | Poin | Keterangan |
|------|-------|------|------------|
| 1 | Analisis Sistem Orde-2 | 25 | Wajib |
| 2 | Analisis Sistem Orde-3 + K Kritis | 25 | Wajib |
| 3 | Desain K Berdasarkan Spesifikasi | 25 | Wajib |
| 4 | Pengayaan: Efek Pole & Zero | 25 | Nilai tambah |
| **Total** | | **100** | |

> **Catatan:** Mahasiswa yang tidak mengerjakan Soal 4 dapat memperoleh maksimum **75 poin**. Soal 4 berfungsi sebagai **pengayaan** untuk menaikkan nilai ke rentang A.

---

## SOAL 1 — Analisis Sistem Orde-2 (25 poin)

### 1a. Definisi Fungsi Alih (3 poin)

| Kriteria | Poin Penuh | Sebagian | Tidak |
|----------|-----------|----------|-------|
| `num_G1` dan `den_G1` benar | 1 | 0.5 | 0 |
| Objek `tf()` terbentuk tanpa error | 1 | — | 0 |
| Output `cetak_info_sistem()` tampil poles/zeros yang benar | 1 | 0.5 | 0 |

### 1b. Perhitungan Manual (5 poin)

| Kriteria | Poin |
|----------|------|
| Poles G(s) benar: s=0 dan s=−4 | 1 |
| Jumlah asimtot benar: n−m = 2 | 0.5 |
| Sudut asimtot benar: ±90° | 0.5 |
| Centroid asimtot benar: σ_a = −2 | 1 |
| Break-away point benar: s = −2, K = 4 | 2 |

> **Panduan Koreksi Break-away:**
> dK/ds = 0 dimana K = −1/G(s).
> K = −s(s+4) = −s²−4s → dK/ds = −2s−4 = 0 → s = −2.
> K = −(−2)(−2+4) = 4. ✓

### 1c. Plot Root Locus (7 poin)

| Kriteria | Poin |
|----------|------|
| Root locus tergambar benar (dua cabang simetri) | 2 |
| Poles asal ditandai dengan × di posisi yang tepat | 1 |
| Tiga nilai K ditandai dengan simbol berbeda | 2 |
| Judul, label sumbu, legenda lengkap | 1 |
| Gambar tersimpan sebagai `soal1c_root_locus.png` | 1 |

**Deduction:** −1 poin jika asimtot tidak terlihat atau sumbu tidak proporsional.

### 1d. Respons Step Variasi K (5 poin)

| Kriteria | Poin |
|----------|------|
| Empat kurva K = 1, 4, 8, 16 tampil semua | 2 |
| Garis referensi r=1 dan band ±2% ada | 1 |
| Tren overshoot meningkat seiring K terlihat jelas | 1 |
| Gambar tersimpan sebagai `soal1d_respons_step.png` | 1 |

### 1e. Parameter Transien (5 poin)

| Kriteria | Poin |
|----------|------|
| Fungsi `hitung_parameter_respons()` dipanggil dengan K=4 | 1 |
| Rise time, settling time, overshoot, ess tampil | 1 |
| Jawaban pertanyaan analisis 1 (stabil ∀K>0) benar & berargumen | 1.5 |
| Jawaban pertanyaan analisis 2 (pengaruh K ke ts) benar | 1.5 |

**Kunci Jawaban 1e:**
- Sistem orde-2 tanpa zero **selalu stabil** untuk K>0 karena semua root locus berada di sisi kiri bidang-s (ke arah ±j∞).
- Menaikkan K meningkatkan ωn sehingga ts (≈4/ζωn) bisa naik atau turun tergantung perubahan ζ.

---

## SOAL 2 — Analisis Sistem Orde-3 + K Kritis (25 poin)

### 2a. Definisi G(s) (3 poin)

| Kriteria | Poin |
|----------|------|
| Penyebut s³+7s²+10s ditulis benar: `[1, 7, 10, 0]` | 2 |
| Poles tiga buah benar: 0, −2, −5 | 1 |

### 2b. Routh-Hurwitz Manual (7 poin)

| Kriteria | Poin |
|----------|------|
| Karakteristik CL: s³+7s²+10s+K ditulis benar | 1 |
| Tabel Routh disusun lengkap 4 baris | 2 |
| Elemen baris s¹: (70−K)/7 ditulis benar | 2 |
| Syarat stabil: K < 70 disimpulkan benar | 1 |
| K kritis = 70 dicantumkan pada variabel kode | 1 |

> **Kunci Tabel Routh:**
>
> | | Kolom 1 | Kolom 2 |
> |--|---------|---------|
> | s³ | 1 | 10 |
> | s² | 7 | K |
> | s¹ | (70−K)/7 | 0 |
> | s⁰ | K | — |
>
> Syarat: (70−K)/7 > 0 **dan** K > 0 → **0 < K < 70**.

### 2c. Verifikasi Simulasi (5 poin)

| Kriteria | Poin |
|----------|------|
| Tiga nilai K (bawah, kritis, atas) disimulasikan | 2 |
| Respons K < K_kritis konvergen | 1 |
| Respons K > K_kritis divergen/osilasi tak teredam | 1 |
| Gambar tersimpan sebagai `soal2c_verifikasi_K_kritis.png` | 1 |

**Toleransi Nilai K Kritis:** Jawaban diterima jika **65 ≤ K_kritis ≤ 75** (toleransi kesalahan pembulatan +7%).

### 2d. Dashboard & Analisis (10 poin)

| Kriteria | Poin |
|----------|------|
| `plot_dashboard_lengkap()` dipanggil dengan benar | 2 |
| Dashboard menampilkan 4 panel lengkap | 2 |
| Gambar tersimpan sebagai `soal2d_dashboard.png` | 1 |
| Jawaban: K_kritis manual vs simulasi dibandingkan | 2 |
| Jawaban: alasan orde-3 bisa tidak stabil (asimtot ke kanan) | 2 |
| Jawaban: trade-off K kecil vs mendekati K_kritis | 1 |

**Kunci Analisis 2d:**
- Orde-3 memiliki 3 asimtot (sudut ±60° dan 180°), asimtot 60° melewati kuadran kanan → cabang root locus bisa menyeberang sumbu imajiner.
- K kecil: lambat tapi stabil besar; K mendekati K_kritis: respons cepat tapi margin kecil, mudah tidak stabil akibat gangguan parameter.

---

## SOAL 3 — Desain K Berdasarkan Spesifikasi (25 poin)

### 3a. Konversi Spesifikasi ke Bidang-s (7 poin)

| Kriteria | Poin |
|----------|------|
| Rumus ζ dari %OS ditulis dan dihitung benar (ζ ≥ 0.517) | 3 |
| Rumus σ_min dari ts ditulis benar (σ_min ≥ 0.8) | 2 |
| Nilai `zeta_min` dan `sigma_min` di kode benar | 2 |

> **Kunci:**
> %OS = 15% → ζ = −ln(0.15)/√(π²+ln²(0.15)) ≈ **0.517**
> ts ≤ 5 s → ζωn ≥ 4/5 = **0.8** → Re(poles) ≤ **−0.8**

### 3b. Plot Root Locus + Daerah Spesifikasi (8 poin)

| Kriteria | Poin |
|----------|------|
| Root locus benar (dua cabang) | 2 |
| Garis vertikal batas ts di posisi benar (x = −0.8) | 2 |
| Garis diagonal batas %OS sudut benar | 2 |
| Arsiran daerah yang memenuhi spesifikasi ada | 1 |
| Gambar tersimpan sebagai `soal3b_root_locus_spesifikasi.png` | 1 |

### 3c. Scanning K Optimal (5 poin)

| Kriteria | Poin |
|----------|------|
| Loop scanning K diimplementasikan benar | 2 |
| Filter kondisi (%OS ≤ 15% **DAN** ts ≤ 5) benar | 2 |
| K_optimal dicetak ke konsol | 1 |

**Rentang K yang Diharapkan:** Sekitar **0.5 ≤ K_optimal ≤ 3.0** (tergantung granularitas scanning). Jawaban diterima selama parameter transien memenuhi spesifikasi.

### 3d. Verifikasi & Analisis (5 poin)

| Kriteria | Poin |
|----------|------|
| Dashboard K optimal tergambar dan tersimpan | 2 |
| Jawaban konflik OS vs ts dijawab dengan benar | 1.5 |
| Jawaban mengapa ess = 0 untuk sistem tipe-1 (integral) | 1.5 |

**Kunci ess = 0:** Sistem tipe 1 (ada satu integrator s di penyebut) memastikan untuk input step r(t)=1, error steady-state = 0 karena Kp → ∞.

---

## SOAL 4 — Pengayaan: Efek Pole & Zero (25 poin)

### 4a. Definisi Semua Varian (5 poin)

| Varian | Kode yang Benar | Poin |
|--------|----------------|------|
| G_A (zero s=−1) | `tf([1,1],[1,2,0])` | 1 |
| G_B (zero s=−3) | `tf([1,3],[1,2,0])` | 1 |
| G_C (pole s=−10) | `tf([1],[1,12,20,0])` | 1.5 |
| G_D (pole s=−1) | `tf([1],[1,3,2,0])` | 1.5 |

> **Kunci Penyebut:**
> s(s+2)(s+10) = s³+12s²+20s → `[1,12,20,0]`
> s(s+2)(s+1)  = s³+3s²+2s  → `[1,3,2,0]`

### 4b. Plot Komparatif Root Locus (10 poin)

| Kriteria | Poin |
|----------|------|
| Semua 5 subplot tergambar tanpa error | 3 |
| Poles dan zeros dibedakan dengan simbol berbeda di tiap subplot | 2 |
| Batas sumbu seragam memudahkan perbandingan visual | 2 |
| Judul tiap subplot informatif | 1 |
| Gambar tersimpan sebagai `soal4b_perbandingan_pole_zero.png` | 2 |

### 4c. Perbandingan Respons Step (5 poin)

| Kriteria | Poin |
|----------|------|
| Semua varian stabil diplot dengan warna/style berbeda | 2 |
| Legenda jelas mengidentifikasi tiap kurva | 1 |
| Tren perbedaan respons tampak jelas | 1 |
| Gambar tersimpan sebagai `soal4c_respons_step_perbandingan.png` | 1 |

### 4d. Pertanyaan Analisis (5 poin)

| Pertanyaan | Kunci Jawaban | Poin |
|-----------|--------------|------|
| Efek zero dekat vs jauh | Zero dekat origin "menarik" cabang RL ke kirinya → stabil lebih baik. Zero jauh kurang berpengaruh. | 1.5 |
| Pole jauh vs dekat | Pole jauh (s=−10) hampir tidak mempengaruhi root locus di dekat origin (dominan pole approx). Pole dekat (s=−1) mengubah bentuk signifikan. | 1.5 |
| Mengapa zero lead dekat origin | Zero dekat membuat kompensator menarik jalur ke kiri, meningkatkan margin kestabilan dan mempercepat respons. | 1 |
| 5 aturan root locus | Lihat kunci di bawah | 1 |

**Kunci 5 Aturan Root Locus:**
1. Jumlah cabang = jumlah poles OL (n).
2. Cabang dimulai di poles OL (K=0) dan berakhir di zeros OL atau ∞ (K→∞).
3. Root locus simetri terhadap sumbu real.
4. Bagian sumbu real: RL ada di sebelah kiri jika jumlah poles+zeros di kanannya adalah ganjil.
5. Sudut asimtot: (2k+1)×180°/(n−m), centroid: (ΣRe(poles)−ΣRe(zeros))/(n−m).
6. *(Bonus)* Break-away/break-in: dK/ds = 0.
7. *(Bonus)* Sudut keberangkatan dari pole kompleks: 180° − Σ∠zeros + Σ∠poles lain.

---

## KRITERIA PENILAIAN UMUM

### Kualitas Kode (deduction, berlaku untuk semua soal)

| Kondisi | Pengurangan |
|---------|-------------|
| Kode tidak bisa dijalankan (syntax error) tanpa perbaikan | −5 per soal |
| Tidak ada gambar yang tersimpan (savefig) | −2 per gambar |
| Variabel `???` tidak diisi | −1 per instance |
| Import tidak lengkap sehingga error | −3 |

### Laporan & Analisis

| Kriteria | Poin Bonus / Deduction |
|----------|------------------------|
| Semua pertanyaan analisis dijawab lengkap + argumen teori | +0 (sudah termasuk dalam poin soal) |
| Kesimpulan akhir ≥ 100 kata, relevan, berdasarkan data | +3 (bonus) |
| Penulisan jawaban sangat singkat tanpa penjelasan | −1 per pertanyaan |
| Copy-paste jawaban identik antar mahasiswa | −20 (indikasi plagiat) |

---

## KONVERSI NILAI

| Total Poin | Grade | Keterangan |
|-----------|-------|------------|
| 90 – 100 | A | Sangat Baik — menguasai semua konsep termasuk pengayaan |
| 80 – 89 | A− | Baik sekali |
| 70 – 79 | B+ | Baik — semua soal wajib benar, pengayaan sebagian |
| 60 – 69 | B | Cukup baik — soal wajib umumnya benar |
| 50 – 59 | C+ | Cukup — pemahaman dasar ada tapi banyak celah |
| 40 – 49 | C | Kurang — banyak konsep yang belum dipahami |
| < 40 | D/E | Tidak lulus — perlu mengulang |

---

## PANDUAN UNTUK ASISTEN/DOSEN PENILAI

### Urutan Koreksi yang Disarankan

1. **Jalankan kode terlebih dahulu** — pastikan tidak ada syntax error fatal.
2. Jika ada error pada Soal 1a, koreksi nilai `???` secara manual dan lanjutkan.
3. Periksa **gambar PNG** yang dihasilkan — kualitas visual adalah bagian dari penilaian.
4. Baca **jawaban analisis** di bagian komentar kode.
5. Cek **kesimpulan akhir** di bagian penutup.

### Kesalahan Umum yang Perlu Diantisipasi

| Kesalahan | Cara Menilai |
|-----------|-------------|
| Urutan koefisien terbalik (`[0, 4, 1]` bukan `[1, 4, 0]`) | −1, arahkan ke dokumentasi `tf()` |
| Lupa faktor K dalam `feedback(K * G, 1)` | −2 untuk soal terkait |
| K_kritis dari Routh salah karena kesalahan aritmatika tabel | Berikan setengah poin jika metode benar tapi angka salah |
| `zeta_min` dihitung dengan rumus yang berbeda tapi hasil sama | Diterima penuh |
| Scanning K menemukan nilai yang sedikit berbeda dari kunci | Diterima jika parameter transien terpenuhi |

### Deteksi Plagiat

- Bandingkan nilai `K_optimal` antar mahasiswa — kemungkinan besar berbeda karena granularitas `linspace`.
- Jika nilai identik **dan** teks jawaban sangat mirip, indikasi kuat plagiat → nilai 0 untuk kedua pihak dan laporkan ke koordinator.

---

## LAMPIRAN: KUNCI JAWABAN RINGKAS

### Soal 1
- G(s) = 1/(s²+4s): `num=[1]`, `den=[1,4,0]`
- Poles: 0, −4; Break-away: s=−2, K=4
- Sistem **selalu stabil** untuk K > 0

### Soal 2
- G(s) = 1/(s³+7s²+10s): `den=[1,7,10,0]`
- K kritis (Routh) = **70**
- Sistem orde-3 bisa tidak stabil karena asimtot 60° → kuadran kanan

### Soal 3
- ζ_min ≈ 0.517; σ_min = 0.8
- K_optimal ≈ 1.0–2.0 (tergantung granularitas scan)
- ess = 0 karena sistem tipe-1

### Soal 4
- G_C: `den=[1,12,20,0]` (s(s+2)(s+10))
- G_D: `den=[1,3,2,0]` (s(s+2)(s+1))
- Zero dekat origin menarik lintasan root locus ke kiri → stabilitas lebih baik

---

*Rubrik ini dapat dimodifikasi sesuai kebutuhan. Versi terakhir: Mei 2026.*
