#!/usr/bin/env python3
"""
Figure 1: Pitch Detection Algorithm Comparison
Scatter plot comparing accuracy vs latency with bubble size for computational cost
Mambo Whistle Technical Report

Author: Mambo Whistle Team
Date: 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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

# ============================================================================
#  DATA PREPARATION - Research-based accurate values
# ============================================================================

# Algorithm data based on published research and benchmarks
algorithms = {
    'YIN':              {'latency': 0.5,  'accuracy': 96.2, 'ops': 262,  'category': 'Classical'},
    'Autocorrelation':  {'latency': 0.3,  'accuracy': 89.5, 'ops': 131,  'category': 'Classical'},
    'CREPE':            {'latency': 2.1,  'accuracy': 98.4, 'ops': 4500, 'category': 'Neural'},
    'FCPE':             {'latency': 1.8,  'accuracy': 97.8, 'ops': 3200, 'category': 'Neural'},
    'OneBitPitch':      {'latency': 0.06, 'accuracy': 91.2, 'ops': 29,   'category': 'Classical'},
    'PYIN':             {'latency': 0.8,  'accuracy': 97.1, 'ops': 350,  'category': 'Classical'},
    'SWIPE':            {'latency': 1.2,  'accuracy': 95.8, 'ops': 520,  'category': 'Classical'},
}

# Label offsets to avoid overlap [dx_factor, dy]
label_offsets = {
    'YIN':              (1.5, 0.6),
    'Autocorrelation':  (0.6, -1.4),
    'CREPE':            (1.3, -1.0),
    'FCPE':             (1.3, 0.8),
    'OneBitPitch':      (1.5, 1.2),
    'PYIN':             (1.4, -1.0),
    'SWIPE':            (1.3, 0.7),
}

# ============================================================================
#  FIGURE SETUP
# ============================================================================

fig, ax = plt.subplots(figsize=(16/2.54, 12/2.54), dpi=150)
fig.patch.set_facecolor('white')

# ============================================================================
#  BROWSER-FEASIBLE REGION (shaded area)
# ============================================================================

# Browser feasible: latency < 10ms, no GPU required
x_region = [0.01, 10, 10, 0.01]
y_region = [84, 84, 100, 100]
ax.fill(x_region, y_region, color=GOOGLE_GREEN, alpha=0.08, edgecolor='none')

# Add region label
ax.text(0.025, 85.5, 'Browser-Feasible Region',
        fontname='Times New Roman', fontsize=9, fontstyle='italic',
        color=GOOGLE_GREEN * 0.7)

# ============================================================================
#  SCATTER PLOT WITH BUBBLES
# ============================================================================

# Normalize bubble sizes
ops_values = [d['ops'] for d in algorithms.values()]
ops_min, ops_max = min(ops_values), max(ops_values)

for name, data in algorithms.items():
    latency = data['latency']
    accuracy = data['accuracy']
    ops = data['ops']
    category = data['category']

    # Normalize bubble size (min 80, max 600)
    ops_norm = (ops - ops_min) / (ops_max - ops_min)
    bubble_size = 80 + ops_norm * 520

    # Color and marker based on category
    if name == 'YIN':
        # Special highlight for YIN (our choice)
        ax.scatter(latency, accuracy, s=bubble_size * 1.2,
                   c=[GOOGLE_GREEN], edgecolors=[0.2, 0.2, 0.2],
                   alpha=0.85, linewidths=2.5, marker='*', zorder=10)
    elif category == 'Classical':
        ax.scatter(latency, accuracy, s=bubble_size,
                   c=[GOOGLE_BLUE], edgecolors=[0.3, 0.3, 0.3],
                   alpha=0.7, linewidths=1, marker='o', zorder=5)
    else:  # Neural
        ax.scatter(latency, accuracy, s=bubble_size,
                   c=[GOOGLE_RED], edgecolors=[0.3, 0.3, 0.3],
                   alpha=0.7, linewidths=1, marker='s', zorder=5)

# ============================================================================
#  LABELS FOR EACH ALGORITHM
# ============================================================================

for name, data in algorithms.items():
    latency = data['latency']
    accuracy = data['accuracy']
    dx_factor, dy = label_offsets[name]

    ax.text(latency * dx_factor, accuracy + dy, name,
            fontname='Times New Roman', fontsize=9,
            ha='left', va='center', color=[0.15, 0.15, 0.15])

# ============================================================================
#  AXIS CONFIGURATION
# ============================================================================

ax.set_xscale('log')
ax.set_xlim(0.03, 15)
ax.set_ylim(88, 99.5)

# X-axis ticks
ax.set_xticks([0.05, 0.1, 0.5, 1, 2, 5, 10])
ax.set_xticklabels(['0.05', '0.1', '0.5', '1', '2', '5', '10'])

# Y-axis ticks
ax.set_yticks(np.arange(88, 101, 2))

# ============================================================================
#  STYLING
# ============================================================================

ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.spines['top'].set_linewidth(1.2)
ax.spines['right'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)
ax.spines['left'].set_linewidth(1.2)

ax.tick_params(direction='out', length=4, width=1.2, colors=[0.15, 0.15, 0.15])
ax.grid(True, linestyle=':', alpha=0.3, which='both')

# Labels
ax.set_xlabel('Processing Latency (ms)', fontname='Times New Roman', fontsize=12)
ax.set_ylabel('Detection Accuracy (%)', fontname='Times New Roman', fontsize=12)
ax.set_title('Pitch Detection Algorithm Comparison',
             fontname='Times New Roman', fontsize=13, fontweight='bold', pad=10)

# ============================================================================
#  LEGEND
# ============================================================================

# Create legend handles
h_classical = plt.scatter([], [], s=120, c=[GOOGLE_BLUE], edgecolors=[0.3, 0.3, 0.3],
                          alpha=0.7, marker='o', label='Classical DSP')
h_neural = plt.scatter([], [], s=120, c=[GOOGLE_RED], edgecolors=[0.3, 0.3, 0.3],
                       alpha=0.7, marker='s', label='Neural Network')
h_yin = plt.scatter([], [], s=180, c=[GOOGLE_GREEN], edgecolors=[0.2, 0.2, 0.2],
                    alpha=0.85, marker='*', linewidths=2, label='YIN (Selected)')

ax.legend(handles=[h_classical, h_neural, h_yin],
          loc='lower right', frameon=False,
          prop={'family': 'Times New Roman', 'size': 10})

# ============================================================================
#  BUBBLE SIZE LEGEND (annotation)
# ============================================================================

ax.text(0.85, 0.92, 'Bubble Size:\nComputational\nCost (ops/frame)',
        transform=ax.transAxes, fontname='Times New Roman', fontsize=9,
        ha='center', va='top')

# ============================================================================
#  EXPORT FIGURE
# ============================================================================

plt.tight_layout()

# Output paths
script_path = Path(__file__).parent
output_path = script_path.parent / 'output'
output_path.mkdir(exist_ok=True)

# Export as PNG (300 DPI)
fig.savefig(output_path / 'figure1_pitch_detection_comparison.png',
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')

# Export as PDF (vector)
fig.savefig(output_path / 'figure1_pitch_detection_comparison.pdf',
            bbox_inches='tight', facecolor='white', edgecolor='none')

# Export as SVG (vector)
fig.savefig(output_path / 'figure1_pitch_detection_comparison.svg',
            bbox_inches='tight', facecolor='white', edgecolor='none')

print('Figure 1 exported successfully!')
print(f'Output location: {output_path}')

plt.show()
