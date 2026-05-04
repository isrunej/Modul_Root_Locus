"""
==============================================================
TUGAS PRAKTIKUM: TEMPAT KEDUDUKAN AKAR (ROOT LOCUS)
Sistem Kontrol — Teknik Elektro
==============================================================
Nama    : ___________________________________
NIM     : ___________________________________
Kelas   : ___________________________________
Tanggal : ___________________________________

PETUNJUK UMUM:
  1. Kerjakan setiap soal secara berurutan.
  2. Lengkapi semua bagian yang ditandai  # ← ANDA ISIAN DI SINI
  3. Jalankan tiap sel/soal dan amati hasilnya.
  4. Jawab semua pertanyaan analisis di bagian komentar.
  5. Kumpulkan file .py ini beserta semua gambar yang dihasilkan.

KRITERIA KELULUSAN MINIMUM:
  - Soal 1–3 wajib dikerjakan (bobot 75%)
  - Soal 4 pengayaan (bobot 25%)

Impor semua fungsi dari modul simulasi sebelum mulai.
==============================================================
"""

# ──────────────────────────────────────────────────────────────
# IMPOR LIBRARY (jangan diubah)
# ──────────────────────────────────────────────────────────────
import numpy as np
import matplotlib.pyplot as plt
import control
from control import tf, feedback, step_response

# Impor fungsi dari modul simulasi buatan dosen
from root_locus_simulasi import (
    cetak_info_sistem,
    hitung_parameter_respons,
    plot_root_locus,
    plot_respons_step_variasi_K,
    plot_dashboard_lengkap,
    analisis_sistem,
)


# ══════════════════════════════════════════════════════════════
#  SOAL 1 — ANALISIS SISTEM ORDE-2  (25 poin)
# ══════════════════════════════════════════════════════════════
"""
LATAR BELAKANG:
  Sebuah sistem kontrol posisi motor DC memiliki fungsi alih
  loop-terbuka:

             K
  G(s) = ──────────
          s(s + 4)

  Sistem menggunakan umpan balik satuan (H(s) = 1).

TUJUAN:
  - Menggambar dan menganalisis root locus sistem orde-2.
  - Memahami hubungan antara posisi poles dan respons transien.
  - Menentukan nilai K untuk spesifikasi tertentu.
"""

print("=" * 60)
print("SOAL 1 — Sistem Orde-2: G(s) = K / [s(s+4)]")
print("=" * 60)

# ─────────────────────────────────────────────────────────────
# 1a. Definisikan fungsi alih G(s)  [3 poin]
#     Ganti tanda ??? dengan koefisien yang benar.
# ─────────────────────────────────────────────────────────────

# G(s) = 1 / (s^2 + 4s) = 1 / [s(s+4)]
# tf(pembilang, penyebut)  — koefisien dari pangkat TERTINGGI ke terendah
num_G1 = [???]          # ← koefisien pembilang
den_G1 = [???, ???, ???]  # ← koefisien penyebut s^2 + 4s + 0

G1 = tf(num_G1, den_G1)
cetak_info_sistem(G1, "G(s) = 1/[s(s+4)]")


# ─────────────────────────────────────────────────────────────
# 1b. Hitung secara manual (isi di komentar)  [5 poin]
# ─────────────────────────────────────────────────────────────
"""
HITUNG MANUAL — isi jawaban Anda di sini:

  Poles G(s)        : s1 = _____  , s2 = _____
  Zeros G(s)        : (ada/tidak ada) = _____
  Jumlah asimtot    : n - m = _____
  Sudut asimtot     : _____ °
  Centroid asimtot  : σ_a = _____

  Break-away point  :
    Persamaan: dK/ds = 0  →  _______________________
    Jawaban  : s = _____
    K saat break-away = _____
"""


# ─────────────────────────────────────────────────────────────
# 1c. Plot Root Locus  [7 poin]
#     Tandai K = 1, 4, dan 8 pada plot.
# ─────────────────────────────────────────────────────────────

fig1c, ax1c = plot_root_locus(
    G1,
    judul="Root Locus — G(s) = 1/[s(s+4)]",
    K_tandai=[???, ???, ???]   # ← isi 3 nilai K
)
fig1c.savefig("soal1c_root_locus.png", bbox_inches='tight')
plt.show()
print("→ Gambar disimpan: soal1c_root_locus.png")


# ─────────────────────────────────────────────────────────────
# 1d. Plot respons step untuk K = 1, 4, 8, 16  [5 poin]
# ─────────────────────────────────────────────────────────────

fig1d, ax1d = plot_respons_step_variasi_K(
    G1,
    nilai_K=[1, 4, 8, ???],    # ← tambahkan K = 16
    t_max=10,
    judul="Respons Step — G(s) = 1/[s(s+4)]"
)
fig1d.savefig("soal1d_respons_step.png", bbox_inches='tight')
plt.show()
print("→ Gambar disimpan: soal1d_respons_step.png")


# ─────────────────────────────────────────────────────────────
# 1e. Hitung parameter transien untuk K = 4  [5 poin]
# ─────────────────────────────────────────────────────────────

K_soal1e = ???           # ← ganti dengan nilai K = 4

cl_G1 = feedback(K_soal1e * G1, 1)
t1 = np.linspace(0, 10, 2000)
t_out1, y_out1 = step_response(cl_G1, T=t1)
par1 = hitung_parameter_respons(t_out1, y_out1,
                                 nama=f"Soal 1e, K={K_soal1e}")

"""
PERTANYAAN ANALISIS 1e (jawab di sini):

  1. Berapa nilai % Overshoot untuk K = 4?
     Jawab: _______

  2. Apakah sistem stabil untuk semua nilai K > 0? Jelaskan!
     Jawab: _______

  3. Bagaimana pengaruh menaikkan K terhadap settling time?
     Jawab: _______
"""


# ══════════════════════════════════════════════════════════════
#  SOAL 2 — ANALISIS SISTEM ORDE-3  (25 poin)
# ══════════════════════════════════════════════════════════════
"""
LATAR BELAKANG:
  Sistem kendali level cairan pada reaktor kimia memiliki
  fungsi alih:

                    K
  G(s) = ────────────────────
          s(s + 2)(s + 5)

TUJUAN:
  - Menganalisis root locus sistem orde-3.
  - Menentukan K kritis menggunakan kriteria Routh-Hurwitz.
  - Memverifikasi K kritis dengan simulasi.
"""

print("\n" + "=" * 60)
print("SOAL 2 — Sistem Orde-3: G(s) = K / [s(s+2)(s+5)]")
print("=" * 60)

# ─────────────────────────────────────────────────────────────
# 2a. Definisikan G(s)  [3 poin]
#     Kalikan penyebut: s(s+2)(s+5) = s^3 + 7s^2 + 10s
# ─────────────────────────────────────────────────────────────

# G(s) = 1 / (s^3 + 7s^2 + 10s)
num_G2 = [???]
den_G2 = [???, ???, ???, ???]   # ← 4 koefisien untuk s^3

G2 = tf(num_G2, den_G2)
cetak_info_sistem(G2, "G(s) = 1/[s(s+2)(s+5)]")


# ─────────────────────────────────────────────────────────────
# 2b. Hitung K kritis menggunakan Routh-Hurwitz  [7 poin]
# ─────────────────────────────────────────────────────────────
"""
PERHITUNGAN ROUTH-HURWITZ:

  Karakteristik loop tertutup: 1 + KG(s) = 0
  → s^3 + 7s^2 + 10s + K = 0

  Tabel Routh:
    s^3 |  1   |  10  |
    s^2 |  7   |  K   |
    s^1 |  ??? |   0  |   ← isi nilai elemen ini (dalam K)
    s^0 |  K   |      |

  Syarat stabil (semua elemen kolom 1 > 0):
    Baris s^1: ________ > 0  →  K < ________
    Baris s^0:  K > 0

  K kritis = ________

  Simpan jawaban Anda:
"""
K_kritis_manual = ???   # ← isi nilai K kritis hasil Routh-Hurwitz


# ─────────────────────────────────────────────────────────────
# 2c. Verifikasi K kritis dengan simulasi  [5 poin]
# ─────────────────────────────────────────────────────────────

# Plot respons step untuk K di bawah, tepat, dan di atas K kritis
K_bawah = K_kritis_manual * 0.5
K_tepat = K_kritis_manual
K_atas  = K_kritis_manual * 1.5

fig2c, ax2c = plot_respons_step_variasi_K(
    G2,
    nilai_K=[K_bawah, K_tepat, K_atas],
    t_max=30,
    judul=f"Verifikasi K Kritis ≈ {K_kritis_manual}"
)
fig2c.savefig("soal2c_verifikasi_K_kritis.png", bbox_inches='tight')
plt.show()
print("→ Gambar disimpan: soal2c_verifikasi_K_kritis.png")


# ─────────────────────────────────────────────────────────────
# 2d. Dashboard lengkap untuk K desain  [5 poin]
#     Pilih K desain = 0.5 × K_kritis (margin keamanan 50%)
# ─────────────────────────────────────────────────────────────

K_desain_soal2 = round(K_kritis_manual * 0.5, 2)
print(f"\nK desain (50% dari K kritis): {K_desain_soal2}")

fig2d = plot_dashboard_lengkap(
    G2,
    K_desain=K_desain_soal2,
    nama_sistem="Soal 2 — G(s)=1/[s(s+2)(s+5)]",
    t_max=25,
    nilai_K_banding=[1, K_kritis_manual]
)
fig2d.savefig("soal2d_dashboard.png", bbox_inches='tight')
plt.show()
print("→ Dashboard disimpan: soal2d_dashboard.png")

"""
PERTANYAAN ANALISIS 2d (jawab di sini):

  1. Berapa nilai K kritis hasil simulasi vs hasil Routh-Hurwitz?
     Routh-Hurwitz  : K_kritis = _______
     Simulasi       : K_kritis ≈ _______

  2. Mengapa sistem orde-3 dapat menjadi tidak stabil untuk K besar,
     sedangkan sistem orde-2 selalu stabil?
     Jawab: _______

  3. Apa trade-off antara memilih K kecil vs K mendekati K_kritis?
     Jawab: _______
"""


# ══════════════════════════════════════════════════════════════
#  SOAL 3 — DESAIN PENGUATAN K BERDASARKAN SPESIFIKASI  (25 poin)
# ══════════════════════════════════════════════════════════════
"""
LATAR BELAKANG:
  Sistem kendali kecepatan turbin angin memiliki G(s) = 1/[s(s+3)].
  Insinyur mensyaratkan:
    - % Overshoot ≤ 15%
    - Settling time ≤ 5 detik (kriteria 2%)
    - Error steady-state = 0 (sistem tipe 1)

TUJUAN:
  - Mencari K optimal yang memenuhi semua spesifikasi.
  - Menggunakan analisis pole-zero untuk desain.
"""

print("\n" + "=" * 60)
print("SOAL 3 — Desain K: G(s) = 1/[s(s+3)]")
print("=" * 60)

G3 = tf([1], [1, 3, 0])        # G(s) = 1/[s(s+3)]
cetak_info_sistem(G3, "Turbin Angin: G(s)=1/[s(s+3)]")


# ─────────────────────────────────────────────────────────────
# 3a. Tentukan daerah poles yang memenuhi spesifikasi  [7 poin]
# ─────────────────────────────────────────────────────────────
"""
ANALISIS SPESIFIKASI → DAERAH DI BIDANG-s:

  Spesifikasi % Overshoot ≤ 15%:
    ζ ≥ ???  (gunakan rumus: %OS = 100 × exp(-πζ/√(1-ζ²)))
    → sudut damping: θ = arccos(ζ) ≤ _____°

  Spesifikasi Settling time ≤ 5 s:
    Gunakan ts ≈ 4/(ζωn)
    → ζωn ≥ _____  → Re(poles) ≤ _____

  Gambarkan daerah yang memenuhi kedua spesifikasi pada root locus.
"""

# Hitung ζ minimum dari %OS ≤ 15%
OS_maks = 15.0   # %
zeta_min = ???   # ← isi rumus: -np.log(OS_maks/100) / np.sqrt(np.pi**2 + np.log(OS_maks/100)**2)

# Batasan settling time: σ_min = 4 / ts_maks
ts_maks = 5.0
sigma_min = ???  # ← isi rumus: 4 / ts_maks

print(f"\n  ζ minimum    : {zeta_min:.4f}")
print(f"  σ minimum    : {sigma_min:.4f}  (Re(poles) ≤ -{sigma_min:.4f})")


# ─────────────────────────────────────────────────────────────
# 3b. Plot root locus + overlay daerah spesifikasi  [8 poin]
# ─────────────────────────────────────────────────────────────

fig3b, ax3b = plt.subplots(figsize=(9, 7))

# Plot root locus
rlist, klist = control.root_locus(G3, plot=False)
for i in range(rlist.shape[1]):
    ax3b.plot(rlist[:, i].real, rlist[:, i].imag,
              color='#1f77b4', lw=2.2, alpha=0.85)
    ax3b.plot(rlist[:, i].real, -rlist[:, i].imag,
              color='#1f77b4', lw=2.2, alpha=0.85)

# Poles dan zeros
poles_G3 = control.poles(G3)
ax3b.plot(poles_G3.real, poles_G3.imag, 'x', color='red',
          ms=12, mew=2.5, label='Poles G(s)')

# ── Gambar DAERAH yang memenuhi spesifikasi ──
# Daerah: Re(s) ≤ -sigma_min  DAN  sudut dari origin ≤ arccos(zeta_min)
xlim_kiri = -8
x_range = np.linspace(xlim_kiri, 0, 300)
theta_min = np.arccos(zeta_min)  # sudut dalam radian

# Garis batas settling time (garis vertikal)
ax3b.axvline(-sigma_min, color='green', lw=2, ls='--',
             label=f'ts ≤ {ts_maks}s  (Re ≤ -{sigma_min:.2f})')

# Garis batas %OS (garis diagonal dari origin)
y_upper = np.tan(theta_min) * abs(x_range)   # bagian atas
y_lower = -y_upper                            # bagian bawah (simetri)

ax3b.plot(x_range, y_upper, color='orange', lw=2, ls='--',
          label=f'OS ≤ {OS_maks}%  (ζ ≥ {zeta_min:.2f})')
ax3b.plot(x_range, y_lower, color='orange', lw=2, ls='--')

# Arsiran daerah yang OK (Re ≤ -σ_min, di dalam sudut damping)
x_ok = x_range[x_range <= -sigma_min]
if len(x_ok) > 0:
    y_ok_upper = np.tan(theta_min) * abs(x_ok)
    ax3b.fill_between(x_ok, -y_ok_upper, y_ok_upper,
                      alpha=0.12, color='green', label='Daerah memenuhi specs')

ax3b.axhline(0, color='gray', lw=0.7, ls='--', alpha=0.5)
ax3b.axvline(0, color='red',  lw=1.2, ls='-.', alpha=0.4,
             label='Batas stabil')
ax3b.set_xlim(-8, 2)
ax3b.set_ylim(-6, 6)
ax3b.set_xlabel('Re(s)  σ', fontsize=11)
ax3b.set_ylabel('Im(s)  jω', fontsize=11)
ax3b.set_title('Root Locus + Daerah Spesifikasi\nG(s) = 1/[s(s+3)]',
               fontsize=12, fontweight='bold')
ax3b.legend(loc='upper right', fontsize=8.5)
ax3b.grid(True, alpha=0.3, ls=':')

fig3b.savefig("soal3b_root_locus_spesifikasi.png", bbox_inches='tight')
plt.show()
print("→ Gambar disimpan: soal3b_root_locus_spesifikasi.png")


# ─────────────────────────────────────────────────────────────
# 3c. Cari K optimal dengan scanning  [5 poin]
# ─────────────────────────────────────────────────────────────

K_coba  = np.linspace(0.1, 10, 500)
t_sim   = np.linspace(0, 25, 3000)

hasil_scan = []
for K in K_coba:
    cl = feedback(K * G3, 1)
    # Cek kestabilan terlebih dahulu
    poles_cl = control.poles(cl)
    if any(p.real >= 0 for p in poles_cl):
        continue
    t_out, y_out = step_response(cl, T=t_sim)
    par = hitung_parameter_respons(t_out, y_out)
    hasil_scan.append({
        'K': K,
        'OS': par['overshoot'],
        'ts': par['settling_time'],
        'ess': par['steady_state_error'],
    })

# Filter yang memenuhi semua spesifikasi
K_valid = [r for r in hasil_scan
           if r['OS'] <= OS_maks and r['ts'] <= ts_maks]

if K_valid:
    # Pilih K yang memberikan settling time terkecil
    K_optimal = min(K_valid, key=lambda r: r['ts'])
    print(f"\n  ✓ K optimal ditemukan: K = {K_optimal['K']:.3f}")
    print(f"    %OS    = {K_optimal['OS']:.2f}% (syarat ≤ {OS_maks}%)")
    print(f"    ts     = {K_optimal['ts']:.3f} s (syarat ≤ {ts_maks} s)")
    print(f"    ess    = {K_optimal['ess']:.4f}")
else:
    print("\n  ✗ Tidak ditemukan K yang memenuhi semua spesifikasi.")
    print("    Periksa kembali perhitungan zeta_min dan sigma_min.")
    K_optimal = {'K': 2.0}  # nilai default


# ─────────────────────────────────────────────────────────────
# 3d. Verifikasi K optimal — dashboard  [5 poin]
# ─────────────────────────────────────────────────────────────

fig3d = plot_dashboard_lengkap(
    G3,
    K_desain=round(K_optimal['K'], 3),
    nama_sistem="Soal 3 — Turbin Angin (K Optimal)",
    t_max=20,
    nilai_K_banding=[1.0, 5.0]
)
fig3d.savefig("soal3d_K_optimal.png", bbox_inches='tight')
plt.show()
print("→ Dashboard disimpan: soal3d_K_optimal.png")

"""
PERTANYAAN ANALISIS 3d (jawab di sini):

  1. Berapa nilai K optimal yang Anda temukan?
     K_optimal = _______

  2. Apakah ada konflik antara spesifikasi OS dan settling time?
     (Misal: K yang memperkecil OS justru memperbesar ts?)
     Jawab: _______

  3. Mengapa error steady-state sistem tipe-1 dengan input step = 0?
     Jawab: _______
"""


# ══════════════════════════════════════════════════════════════
#  SOAL 4 — PENGAYAAN: EFEK PENAMBAHAN POLE & ZERO  (25 poin)
# ══════════════════════════════════════════════════════════════
"""
LATAR BELAKANG:
  Dalam desain kompensator (lead/lag), kita menambahkan pole
  atau zero ke fungsi alih. Soal ini menyelidiki pengaruhnya
  terhadap bentuk root locus.

  Sistem dasar: G0(s) = K / [s(s+2)]

  Variasi yang akan dibandingkan:
    A. G0(s) = K / [s(s+2)]               — baseline
    B. G_A(s) = K(s+1) / [s(s+2)]         — tambah zero di s=-1
    C. G_B(s) = K(s+3) / [s(s+2)]         — tambah zero di s=-3
    D. G_C(s) = K / [s(s+2)(s+10)]        — tambah pole di s=-10 (jauh)
    E. G_D(s) = K / [s(s+2)(s+1)]         — tambah pole di s=-1 (dekat)
"""

print("\n" + "=" * 60)
print("SOAL 4 — Pengayaan: Efek Penambahan Pole & Zero")
print("=" * 60)


# ─────────────────────────────────────────────────────────────
# 4a. Definisikan semua varian fungsi alih  [5 poin]
# ─────────────────────────────────────────────────────────────

G0_base = tf([1],    [1, 2, 0])          # baseline
G_A     = tf([???, ???], [???, ???, ???]) # ← zero di s=-1: num=[1,1]
G_B     = tf([???, ???], [???, ???, ???]) # ← zero di s=-3: num=[1,3]
G_C     = tf([1],    [???, ???, ???, ???])# ← pole di s=-10: den=s(s+2)(s+10)
G_D     = tf([1],    [???, ???, ???, ???])# ← pole di s=-1:  den=s(s+2)(s+1)

varian = {
    'A — Baseline G0': G0_base,
    'B — Zero s=-1':   G_A,
    'C — Zero s=-3':   G_B,
    'D — Pole s=-10':  G_C,
    'E — Pole s=-1':   G_D,
}


# ─────────────────────────────────────────────────────────────
# 4b. Plot root locus semua varian dalam satu figure  [10 poin]
# ─────────────────────────────────────────────────────────────

fig4b, axes4b = plt.subplots(2, 3, figsize=(16, 10))
fig4b.suptitle('Efek Penambahan Pole/Zero pada Root Locus',
               fontsize=13, fontweight='bold')
axes_flat = axes4b.flatten()

colors_rl = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

for idx, (label, G_var) in enumerate(varian.items()):
    ax = axes_flat[idx]
    try:
        rlist, _ = control.root_locus(G_var, plot=False)
        for i in range(rlist.shape[1]):
            ax.plot(rlist[:, i].real, rlist[:, i].imag,
                    color=colors_rl[idx], lw=2)
            ax.plot(rlist[:, i].real, -rlist[:, i].imag,
                    color=colors_rl[idx], lw=2)
        poles_v = control.poles(G_var)
        zeros_v = control.zeros(G_var)
        ax.plot(poles_v.real, poles_v.imag, 'x', color='red',
                ms=11, mew=2.5, label='Poles')
        if len(zeros_v) > 0:
            ax.plot(zeros_v.real, zeros_v.imag, 'o', color='green',
                    ms=9, mew=2.5, mfc='none', label='Zeros')
    except Exception as e:
        ax.text(0.5, 0.5, f'Error:\n{e}', ha='center', va='center',
                transform=ax.transAxes, fontsize=8)
    ax.axvline(0, color='red', lw=1, ls='-.', alpha=0.4)
    ax.axhline(0, color='gray', lw=0.6, ls='--', alpha=0.4)
    ax.set_title(label, fontsize=9, fontweight='bold')
    ax.set_xlabel('Re(s)', fontsize=8)
    ax.set_ylabel('Im(s)', fontsize=8)
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3, ls=':')
    ax.set_xlim(-12, 2)

# Sembunyikan subplot ke-6 (tidak terpakai)
axes_flat[5].axis('off')

plt.tight_layout()
fig4b.savefig("soal4b_perbandingan_pole_zero.png", bbox_inches='tight')
plt.show()
print("→ Gambar disimpan: soal4b_perbandingan_pole_zero.png")


# ─────────────────────────────────────────────────────────────
# 4c. Perbandingan respons step semua varian  [5 poin]
#     Gunakan K = 2 untuk semua varian
# ─────────────────────────────────────────────────────────────

K_banding = 2.0
t_sim4 = np.linspace(0, 20, 2000)
fig4c, ax4c = plt.subplots(figsize=(11, 5))

for idx, (label, G_var) in enumerate(varian.items()):
    try:
        cl_v = feedback(K_banding * G_var, 1)
        poles_cl_v = control.poles(cl_v)
        if any(p.real >= 0 for p in poles_cl_v):
            print(f"  ✗ {label}: TIDAK STABIL untuk K={K_banding}")
            continue
        t_out, y_out = step_response(cl_v, T=t_sim4)
        lw = 2.8 if idx == 0 else 1.8
        ax4c.plot(t_out, y_out, color=colors_rl[idx],
                  lw=lw, label=label)
    except Exception as e:
        print(f"  ✗ {label}: {e}")

ax4c.axhline(1, color='gray', lw=1.2, ls='--', alpha=0.7, label='r(t)=1')
ax4c.axhline(1.02, color='red', lw=0.7, ls=':', alpha=0.5)
ax4c.axhline(0.98, color='red', lw=0.7, ls=':', alpha=0.5)
ax4c.set_xlabel('Waktu (s)', fontsize=11)
ax4c.set_ylabel('y(t)', fontsize=11)
ax4c.set_title(f'Perbandingan Respons Step (K = {K_banding})',
               fontsize=12, fontweight='bold')
ax4c.legend(loc='upper right', fontsize=8.5)
ax4c.grid(True, alpha=0.3, ls=':')
ax4c.set_xlim(0, 20)

fig4c.savefig("soal4c_respons_step_perbandingan.png", bbox_inches='tight')
plt.show()
print("→ Gambar disimpan: soal4c_respons_step_perbandingan.png")

"""
PERTANYAAN ANALISIS 4 (jawab di sini):

  1. Apa efek penambahan zero pada bagian kiri sumbu (s=-1 vs s=-3)
     terhadap bentuk root locus?
     Jawab: _______

  2. Bandingkan penambahan pole jauh (s=-10) vs pole dekat (s=-1).
     Mana yang lebih mendekati sistem asli? Mengapa?
     Jawab: _______

  3. Dalam desain kompensator, mengapa zero lead-compensator
     biasanya ditempatkan lebih dekat ke origin daripada pole-nya?
     Jawab: _______

  4. Rangkum aturan-aturan utama konstruksi root locus yang
     Anda gunakan dalam tugas ini (minimal 5 aturan):
     a. _______
     b. _______
     c. _______
     d. _______
     e. _______
"""


# ══════════════════════════════════════════════════════════════
#  PENUTUP — Laporan Singkat
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("  TUGAS SELESAI")
print("  Pastikan semua gambar berikut telah tersimpan:")
gambar_wajib = [
    "soal1c_root_locus.png",
    "soal1d_respons_step.png",
    "soal2c_verifikasi_K_kritis.png",
    "soal2d_dashboard.png",
    "soal3b_root_locus_spesifikasi.png",
    "soal3d_K_optimal.png",
    "soal4b_perbandingan_pole_zero.png",
    "soal4c_respons_step_perbandingan.png",
]
for f in gambar_wajib:
    import os
    status = "✓" if os.path.exists(f) else "✗ BELUM ADA"
    print(f"    {status}  {f}")
print("=" * 60)

"""
KESIMPULAN MAHASISWA (tulis di sini, minimal 100 kata):

  _________________________________________________________________
  _________________________________________________________________
  _________________________________________________________________
  _________________________________________________________________
  _________________________________________________________________
"""
