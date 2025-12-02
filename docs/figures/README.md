# Technical Report Figures

This directory contains Python scripts for generating publication-quality figures for the Mambo Whistle Technical Report.

## Directory Structure

```
figures/
├── scripts/           # Python source files
│   ├── figure1_pitch_detection_comparison.py
│   ├── figure5_yin_algorithm_visualization.py
│   └── figure7_latency_breakdown.py
├── output/            # Generated figures (PNG, PDF, SVG)
├── requirements.txt   # Python dependencies
└── README.md
```

## Figure Descriptions

### Figure 1: Pitch Detection Algorithm Comparison
- **Type**: Scatter plot with logarithmic x-axis
- **Content**: Compares pitch detection algorithms across accuracy, latency, and computational cost
- **Key Feature**: Highlights YIN algorithm's optimal position for browser-based real-time processing
- **Data Points**: YIN, Autocorrelation, CREPE, FCPE, OneBitPitch, PYIN, SWIPE

### Figure 5: YIN Algorithm Visualization
- **Type**: Four-panel vertical arrangement
- **Content**: Step-by-step visualization of YIN pitch detection
- **Panels**:
  - (a) Input waveform with periodic structure
  - (b) Squared Difference Function
  - (c) Cumulative Mean Normalized Difference with threshold
  - (d) Parabolic interpolation detail with refined estimate

### Figure 7: Latency Breakdown
- **Type**: Stacked horizontal bar chart
- **Content**: Pipeline stage latency contributions
- **Key Feature**: Shows thread boundary between AudioWorklet and Main thread
- **Comparison**: AudioWorklet vs ScriptProcessor performance

## Style Guidelines

All figures follow these specifications:
- **Font**: Times New Roman
- **Color Palette**: Google brand colors
  - Blue: #4285F4 (rgb: 66, 133, 244)
  - Red: #EA4335 (rgb: 234, 67, 53)
  - Yellow: #FBBC05 (rgb: 251, 188, 5)
  - Green: #34A853 (rgb: 52, 168, 83)
- **Resolution**: 300 DPI for PNG
- **Export Formats**: PNG, PDF, SVG

## Installation

```bash
cd docs/figures
pip install -r requirements.txt
```

## Usage

```bash
# Generate all figures
cd scripts
python figure1_pitch_detection_comparison.py
python figure5_yin_algorithm_visualization.py
python figure7_latency_breakdown.py
```

Or run all at once:
```bash
for f in scripts/*.py; do python "$f"; done
```

Output files will be saved to `output/` directory.

## Requirements

- Python 3.8+
- NumPy >= 1.20.0
- Matplotlib >= 3.5.0
- Times New Roman font (usually pre-installed on Windows/macOS)
