#!/usr/bin/env python3
"""
Figure 7: Latency Breakdown
Stacked horizontal bar chart showing pipeline stage contributions
Mambo Whistle Technical Report

Author: Mambo Whistle Team
Date: 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

# ============================================================================
#  CONFIGURATION
# ============================================================================

# Use Times New Roman font
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['axes.unicode_minus'] = False

# Google brand colors
GOOGLE_BLUE = np.array([66, 133, 244]) / 255
GOOGLE_RED = np.array([234, 67, 53]) / 255
GOOGLE_YELLOW = np.array([251, 188, 5]) / 255
GOOGLE_GREEN = np.array([52, 168, 83]) / 255
GOOGLE_GRAY = np.array([95, 99, 104]) / 255

# Extended palette for 7 stages (audio thread: blues/greens, main thread: yellows/reds)
STAGE_COLORS = [
    np.array([66, 133, 244]) / 255,    # Microphone Capture - Google Blue
    np.array([52, 168, 83]) / 255,     # Buffer Accumulation - Google Green
    np.array([23, 107, 135]) / 255,    # YIN Processing - Teal
    np.array([102, 187, 106]) / 255,   # FFT Processing - Light Green
    np.array([251, 188, 5]) / 255,     # Message Transfer - Google Yellow (boundary)
    np.array([255, 167, 38]) / 255,    # Synthesis - Orange
    np.array([234, 67, 53]) / 255,     # DOM Rendering - Google Red
]

# ============================================================================
#  LATENCY DATA (precise measurements from system)
# ============================================================================

# Stage data based on actual system measurements
stages = [
    ('Microphone Capture',   1.5,  'Audio Thread'),
    ('Buffer Accumulation', 12.0,  'Audio Thread'),
    ('YIN Pitch Detection',  0.5,  'Audio Thread'),
    ('FFT + Features',       0.1,  'Audio Thread'),
    ('Message Transfer',     0.8,  'Thread Boundary'),
    ('Synthesis Processing', 2.5,  'Main Thread'),
    ('DOM Rendering',       16.0,  'Main Thread'),
]

stage_names = [s[0] for s in stages]
latencies = np.array([s[1] for s in stages])
thread_types = [s[2] for s in stages]

# Total latency
total_latency = np.sum(latencies)

# Cumulative latencies for positioning
cumulative = np.cumsum(latencies)
cumulative = np.insert(cumulative, 0, 0)  # Start from 0

# ============================================================================
#  FIGURE SETUP
# ============================================================================

fig, ax = plt.subplots(figsize=(18/2.54, 10/2.54), dpi=150)
fig.patch.set_facecolor('white')

# ============================================================================
#  STACKED HORIZONTAL BAR CHART
# ============================================================================

bar_y = 0.5
bar_height = 0.25

# Draw each segment
for i, (name, latency) in enumerate(zip(stage_names, latencies)):
    x_start = cumulative[i]

    # Create rounded rectangle
    rect = FancyBboxPatch(
        (x_start, bar_y - bar_height/2), latency, bar_height,
        boxstyle="round,pad=0,rounding_size=0.02",
        facecolor=STAGE_COLORS[i],
        edgecolor=[0.3, 0.3, 0.3],
        linewidth=1
    )
    ax.add_patch(rect)

    # Add latency value inside bar (if wide enough)
    if latency > 2:
        ax.text(x_start + latency/2, bar_y, f'{latency:.1f} ms',
                fontname='Times New Roman', fontsize=9, fontweight='bold',
                ha='center', va='center', color='white')

# ============================================================================
#  100ms REFERENCE LINE
# ============================================================================

ax.axvline(100, linestyle='--', color=GOOGLE_RED, linewidth=2, alpha=0.8)
ax.text(100, bar_y + 0.38, '100 ms Perceptual Threshold',
        fontname='Times New Roman', fontsize=10, fontweight='bold',
        ha='center', color=GOOGLE_RED)

# ============================================================================
#  THREAD BOUNDARY INDICATOR
# ============================================================================

# Calculate boundary position (after Message Transfer starts)
boundary_x = cumulative[4] + latencies[4] / 2

# Vertical dashed line for thread boundary
ax.plot([boundary_x, boundary_x], [0.1, 0.9], ':',
        color=GOOGLE_GRAY, linewidth=1.5)

# Thread labels
ax.text(cumulative[4] / 2, 0.18, 'AudioWorklet Thread',
        fontname='Times New Roman', fontsize=9, fontstyle='italic',
        ha='center', color=GOOGLE_BLUE * 0.8)

ax.text(boundary_x + (total_latency - boundary_x) / 2, 0.18, 'Main Thread',
        fontname='Times New Roman', fontsize=9, fontstyle='italic',
        ha='center', color=GOOGLE_RED * 0.8)

# ============================================================================
#  TOTAL LATENCY ANNOTATION
# ============================================================================

# Arrow showing total latency
ax.annotate('', xy=(total_latency, 0.08), xytext=(0, 0.08),
            arrowprops=dict(arrowstyle='<->', color=[0.2, 0.2, 0.2], lw=1.2))

ax.text(total_latency / 2, 0.02, f'Total: {total_latency:.1f} ms',
        fontname='Times New Roman', fontsize=11, fontweight='bold',
        ha='center', color=[0.2, 0.2, 0.2])

# ============================================================================
#  LEGEND (Stage names with colors)
# ============================================================================

# Create legend below the main bar
legend_y = 0.92
legend_cols = 4
legend_x_positions = [5, 30, 58, 88]

for i, (name, latency) in enumerate(zip(stage_names, latencies)):
    row = i // legend_cols
    col = i % legend_cols

    lx = legend_x_positions[col] if col < len(legend_x_positions) else legend_x_positions[-1]
    ly = legend_y - row * 0.12

    # Color box
    rect = FancyBboxPatch(
        (lx - 3, ly - 0.03), 2, 0.06,
        boxstyle="round,pad=0,rounding_size=0.01",
        facecolor=STAGE_COLORS[i],
        edgecolor=[0.3, 0.3, 0.3],
        linewidth=0.5
    )
    ax.add_patch(rect)

    # Label
    ax.text(lx + 0.5, ly, f'{name} ({latency:.1f} ms)',
            fontname='Times New Roman', fontsize=8,
            ha='left', va='center', color=[0.2, 0.2, 0.2])

# ============================================================================
#  COMPARISON BARS (AudioWorklet vs ScriptProcessor)
# ============================================================================

# Add comparison section below main bar
comp_y = 0.35
comp_height = 0.08

# ScriptProcessor latency (for comparison)
script_processor_latency = 49.4  # Based on 2048 sample buffer

# Mambo Whistle (AudioWorklet)
rect_aw = FancyBboxPatch(
    (0, comp_y - comp_height/2), total_latency, comp_height,
    boxstyle="round,pad=0,rounding_size=0.01",
    facecolor=GOOGLE_GREEN, edgecolor=[0.3, 0.3, 0.3],
    linewidth=0.8, alpha=0.7
)
ax.add_patch(rect_aw)
ax.text(total_latency + 2, comp_y, f'AudioWorklet: {total_latency:.1f} ms',
        fontname='Times New Roman', fontsize=8, ha='left',
        color=GOOGLE_GREEN * 0.7)

# ScriptProcessor (legacy)
comp_y2 = 0.22
rect_sp = FancyBboxPatch(
    (0, comp_y2 - comp_height/2), script_processor_latency, comp_height,
    boxstyle="round,pad=0,rounding_size=0.01",
    facecolor=GOOGLE_GRAY, edgecolor=[0.3, 0.3, 0.3],
    linewidth=0.8, alpha=0.5
)
ax.add_patch(rect_sp)
ax.text(script_processor_latency + 2, comp_y2, f'ScriptProcessor: {script_processor_latency:.1f} ms',
        fontname='Times New Roman', fontsize=8, ha='left',
        color=GOOGLE_GRAY * 0.8)

# Improvement annotation
improvement = script_processor_latency / total_latency
ax.text(80, 0.28, f'{improvement:.1f}× improvement',
        fontname='Times New Roman', fontsize=9, fontstyle='italic', fontweight='bold',
        ha='center', color=GOOGLE_GREEN * 0.8)

# ============================================================================
#  PERCENTAGE BREAKDOWN BOX
# ============================================================================

# Calculate percentages
audio_thread_latency = np.sum(latencies[:4])
main_thread_latency = np.sum(latencies[5:])
audio_pct = audio_thread_latency / total_latency * 100
main_pct = main_thread_latency / total_latency * 100

table_str = (f'Latency Distribution:\n'
             f'Audio Thread: {audio_pct:.1f}% ({audio_thread_latency:.1f} ms)\n'
             f'Main Thread: {main_pct:.1f}% ({main_thread_latency:.1f} ms)')

props = dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=GOOGLE_GRAY,
             alpha=0.9, linewidth=1)
ax.text(0.88, 0.55, table_str, transform=ax.transAxes,
        fontname='Times New Roman', fontsize=9,
        ha='left', va='top', bbox=props)

# ============================================================================
#  AXIS CONFIGURATION
# ============================================================================

ax.set_xlim(0, 120)
ax.set_ylim(0, 1.05)

# X-axis ticks
ax.set_xticks(np.arange(0, 121, 20))

# Hide Y-axis (not meaningful for single bar)
ax.set_yticks([])
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# ============================================================================
#  STYLING
# ============================================================================

ax.spines['bottom'].set_linewidth(1.2)
ax.tick_params(direction='out', length=4, width=1.2, colors=[0.15, 0.15, 0.15])
ax.grid(True, axis='x', linestyle=':', alpha=0.3)

# Labels
ax.set_xlabel('Cumulative Latency (ms)', fontname='Times New Roman', fontsize=12)
ax.set_title('Audio Processing Pipeline Latency Breakdown',
             fontname='Times New Roman', fontsize=13, fontweight='bold', pad=15)

# ============================================================================
#  EXPORT FIGURE
# ============================================================================

plt.tight_layout()

# Output paths
script_path = Path(__file__).parent
output_path = script_path.parent / 'output'
output_path.mkdir(exist_ok=True)

# Export as PNG (300 DPI)
fig.savefig(output_path / 'figure7_latency_breakdown.png',
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')

# Export as PDF (vector)
fig.savefig(output_path / 'figure7_latency_breakdown.pdf',
            bbox_inches='tight', facecolor='white', edgecolor='none')

# Export as SVG (vector)
fig.savefig(output_path / 'figure7_latency_breakdown.svg',
            bbox_inches='tight', facecolor='white', edgecolor='none')

print('Figure 7 exported successfully!')
print(f'Total latency: {total_latency:.1f} ms')
print(f'Margin below 100ms threshold: {100 - total_latency:.1f} ms')
print(f'Output location: {output_path}')

plt.show()
