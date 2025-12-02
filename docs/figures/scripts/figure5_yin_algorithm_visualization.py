#!/usr/bin/env python3
"""
Figure 5: YIN Algorithm Visualization
Four-panel visualization showing YIN pitch detection processing stages
Mambo Whistle Technical Report

Author: Mambo Whistle Team
Date: 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================================
#  CONFIGURATION
# ============================================================================

# Use Times New Roman font
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['axes.unicode_minus'] = False

# Google brand colors
GOOGLE_BLUE = np.array([66, 133, 244]) / 255
GOOGLE_RED = np.array([234, 67, 53]) / 255
GOOGLE_YELLOW = np.array([251, 188, 5]) / 255
GOOGLE_GREEN = np.array([52, 168, 83]) / 255
GOOGLE_GRAY = np.array([95, 99, 104]) / 255

# ============================================================================
#  GENERATE SYNTHETIC VOCAL SIGNAL (F0 = 220 Hz, A3)
# ============================================================================

fs = 44100                  # Sample rate
N = 1024                    # Window size (same as our system)
f0_true = 220               # True fundamental frequency (A3)
t = np.arange(N) / fs       # Time vector

# Generate harmonic-rich signal simulating human voice
# Fundamental + harmonics with decreasing amplitude + slight noise
np.random.seed(42)  # For reproducibility
signal = np.zeros(N)
num_harmonics = 8

for h in range(1, num_harmonics + 1):
    amplitude = 1 / (h ** 0.8)  # Harmonic roll-off
    phase = np.random.rand() * 2 * np.pi  # Random phase
    signal += amplitude * np.sin(2 * np.pi * f0_true * h * t + phase)

# Add slight noise (simulating breath/microphone noise)
signal += 0.02 * np.random.randn(N)

# Normalize
signal = signal / np.max(np.abs(signal)) * 0.9

# ============================================================================
#  YIN ALGORITHM IMPLEMENTATION
# ============================================================================

W = N // 2  # Integration window (half of buffer)

# Step 1: Squared Difference Function
d = np.zeros(W)
for tau in range(1, W):
    for j in range(N - tau):
        d[tau] += (signal[j] - signal[j + tau]) ** 2

# Step 2: Cumulative Mean Normalized Difference Function
d_prime = np.ones(W)
cumsum_d = 0
for tau in range(1, W):
    cumsum_d += d[tau]
    if cumsum_d > 0:
        d_prime[tau] = d[tau] / (cumsum_d / tau)

# Step 3: Absolute Threshold
threshold = 0.15
tau_estimate = 0

for tau in range(2, W):
    if d_prime[tau] < threshold:
        # Find local minimum
        while tau + 1 < W and d_prime[tau + 1] < d_prime[tau]:
            tau += 1
        tau_estimate = tau
        break

# Fallback if no threshold crossing
if tau_estimate == 0:
    tau_estimate = np.argmin(d_prime[2:]) + 2

# Step 4: Parabolic Interpolation
if 1 < tau_estimate < W - 1:
    y_prev = d_prime[tau_estimate - 1]
    y_curr = d_prime[tau_estimate]
    y_next = d_prime[tau_estimate + 1]

    denominator = y_prev - 2 * y_curr + y_next
    if abs(denominator) > 1e-10:
        delta = 0.5 * (y_prev - y_next) / denominator
    else:
        delta = 0
    tau_refined = tau_estimate + delta
else:
    tau_refined = tau_estimate
    delta = 0

# Calculate detected frequency
f0_detected = fs / tau_refined
confidence = 1 - d_prime[tau_estimate]

# ============================================================================
#  FIGURE SETUP - 4 PANEL LAYOUT
# ============================================================================

fig, axes = plt.subplots(4, 1, figsize=(16/2.54, 20/2.54), dpi=150)
fig.patch.set_facecolor('white')
plt.subplots_adjust(hspace=0.4, left=0.12, right=0.95, top=0.95, bottom=0.06)

# ============================================================================
#  PANEL (a): INPUT WAVEFORM
# ============================================================================

ax1 = axes[0]
t_ms = t * 1000  # Time in milliseconds

ax1.plot(t_ms, signal, color=GOOGLE_BLUE, linewidth=1.2)

# Mark two periods
period_ms = 1000 / f0_true
for p in range(1, 3):
    ax1.axvline(p * period_ms, linestyle='--', color=GOOGLE_RED, linewidth=1, alpha=0.7)

# Period annotation
ax1.annotate('', xy=(period_ms, 0.85), xytext=(0, 0.85),
             arrowprops=dict(arrowstyle='<->', color=GOOGLE_RED, lw=1.5))
ax1.text(period_ms / 2, 0.95, r'$T_0$', fontname='Times New Roman', fontsize=10,
         ha='center', color=GOOGLE_RED)

# Styling
ax1.set_xlim(0, t_ms[-1])
ax1.set_ylim(-1.1, 1.1)
ax1.set_xlabel('Time (ms)', fontname='Times New Roman', fontsize=11)
ax1.set_ylabel('Amplitude', fontname='Times New Roman', fontsize=11)
ax1.set_title('(a) Input Waveform', fontname='Times New Roman', fontsize=12, fontweight='bold')
ax1.grid(True, linestyle=':', alpha=0.3)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.tick_params(direction='out', length=3)

# ============================================================================
#  PANEL (b): SQUARED DIFFERENCE FUNCTION
# ============================================================================

ax2 = axes[1]
lag_samples = np.arange(1, W)
lag_ms = lag_samples / fs * 1000

ax2.plot(lag_ms, d[1:], color=GOOGLE_YELLOW, linewidth=1.5)

# Mark minimum (fundamental period)
valid_start = 20
min_idx = np.argmin(d[valid_start:W]) + valid_start
min_lag_ms = min_idx / fs * 1000
min_d = d[min_idx]

ax2.scatter(min_lag_ms, min_d, s=80, c=[GOOGLE_GREEN],
            edgecolors=[0.2, 0.2, 0.2], linewidths=1.5, zorder=10)

# Annotation
ax2.text(min_lag_ms + 0.5, min_d + np.max(d) * 0.08,
         f'τ = {min_lag_ms:.1f} ms', fontname='Times New Roman', fontsize=9,
         color=GOOGLE_GREEN * 0.8)

# Styling
ax2.set_xlim(0, lag_ms[-1])
ax2.set_ylim(0, np.max(d) * 1.1)
ax2.set_xlabel(r'Lag $\tau$ (ms)', fontname='Times New Roman', fontsize=11)
ax2.set_ylabel(r'$d(\tau)$', fontname='Times New Roman', fontsize=11)
ax2.set_title('(b) Squared Difference Function', fontname='Times New Roman', fontsize=12, fontweight='bold')
ax2.grid(True, linestyle=':', alpha=0.3)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.tick_params(direction='out', length=3)

# ============================================================================
#  PANEL (c): CUMULATIVE MEAN NORMALIZED DIFFERENCE
# ============================================================================

ax3 = axes[2]

ax3.plot(lag_ms, d_prime[1:], color=GOOGLE_RED, linewidth=1.5)

# Threshold line
ax3.axhline(threshold, linestyle='--', color=GOOGLE_GRAY, linewidth=1.5)
ax3.text(lag_ms[-1] * 0.85, threshold + 0.05,
         f'θ = {threshold:.2f}', fontname='Times New Roman', fontsize=9, color=GOOGLE_GRAY)

# Mark detected period
detected_lag_ms = tau_estimate / fs * 1000
ax3.scatter(detected_lag_ms, d_prime[tau_estimate], s=100, c=[GOOGLE_GREEN],
            edgecolors=[0.2, 0.2, 0.2], linewidths=1.5, marker='*', zorder=10)

# Vertical line at detection point
ax3.axvline(detected_lag_ms, linestyle=':', color=GOOGLE_GREEN, linewidth=1.2)

# Annotation
ax3.text(detected_lag_ms + 0.3, d_prime[tau_estimate] - 0.12,
         f'Detected: {detected_lag_ms:.2f} ms', fontname='Times New Roman', fontsize=9,
         color=GOOGLE_GREEN * 0.8)

# Styling
ax3.set_xlim(0, lag_ms[-1])
ax3.set_ylim(0, 1.5)
ax3.set_yticks(np.arange(0, 1.6, 0.25))
ax3.set_xlabel(r'Lag $\tau$ (ms)', fontname='Times New Roman', fontsize=11)
ax3.set_ylabel(r"$d'(\tau)$", fontname='Times New Roman', fontsize=11)
ax3.set_title('(c) Cumulative Mean Normalized Difference', fontname='Times New Roman', fontsize=12, fontweight='bold')
ax3.grid(True, linestyle=':', alpha=0.3)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.tick_params(direction='out', length=3)

# ============================================================================
#  PANEL (d): PARABOLIC INTERPOLATION DETAIL
# ============================================================================

ax4 = axes[3]

# Zoom into region around detected minimum
zoom_start = max(1, tau_estimate - 15)
zoom_end = min(W - 1, tau_estimate + 15)
zoom_range = np.arange(zoom_start, zoom_end + 1)
zoom_lag_ms = zoom_range / fs * 1000

ax4.plot(zoom_lag_ms, d_prime[zoom_range], color=GOOGLE_RED, linewidth=1.5)

# Plot the three points used for interpolation
if 1 < tau_estimate < W - 1:
    interp_points = [tau_estimate - 1, tau_estimate, tau_estimate + 1]
    interp_lag_ms = np.array(interp_points) / fs * 1000
    interp_vals = d_prime[interp_points]

    ax4.scatter(interp_lag_ms, interp_vals, s=80, c=[GOOGLE_BLUE],
                edgecolors=[0.2, 0.2, 0.2], linewidths=1.2, zorder=10)

    # Fit and plot parabola
    p_coeffs = np.polyfit(interp_lag_ms - interp_lag_ms[1], interp_vals, 2)
    para_x = np.linspace(interp_lag_ms[0], interp_lag_ms[2], 100) - interp_lag_ms[1]
    para_y = np.polyval(p_coeffs, para_x)
    ax4.plot(para_x + interp_lag_ms[1], para_y, '--', color=GOOGLE_YELLOW, linewidth=1.5)

    # Refined minimum point
    refined_lag_ms = tau_refined / fs * 1000
    refined_val = np.polyval(p_coeffs, refined_lag_ms - interp_lag_ms[1])

    ax4.scatter(refined_lag_ms, refined_val, s=150, c=[GOOGLE_GREEN],
                edgecolors=[0.2, 0.2, 0.2], linewidths=2, marker='*', zorder=15)

    # Horizontal line to show refinement
    ax4.plot([interp_lag_ms[1], refined_lag_ms], [interp_vals[1], interp_vals[1]],
             ':', color=GOOGLE_GREEN, linewidth=1)

# Results annotation box
result_str = f'$f_0$ = {f0_detected:.1f} Hz\nConfidence = {confidence:.2f}'
props = dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=GOOGLE_GRAY, alpha=0.9)
ax4.text(0.75, 0.85, result_str, transform=ax4.transAxes,
         fontname='Times New Roman', fontsize=10, ha='center', va='top', bbox=props)

# Styling
ax4.set_xlim(zoom_lag_ms[0], zoom_lag_ms[-1])
ax4.set_xlabel(r'Lag $\tau$ (ms)', fontname='Times New Roman', fontsize=11)
ax4.set_ylabel(r"$d'(\tau)$", fontname='Times New Roman', fontsize=11)
ax4.set_title('(d) Parabolic Interpolation Detail', fontname='Times New Roman', fontsize=12, fontweight='bold')
ax4.grid(True, linestyle=':', alpha=0.3)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)
ax4.tick_params(direction='out', length=3)

# Legend for panel (d)
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=GOOGLE_BLUE,
           markersize=8, markeredgecolor=[0.2, 0.2, 0.2], label='Discrete samples'),
    Line2D([0], [0], linestyle='--', color=GOOGLE_YELLOW, linewidth=1.5, label='Parabolic fit'),
    Line2D([0], [0], marker='*', color='w', markerfacecolor=GOOGLE_GREEN,
           markersize=12, markeredgecolor=[0.2, 0.2, 0.2], label='Refined estimate'),
]
ax4.legend(handles=legend_elements, loc='upper right', frameon=False,
           prop={'family': 'Times New Roman', 'size': 9})

# ============================================================================
#  EXPORT FIGURE
# ============================================================================

# Output paths
script_path = Path(__file__).parent
output_path = script_path.parent / 'output'
output_path.mkdir(exist_ok=True)

# Export as PNG (300 DPI)
fig.savefig(output_path / 'figure5_yin_algorithm_visualization.png',
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')

# Export as PDF (vector)
fig.savefig(output_path / 'figure5_yin_algorithm_visualization.pdf',
            bbox_inches='tight', facecolor='white', edgecolor='none')

# Export as SVG (vector)
fig.savefig(output_path / 'figure5_yin_algorithm_visualization.svg',
            bbox_inches='tight', facecolor='white', edgecolor='none')

print('Figure 5 exported successfully!')
print(f'Detected F0: {f0_detected:.2f} Hz (True: {f0_true} Hz)')
print(f'Confidence: {confidence:.3f}')
print(f'Output location: {output_path}')

plt.show()
