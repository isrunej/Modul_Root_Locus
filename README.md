# Modul Simulasi Tempat Kedudukan Akar (Root Locus)
**Sistem Kontrol — Teknik Elektro**

## File Utama (Notebook — pakai di Google Colab)

| File | Untuk | Deskripsi |
|------|-------|-----------|
| `01_demo_root_locus.ipynb` | Dosen / mahasiswa | Tutorial interaktif: 4 demo lengkap |
| `02_tugas_mahasiswa.ipynb` | Mahasiswa | Template tugas dengan ??? yang diisi |
| `rubrik_penilaian.md` | Dosen | Rubrik penilaian + kunci jawaban |

> File `.py` tetap tersedia sebagai referensi, tapi **notebook adalah versi utama**.

## Buka di Google Colab

Klik tombol di bawah (setelah repo di-push ke GitHub):

```
https://colab.research.google.com/github/<username>/<repo>/blob/main/01_demo_root_locus.ipynb
https://colab.research.google.com/github/<username>/<repo>/blob/main/02_tugas_mahasiswa.ipynb
```

Atau dari Colab: **File → Open notebook → GitHub → cari repo ini**.

Instalasi library dilakukan otomatis oleh sel pertama (`%pip install -q control`).

## Isi Notebook

### `01_demo_root_locus.ipynb` — Tutorial (24 sel)
- Setup & semua fungsi bantu
- **Demo 1** — Sistem orde-2, root locus + variasi K
- **Demo 2** — Sistem orde-3, dashboard 4-panel
- **Demo 3** — Perbandingan efek penambahan zero
- **Demo 4** — Pencarian K kritis otomatis

### `02_tugas_mahasiswa.ipynb` — Tugas (45 sel)

| Soal | Topik | Poin |
|------|-------|------|
| 1 | Sistem orde-2: G(s) = K/[s(s+4)] | 25 |
| 2 | Sistem orde-3 + K kritis (Routh-Hurwitz) | 25 |
| 3 | Desain K dari spesifikasi %OS dan ts | 25 |
| 4 *(pengayaan)* | Efek penambahan pole & zero | 25 |
