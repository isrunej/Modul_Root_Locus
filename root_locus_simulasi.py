"""
==============================================================
MODUL SIMULASI TEMPAT KEDUDUKAN AKAR (ROOT LOCUS)
Sistem Kontrol - Teknik Elektro
==============================================================
Deskripsi:
    Modul ini menyediakan fungsi-fungsi simulasi lengkap untuk
    analisis Tempat Kedudukan Akar (Root Locus) beserta respons
    sistem loop-tertutup.

Prasyarat:
    pip install control matplotlib numpy scipy

Cara Pakai:
    python root_locus_simulasi.py
    atau impor fungsi secara individual:
    from root_locus_simulasi import plot_root_locus, analisis_sistem
==============================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import control
from control import tf, feedback, step_response, bode_plot
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────
# KONFIGURASI TAMPILAN
# ─────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'figure.dpi': 100,
})

WARNA_PRIMER  = '#1f77b4'
WARNA_SEKUNDER = '#ff7f0e'
WARNA_AKSEN   = '#2ca02c'
WARNA_BAHAYA  = '#d62728'


# ─────────────────────────────────────────────────────────────
# BAGIAN 1: FUNGSI UTILITAS DASAR
# ─────────────────────────────────────────────────────────────

def cetak_info_sistem(sys_tf, nama="Sistem"):
    """Cetak informasi lengkap sebuah fungsi alih."""
    print(f"\n{'='*55}")
    print(f"  INFO SISTEM: {nama}")
    print(f"{'='*55}")
    poles = control.poles(sys_tf)
    zeros = control.zeros(sys_tf)
    print(f"  Fungsi Alih G(s):")
    print(f"  {sys_tf}")
    print(f"\n  Poles (akar penyebut): {np.round(poles, 4)}")
    print(f"  Zeros (akar pembilang): {np.round(zeros, 4) if len(zeros) > 0 else 'Tidak ada'}")
    print(f"  Orde sistem           : {len(poles)}")
    print(f"  Jumlah asimtot        : {len(poles) - len(zeros)}")
    if len(poles) > len(zeros):
        sudut_asimtot = [(2*k+1)*180 / (len(poles)-len(zeros))
                         for k in range(len(poles)-len(zeros))]
        centroid = (sum(poles.real) - sum(zeros.real)) / (len(poles)-len(zeros))
        print(f"  Sudut asimtot (°)     : {[round(s, 1) for s in sudut_asimtot]}")
        print(f"  Centroid asimtot      : {round(centroid.real, 4)}")
    print(f"{'='*55}\n")


def hitung_parameter_respons(t, y, nama=""):
    """
    Hitung parameter respons transien dari data time-domain.

    Returns dict berisi: rise_time, settling_time, overshoot,
    steady_state_error, peak_time, peak_value
    """
    y_ss = y[-1]                     # nilai steady-state
    y_final_ref = 1.0                # referensi input step = 1

    # Rise time: 10% → 90% dari nilai akhir
    idx_10 = np.where(y >= 0.1 * y_ss)[0]
    idx_90 = np.where(y >= 0.9 * y_ss)[0]
    rise_time = (t[idx_90[0]] - t[idx_10[0]]) if (len(idx_10) > 0 and len(idx_90) > 0) else None

    # Peak time & overshoot
    idx_peak = np.argmax(y)
    peak_value = y[idx_peak]
    peak_time = t[idx_peak]
    overshoot = max(0, (peak_value - y_ss) / y_ss * 100) if y_ss != 0 else 0

    # Settling time (±2%)
    batas_atas = y_ss * 1.02
    batas_bawah = y_ss * 0.98
    dalam_band = np.where((y <= batas_atas) & (y >= batas_bawah))[0]
    if len(dalam_band) > 0:
        # Cari indeks terakhir di luar band, settling time = setelah itu
        luar_band = np.where((y > batas_atas) | (y < batas_bawah))[0]
        settling_time = t[luar_band[-1]] if len(luar_band) > 0 else t[0]
    else:
        settling_time = t[-1]

    ess = abs(y_final_ref - y_ss)

    hasil = {
        'rise_time': round(rise_time, 4) if rise_time else None,
        'peak_time': round(peak_time, 4),
        'peak_value': round(peak_value, 4),
        'settling_time': round(settling_time, 4),
        'overshoot': round(overshoot, 2),
        'steady_state': round(y_ss, 4),
        'steady_state_error': round(ess, 4),
    }

    if nama:
        print(f"\n  Parameter Respons Transien [{nama}]:")
        print(f"    Rise time (0→90%)  : {hasil['rise_time']} s")
        print(f"    Peak time          : {hasil['peak_time']} s")
        print(f"    Nilai puncak       : {hasil['peak_value']}")
        print(f"    % Overshoot        : {hasil['overshoot']} %")
        print(f"    Settling time (2%) : {hasil['settling_time']} s")
        print(f"    Nilai steady-state : {hasil['steady_state']}")
        print(f"    Error steady-state : {hasil['steady_state_error']}")

    return hasil


# ─────────────────────────────────────────────────────────────
# BAGIAN 2: FUNGSI PLOT UTAMA
# ─────────────────────────────────────────────────────────────

def plot_root_locus(sys_tf, K_range=None, judul="Tempat Kedudukan Akar",
                   tampilkan_grid=True, K_tandai=None):
    """
    Plot Root Locus lengkap dengan anotasi poles, zeros, dan asimtot.

    Parameters
    ----------
    sys_tf   : control.TransferFunction — fungsi alih loop-terbuka G(s)
    K_range  : tuple (K_min, K_max) — rentang penguatan (opsional)
    judul    : str — judul grafik
    tampilkan_grid : bool — tampilkan grid
    K_tandai : list of float — nilai K yang ditandai di plot
    """
    fig, ax = plt.subplots(figsize=(9, 7))

    # Gambar root locus menggunakan library control
    rlist, klist = control.root_locus(sys_tf, plot=False)

    # Plot jalur
    for i in range(rlist.shape[1]):
        ax.plot(rlist[:, i].real, rlist[:, i].imag,
                color=WARNA_PRIMER, linewidth=2, alpha=0.8)
        ax.plot(rlist[:, i].real, -rlist[:, i].imag,
                color=WARNA_PRIMER, linewidth=2, alpha=0.8)

    # Poles (×) dan Zeros (○)
    poles = control.poles(sys_tf)
    zeros = control.zeros(sys_tf)
    ax.plot(poles.real, poles.imag, 'x', color=WARNA_BAHAYA,
            markersize=12, markeredgewidth=2.5, label='Poles G(s)', zorder=5)
    if len(zeros) > 0:
        ax.plot(zeros.real, zeros.imag, 'o', color=WARNA_AKSEN,
                markersize=10, markerfacecolor='none',
                markeredgewidth=2.5, label='Zeros G(s)', zorder=5)

    # Anotasi nilai poles dan zeros
    for p in poles:
        ax.annotate(f'  {p:.2f}', xy=(p.real, p.imag),
                    fontsize=8, color=WARNA_BAHAYA, va='center')
    for z in zeros:
        ax.annotate(f'  {z:.2f}', xy=(z.real, z.imag),
                    fontsize=8, color=WARNA_AKSEN, va='center')

    # Tandai K tertentu
    if K_tandai:
        for K_val in K_tandai:
            cl_sys = feedback(K_val * sys_tf, 1)
            cl_poles = control.poles(cl_sys)
            ax.plot(cl_poles.real, cl_poles.imag, 's',
                    color=WARNA_SEKUNDER, markersize=9,
                    label=f'K = {K_val}', zorder=6)
            for cp in cl_poles:
                ax.annotate(f' K={K_val}\n ({cp.real:.2f},{cp.imag:.2f}j)',
                            xy=(cp.real, cp.imag), fontsize=7.5,
                            color=WARNA_SEKUNDER)

    # Garis sumbu
    ax.axhline(0, color='gray', linewidth=0.8, linestyle='--', alpha=0.6)
    ax.axvline(0, color='gray', linewidth=0.8, linestyle='--', alpha=0.6)

    # Sumbu imajiner = garis kestabilan
    ax.axvline(0, color=WARNA_BAHAYA, linewidth=1.5, linestyle='-.',
               alpha=0.4, label='Batas Kestabilan (jω-axis)')

    ax.set_xlabel('Bagian Real  σ', fontsize=11)
    ax.set_ylabel('Bagian Imajiner  jω', fontsize=11)
    ax.set_title(judul, fontsize=13, fontweight='bold', pad=12)
    ax.legend(loc='upper right', fontsize=8, framealpha=0.9)
    if tampilkan_grid:
        ax.grid(True, alpha=0.35, linestyle=':')
    ax.set_aspect('equal', adjustable='datalim')

    plt.tight_layout()
    return fig, ax


def plot_respons_step_variasi_K(sys_tf, nilai_K, t_max=20,
                                judul="Respons Step — Variasi Penguatan K"):
    """
    Plot respons step loop-tertutup untuk beberapa nilai K sekaligus.

    Parameters
    ----------
    sys_tf  : TransferFunction — G(s) loop-terbuka
    nilai_K : list of float — daftar nilai K yang dibandingkan
    t_max   : float — durasi simulasi (detik)
    """
    t = np.linspace(0, t_max, 2000)
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = plt.cm.viridis(np.linspace(0.15, 0.85, len(nilai_K)))

    for K, warna in zip(nilai_K, colors):
        cl = feedback(K * sys_tf, 1)
        t_out, y_out = step_response(cl, T=t)
        ax.plot(t_out, y_out, color=warna, linewidth=2, label=f'K = {K}')

    ax.axhline(1, color='gray', linewidth=1.2, linestyle='--',
               alpha=0.7, label='Referensi (r=1)')
    ax.axhline(1.02, color='red', linewidth=0.8, linestyle=':', alpha=0.5)
    ax.axhline(0.98, color='red', linewidth=0.8, linestyle=':', alpha=0.5,
               label='Band ±2%')

    ax.set_xlabel('Waktu (s)', fontsize=11)
    ax.set_ylabel('Amplitudo y(t)', fontsize=11)
    ax.set_title(judul, fontsize=13, fontweight='bold', pad=10)
    ax.legend(loc='upper right', fontsize=8.5, framealpha=0.9)
    ax.grid(True, alpha=0.35, linestyle=':')
    ax.set_xlim(0, t_max)
    ax.set_ylim(-0.1, max(1.5, ax.get_ylim()[1]))

    plt.tight_layout()
    return fig, ax


def plot_dashboard_lengkap(sys_tf, K_desain, nama_sistem="Sistem",
                           t_max=20, nilai_K_banding=None):
    """
    Dashboard 4-panel: Root Locus + Respons Step + Diagram Bode + Tabel Parameter.

    Parameters
    ----------
    sys_tf      : TransferFunction — G(s) loop-terbuka
    K_desain    : float — nilai K yang dipilih untuk desain
    nama_sistem : str — label sistem
    t_max       : float — durasi simulasi (s)
    nilai_K_banding : list — nilai K tambahan untuk perbandingan
    """
    if nilai_K_banding is None:
        nilai_K_banding = []

    fig = plt.figure(figsize=(15, 10))
    fig.suptitle(f'Analisis Lengkap: {nama_sistem}', fontsize=14,
                 fontweight='bold', y=0.98)
    gs = gridspec.GridSpec(2, 3, figure=fig,
                           hspace=0.42, wspace=0.38)

    ax_rl   = fig.add_subplot(gs[0, 0])   # Root Locus
    ax_step = fig.add_subplot(gs[0, 1:])  # Respons Step
    ax_mag  = fig.add_subplot(gs[1, 0])   # Bode — Magnitudo
    ax_phase = fig.add_subplot(gs[1, 1])  # Bode — Fase
    ax_tabel = fig.add_subplot(gs[1, 2])  # Tabel parameter

    # ── Panel 1: Root Locus ──────────────────────────────────
    rlist, _ = control.root_locus(sys_tf, plot=False)
    for i in range(rlist.shape[1]):
        ax_rl.plot(rlist[:, i].real, rlist[:, i].imag,
                   color=WARNA_PRIMER, lw=1.8, alpha=0.8)
        ax_rl.plot(rlist[:, i].real, -rlist[:, i].imag,
                   color=WARNA_PRIMER, lw=1.8, alpha=0.8)
    poles = control.poles(sys_tf)
    zeros = control.zeros(sys_tf)
    ax_rl.plot(poles.real, poles.imag, 'x', color=WARNA_BAHAYA,
               ms=11, mew=2.5, label='Poles', zorder=5)
    if len(zeros) > 0:
        ax_rl.plot(zeros.real, zeros.imag, 'o', color=WARNA_AKSEN,
                   ms=9, mew=2.5, mfc='none', label='Zeros', zorder=5)
    cl_K = feedback(K_desain * sys_tf, 1)
    cl_poles_K = control.poles(cl_K)
    ax_rl.plot(cl_poles_K.real, cl_poles_K.imag, 's',
               color=WARNA_SEKUNDER, ms=9, label=f'K={K_desain}', zorder=6)
    ax_rl.axvline(0, color='red', lw=1, ls='-.', alpha=0.4)
    ax_rl.axhline(0, color='gray', lw=0.7, ls='--', alpha=0.5)
    ax_rl.set_title('Root Locus', fontsize=11, fontweight='bold')
    ax_rl.set_xlabel('Re(s)', fontsize=9)
    ax_rl.set_ylabel('Im(s)', fontsize=9)
    ax_rl.legend(fontsize=7.5)
    ax_rl.grid(True, alpha=0.3, ls=':')

    # ── Panel 2: Respons Step ────────────────────────────────
    t = np.linspace(0, t_max, 2000)
    semua_K = [K_desain] + (nilai_K_banding or [])
    colors = plt.cm.tab10(np.linspace(0, 0.6, len(semua_K)))
    for K_val, warna in zip(semua_K, colors):
        cl = feedback(K_val * sys_tf, 1)
        t_out, y_out = step_response(cl, T=t)
        lw = 2.5 if K_val == K_desain else 1.5
        ls = '-' if K_val == K_desain else '--'
        ax_step.plot(t_out, y_out, color=warna, lw=lw, ls=ls,
                     label=f'K = {K_val}' + (' ← desain' if K_val == K_desain else ''))
    ax_step.axhline(1, color='gray', lw=1.2, ls='--', alpha=0.7, label='r(t)=1')
    ax_step.axhline(1.02, color='red', lw=0.8, ls=':', alpha=0.4)
    ax_step.axhline(0.98, color='red', lw=0.8, ls=':', alpha=0.4, label='±2%')
    ax_step.set_title('Respons Step Loop-Tertutup', fontsize=11, fontweight='bold')
    ax_step.set_xlabel('Waktu (s)', fontsize=9)
    ax_step.set_ylabel('y(t)', fontsize=9)
    ax_step.legend(fontsize=8, loc='upper right')
    ax_step.grid(True, alpha=0.3, ls=':')
    ax_step.set_xlim(0, t_max)

    # ── Panel 3 & 4: Diagram Bode ────────────────────────────
    cl_desain = feedback(K_desain * sys_tf, 1)
    try:
        omega = np.logspace(-2, 2, 500)
        mag, phase, om = control.bode(K_desain * sys_tf, omega,
                                      plot=False, dB=True)
        ax_mag.semilogx(om, 20*np.log10(mag + 1e-12),
                        color=WARNA_PRIMER, lw=2)
        ax_mag.axhline(0, color='gray', lw=0.8, ls='--', alpha=0.6)
        ax_mag.set_title('Bode — Magnitudo', fontsize=11, fontweight='bold')
        ax_mag.set_xlabel('ω (rad/s)', fontsize=9)
        ax_mag.set_ylabel('|G(jω)| (dB)', fontsize=9)
        ax_mag.grid(True, which='both', alpha=0.3, ls=':')

        ax_phase.semilogx(om, np.degrees(phase),
                          color=WARNA_SEKUNDER, lw=2)
        ax_phase.axhline(-180, color='red', lw=0.8, ls='--', alpha=0.6,
                          label='-180°')
        ax_phase.set_title('Bode — Fase', fontsize=11, fontweight='bold')
        ax_phase.set_xlabel('ω (rad/s)', fontsize=9)
        ax_phase.set_ylabel('∠G(jω) (°)', fontsize=9)
        ax_phase.legend(fontsize=8)
        ax_phase.grid(True, which='both', alpha=0.3, ls=':')
    except Exception:
        ax_mag.text(0.5, 0.5, 'Bode tidak tersedia',
                    ha='center', va='center', transform=ax_mag.transAxes)
        ax_phase.text(0.5, 0.5, 'Bode tidak tersedia',
                      ha='center', va='center', transform=ax_phase.transAxes)

    # ── Panel 5: Tabel Parameter Transien ────────────────────
    ax_tabel.axis('off')
    t_out, y_out = step_response(cl_desain, T=t)
    par = hitung_parameter_respons(t_out, y_out)

    # Hitung gain margin & phase margin
    try:
        gm, pm, wg, wp = control.margin(K_desain * sys_tf)
        gm_db = round(20 * np.log10(gm), 2) if gm and gm > 0 else '∞'
        pm_deg = round(pm, 2) if pm else None
    except Exception:
        gm_db, pm_deg = '—', '—'

    baris = [
        ['Parameter', 'Nilai', 'Satuan'],
        ['K desain', str(K_desain), '—'],
        ['Rise time', str(par['rise_time']), 's'],
        ['Peak time', str(par['peak_time']), 's'],
        ['% Overshoot', str(par['overshoot']), '%'],
        ['Settling time', str(par['settling_time']), 's'],
        ['Steady-state', str(par['steady_state']), '—'],
        ['Error SS', str(par['steady_state_error']), '—'],
        ['Gain Margin', str(gm_db), 'dB'],
        ['Phase Margin', str(pm_deg), '°'],
    ]
    tabel = ax_tabel.table(cellText=baris[1:], colLabels=baris[0],
                            loc='center', cellLoc='center')
    tabel.auto_set_font_size(False)
    tabel.set_fontsize(9)
    tabel.scale(1.1, 1.5)
    # Warna header
    for j in range(3):
        tabel[(0, j)].set_facecolor('#2c3e50')
        tabel[(0, j)].set_text_props(color='white', fontweight='bold')
    ax_tabel.set_title('Ringkasan Parameter\n(K Desain)',
                        fontsize=11, fontweight='bold')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    return fig


# ─────────────────────────────────────────────────────────────
# BAGIAN 3: DEMO — CONTOH SISTEM
# ─────────────────────────────────────────────────────────────

def demo_sistem_orde2():
    """Demo 1 — Sistem orde-2 standar tanpa zero."""
    print("\n" + "="*55)
    print("  DEMO 1: Sistem Orde-2 Tanpa Zero")
    print("  G(s) = 1 / (s(s+2))")
    print("="*55)

    G = tf([1], [1, 2, 0])          # G(s) = 1 / [s(s+2)]
    cetak_info_sistem(G, "G(s) = 1/[s(s+2)]")

    fig1, _ = plot_root_locus(
        G,
        judul="Root Locus — G(s) = 1/[s(s+2)]",
        K_tandai=[1, 2, 5]
    )
    fig1.savefig("demo1_root_locus.png", bbox_inches='tight')
    print("  → Grafik disimpan: demo1_root_locus.png")

    fig2, _ = plot_respons_step_variasi_K(
        G,
        nilai_K=[0.5, 1, 2, 5, 10],
        t_max=15,
        judul="Respons Step — G(s) = 1/[s(s+2)]"
    )
    fig2.savefig("demo1_respons_step.png", bbox_inches='tight')
    print("  → Grafik disimpan: demo1_respons_step.png")

    # Hitung parameter untuk K = 1
    cl = feedback(1 * G, 1)
    t = np.linspace(0, 15, 2000)
    t_out, y_out = step_response(cl, T=t)
    hitung_parameter_respons(t_out, y_out, nama="K=1, G(s)=1/[s(s+2)]")

    plt.show()


def demo_sistem_orde3():
    """Demo 2 — Sistem orde-3 (lebih kompleks, bisa tidak stabil)."""
    print("\n" + "="*55)
    print("  DEMO 2: Sistem Orde-3")
    print("  G(s) = 1 / (s(s+1)(s+3))")
    print("="*55)

    G = tf([1], [1, 4, 3, 0])       # G(s) = 1 / [s(s+1)(s+3)]
    cetak_info_sistem(G, "G(s) = 1/[s(s+1)(s+3)]")

    fig = plot_dashboard_lengkap(
        G,
        K_desain=3,
        nama_sistem="G(s) = 1/[s(s+1)(s+3)]",
        t_max=25,
        nilai_K_banding=[1, 12]
    )
    fig.savefig("demo2_dashboard.png", bbox_inches='tight')
    print("  → Dashboard disimpan: demo2_dashboard.png")
    plt.show()


def demo_sistem_dengan_zero():
    """Demo 3 — Sistem dengan zero (efek penambahan zero pada root locus)."""
    print("\n" + "="*55)
    print("  DEMO 3: Perbandingan Sistem Dengan dan Tanpa Zero")
    print("  G1(s) = 1 / (s(s+4)(s+5))")
    print("  G2(s) = (s+2) / (s(s+4)(s+5))  ← ada zero di s=-2")
    print("="*55)

    G1 = tf([1],    [1, 9, 20, 0])    # tanpa zero
    G2 = tf([1, 2], [1, 9, 20, 0])   # dengan zero di s=-2

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Efek Penambahan Zero pada Root Locus',
                 fontsize=13, fontweight='bold')

    for ax, G, judul in zip(axes,
                             [G1, G2],
                             ['Tanpa Zero\nG(s)=1/[s(s+4)(s+5)]',
                              'Dengan Zero di s=-2\nG(s)=(s+2)/[s(s+4)(s+5)]']):
        rlist, _ = control.root_locus(G, plot=False)
        for i in range(rlist.shape[1]):
            ax.plot(rlist[:, i].real, rlist[:, i].imag,
                    color=WARNA_PRIMER, lw=2, alpha=0.8)
            ax.plot(rlist[:, i].real, -rlist[:, i].imag,
                    color=WARNA_PRIMER, lw=2, alpha=0.8)
        poles = control.poles(G)
        zeros = control.zeros(G)
        ax.plot(poles.real, poles.imag, 'x', color=WARNA_BAHAYA,
                ms=12, mew=2.5, label='Poles')
        if len(zeros) > 0:
            ax.plot(zeros.real, zeros.imag, 'o', color=WARNA_AKSEN,
                    ms=10, mew=2.5, mfc='none', label='Zeros')
        ax.axvline(0, color='red', lw=1.2, ls='-.', alpha=0.5,
                   label='Batas Stabil')
        ax.axhline(0, color='gray', lw=0.7, ls='--', alpha=0.4)
        ax.set_title(judul, fontsize=10, fontweight='bold')
        ax.set_xlabel('Re(s)', fontsize=9)
        ax.set_ylabel('Im(s)', fontsize=9)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3, ls=':')

    plt.tight_layout()
    fig.savefig("demo3_efek_zero.png", bbox_inches='tight')
    print("  → Grafik disimpan: demo3_efek_zero.png")
    plt.show()


def demo_pencarian_K_kritis():
    """
    Demo 4 — Mencari K kritis (batas kestabilan) secara otomatis
    menggunakan kriteria Routh-Hurwitz lewat library control.
    """
    print("\n" + "="*55)
    print("  DEMO 4: Pencarian K Kritis (Batas Kestabilan)")
    print("  G(s) = 1 / (s(s+1)(s+3))")
    print("="*55)

    G = tf([1], [1, 4, 3, 0])
    K_list = np.linspace(0.01, 20, 500)
    poles_max_real = []

    for K in K_list:
        cl = feedback(K * G, 1)
        poles_cl = control.poles(cl)
        poles_max_real.append(max(poles_cl.real))

    poles_max_real = np.array(poles_max_real)

    # K kritis = saat poles_max_real menyeberang nol
    idx_kritis = np.where(np.diff(np.sign(poles_max_real)))[0]
    K_kritis = K_list[idx_kritis[0]] if len(idx_kritis) > 0 else None

    print(f"\n  Hasil pencarian K kritis:")
    print(f"    K kritis ≈ {K_kritis:.3f}" if K_kritis else "    Tidak ditemukan")
    print(f"    (Sistem tidak stabil untuk K > {K_kritis:.3f})" if K_kritis else "")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle('Analisis Kestabilan: Pencarian K Kritis',
                 fontsize=13, fontweight='bold')

    # Plot root locus
    rlist, _ = control.root_locus(G, plot=False)
    for i in range(rlist.shape[1]):
        ax1.plot(rlist[:, i].real, rlist[:, i].imag,
                 color=WARNA_PRIMER, lw=2)
        ax1.plot(rlist[:, i].real, -rlist[:, i].imag,
                 color=WARNA_PRIMER, lw=2)
    poles = control.poles(G)
    ax1.plot(poles.real, poles.imag, 'x', color=WARNA_BAHAYA,
             ms=12, mew=2.5, label='Poles OL')
    if K_kritis:
        cl_kritis = feedback(K_kritis * G, 1)
        cp_kritis = control.poles(cl_kritis)
        ax1.plot(cp_kritis.real, cp_kritis.imag, 's',
                 color='purple', ms=10,
                 label=f'K_kritis={K_kritis:.2f}', zorder=6)
    ax1.axvline(0, color='red', lw=1.5, ls='-.', alpha=0.5)
    ax1.axhline(0, color='gray', lw=0.7, ls='--', alpha=0.4)
    ax1.set_title('Root Locus & Titik Kritis', fontsize=11, fontweight='bold')
    ax1.set_xlabel('Re(s)', fontsize=9)
    ax1.set_ylabel('Im(s)', fontsize=9)
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3, ls=':')

    # Plot poles max real vs K
    ax2.plot(K_list, poles_max_real, color=WARNA_PRIMER, lw=2)
    ax2.axhline(0, color='red', lw=1.5, ls='--', alpha=0.8,
                label='Re(s)=0 (batas stabil)')
    if K_kritis:
        ax2.axvline(K_kritis, color='purple', lw=1.5, ls='-.',
                    label=f'K_kritis≈{K_kritis:.2f}')
    ax2.fill_between(K_list, poles_max_real, 0,
                     where=(poles_max_real > 0),
                     alpha=0.15, color='red', label='Tidak stabil')
    ax2.fill_between(K_list, poles_max_real, 0,
                     where=(poles_max_real <= 0),
                     alpha=0.15, color='green', label='Stabil')
    ax2.set_title('Bagian Real Maks. Poles vs K', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Penguatan K', fontsize=9)
    ax2.set_ylabel('max[Re(poles CL)]', fontsize=9)
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3, ls=':')

    plt.tight_layout()
    fig.savefig("demo4_K_kritis.png", bbox_inches='tight')
    print("  → Grafik disimpan: demo4_K_kritis.png")
    plt.show()

    return K_kritis


# ─────────────────────────────────────────────────────────────
# BAGIAN 4: FUNGSI BANTU UNTUK TUGAS MAHASISWA
# ─────────────────────────────────────────────────────────────

def analisis_sistem(num, den, K_desain, nama="Sistem", t_max=20):
    """
    Fungsi all-in-one untuk mahasiswa: masukkan num/den dan K,
    dapatkan root locus + respons step + parameter transien.

    Parameters
    ----------
    num      : list — koefisien pembilang G(s)
    den      : list — koefisien penyebut G(s)
    K_desain : float — penguatan yang dipilih
    nama     : str — nama sistem
    t_max    : float — durasi simulasi

    Contoh penggunaan:
        analisis_sistem([1], [1, 3, 2, 0], K_desain=5, nama="Tugas 1")
    """
    G = tf(num, den)
    cetak_info_sistem(G, nama)

    fig = plot_dashboard_lengkap(G, K_desain, nama_sistem=nama,
                                  t_max=t_max)

    cl = feedback(K_desain * G, 1)
    t = np.linspace(0, t_max, 2000)
    t_out, y_out = step_response(cl, T=t)
    par = hitung_parameter_respons(t_out, y_out, nama=f"{nama} (K={K_desain})")

    safe_name = nama.replace(' ', '_').replace('/', '-')
    fname = f"hasil_{safe_name}.png"
    fig.savefig(fname, bbox_inches='tight')
    print(f"\n  → Dashboard disimpan: {fname}")
    plt.show()

    return G, fig, par


# ─────────────────────────────────────────────────────────────
# MAIN — Jalankan semua demo
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════╗
║   MODUL SIMULASI TEMPAT KEDUDUKAN AKAR (ROOT LOCUS) ║
║   Sistem Kontrol — Teknik Elektro                   ║
╚══════════════════════════════════════════════════════╝

Menjalankan 4 demo simulasi...
    """)

    # Pilih demo yang ingin dijalankan (komentari yang tidak diperlukan)
    demo_sistem_orde2()
    demo_sistem_orde3()
    demo_sistem_dengan_zero()
    demo_pencarian_K_kritis()

    print("\n✓ Semua demo selesai. Grafik tersimpan di direktori kerja.")
