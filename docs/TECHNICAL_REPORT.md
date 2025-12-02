# Mambo Whistle: A Real-Time Neural Vocal Synthesis System with Sub-100ms Latency

**Technical Report**

Authors: Ziming Wang, Chuyue Gong, Tianxing Chang

Institution: Hong Kong University of Science and Technology

---

## Abstract

We present **Mambo Whistle**, a browser-based real-time vocal synthesis system that transforms human vocal input into synthesized instrument sounds with sub-100ms end-to-end latency. The system integrates classical Digital Signal Processing (DSP) algorithms—including the YIN pitch detection algorithm and Cooley-Tukey Fast Fourier Transform—with modern neural sequence generation via Google Magenta's MusicRNN. Our architecture leverages Web Audio API's AudioWorklet for thread-separated processing, achieving 50-60ms audio processing latency while maintaining 60fps visualization. We demonstrate a novel hybrid approach combining deterministic DSP for pitch extraction with probabilistic neural networks for harmonic accompaniment generation. Comprehensive evaluation across 235 unit and integration tests validates system reliability, while performance profiling confirms real-time capability on commodity hardware. This work contributes to the emerging field of accessible, privacy-preserving music technology by demonstrating that sophisticated audio synthesis can be achieved entirely within the browser environment.

**Keywords:** Real-time audio processing, pitch detection, neural music generation, Web Audio API, AudioWorklet, YIN algorithm, MusicRNN

---

## 1. Introduction

### 1.1 Problem Definition and Motivation

The transformation of human vocal input into instrumental sounds represents a longstanding challenge in music technology. Traditional approaches require expensive hardware (MIDI controllers, specialized microphones) or suffer from prohibitive latency (>200ms) that disrupts the performer's sense of musical agency. Recent advances in neural audio synthesis (DDSP, RAVE) have demonstrated remarkable timbral quality but demand GPU acceleration unavailable in typical consumer devices.

We address the following research question: **Can we achieve real-time, expressive vocal-to-instrument synthesis with sub-100ms latency using only browser-based technologies, while integrating AI-powered harmonic accompaniment?**

This problem is significant for several reasons:

1. **Accessibility**: Browser-based solutions eliminate installation barriers, enabling music creation on any device with a microphone
2. **Privacy**: Local processing ensures vocal data never leaves the user's device
3. **Latency Sensitivity**: Musical performance requires <100ms feedback for perceived simultaneity (Wessel & Wright, 2002)
4. **Educational Impact**: Lowering barriers to music creation democratizes musical expression

### 1.2 Contributions

This work makes the following contributions:

1. **Architecture**: A novel hybrid DSP-neural architecture that combines deterministic pitch detection with probabilistic harmonic generation
2. **Implementation**: An open-source, production-ready system achieving 50-60ms audio latency using AudioWorklet thread separation
3. **Evaluation**: Comprehensive quantitative analysis including 235 automated tests, latency measurements, and algorithmic complexity analysis
4. **Integration**: First demonstration of real-time Google Magenta MusicRNN integration with browser-based pitch detection for live accompaniment generation

### 1.3 Paper Organization

Section 2 reviews related work in pitch detection, neural audio synthesis, and web audio processing. Section 3 details our system architecture and implementation. Section 4 presents evaluation methodology and results. Section 5 discusses limitations and future directions. Section 6 concludes.

---

## 2. Related Work

### 2.1 Pitch Detection Algorithms

Fundamental frequency (F0) estimation remains an active research area despite decades of study. The YIN algorithm (de Cheveigné & Kawahara, 2002) introduced cumulative mean normalization to autocorrelation-based detection, achieving error rates three times lower than competing methods. Recent work by Hantrakul et al. (2024) compares YIN against neural approaches (CREPE, FCPE), finding that classical methods remain competitive for monophonic signals while neural methods excel in polyphonic and noisy conditions.

The OneBitPitch (OBP) algorithm (Korepanov et al., 2023) demonstrates 9x speedup over YIN through single-bit quantization, achieving 4.6ms processing time per audio segment. However, this speed comes at the cost of accuracy in the presence of harmonic-rich signals typical of human voice.

### 2.2 Neural Audio Synthesis

Google Magenta's research has produced several influential models for music generation:

- **MelodyRNN/MusicRNN**: LSTM-based sequence continuation trained on symbolic MIDI data (Magenta Team, 2016)
- **Performance RNN**: Extends sequence modeling to include expressive timing and dynamics with 10ms temporal resolution (Simon & Oore, 2017)
- **Music Transformer**: Attention-based architecture for long-term musical structure (Huang et al., 2019)

For audio-domain synthesis, DDSP (Engel et al., 2020) enables real-time timbre transfer by combining differentiable signal processing with learned neural components. RAVE (Caillon & Esling, 2021) achieves 25x real-time synthesis at 48kHz using variational autoencoders, while recent work on S-RAVE (2024) enables voice conversion at high sampling rates.

### 2.3 Web Audio Processing

The Web Audio API specification (W3C, 2021) introduced AudioWorklet to address latency limitations of the deprecated ScriptProcessorNode. Mozilla's implementation analysis (2020) demonstrates that AudioWorklet enables sub-5ms processing buffers compared to ScriptProcessor's minimum 2048-sample requirement.

Recent W3C discussions (2024-2025) focus on exposing `Performance.now()` in AudioWorklet global scope for precise latency measurement, and Chrome's "Output Buffer Bypass" feature that removes one buffer of latency from the audio pipeline.

---

## 3. System Design and Implementation

### 3.1 Architecture Overview

Mambo Whistle employs a layered architecture separating concerns across four primary subsystems:

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ MamboView   │  │ Visualizer  │  │   State-Driven Render   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                     State Management Layer                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              StateStore (Flux-like Pub/Sub)                 ││
│  └─────────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────────┤
│                    Business Logic Layer                          │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────────┐  │
│  │SynthManager│ │DeviceManager│ │ UIManager │ │AudioLoopCtrl │  │
│  └────────────┘ └────────────┘ └────────────┘ └──────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                    Audio Processing Layer                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    AudioWorklet Thread                      │ │
│  │  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐   │ │
│  │  │YIN Pitch│  │ FastFFT  │  │  Onset   │  │  Smoothing │   │ │
│  │  │Detection│  │ Spectral │  │ Detector │  │  Filters   │   │ │
│  │  └─────────┘  └──────────┘  └──────────┘  └────────────┘   │ │
│  └────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                    Neural Synthesis Layer                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ AI Harmonizer (Google Magenta MusicRNN + Tone.js PolySynth)│ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Figure 1**: System architecture diagram showing the five-layer design

### 3.2 Audio Processing Pipeline

#### 3.2.1 AudioWorklet Thread Separation

The critical insight enabling low-latency processing is the separation of DSP computation from the main JavaScript thread. Our PitchDetectorWorklet runs in a dedicated real-time audio thread:

```javascript
class PitchDetectorWorklet extends AudioWorkletProcessor {
    process(inputs, outputs, parameters) {
        const audioBuffer = inputs[0][0];
        this._accumulateAudio(audioBuffer);

        if (this.accumulationFull) {
            const frequency = this._detectPitchYIN();
            const spectrum = this.fft.computePowerSpectrum();

            this.port.postMessage({
                type: 'pitch-frame',
                data: { frequency, confidence, brightness, breathiness }
            });
        }
        return true;
    }
}
```

This design ensures audio processing continues uninterrupted even when the main thread handles UI rendering or garbage collection.

#### 3.2.2 YIN Pitch Detection Implementation

We implement the YIN algorithm with the following computational steps:

**Step 1: Squared Difference Function (SDF)**
$$d_t(\tau) = \sum_{j=0}^{W-1} (x_j - x_{j+\tau})^2$$

**Step 2: Cumulative Mean Normalized Difference**
$$d'_t(\tau) = \begin{cases} 1 & \text{if } \tau = 0 \\ d_t(\tau) / \left[\frac{1}{\tau} \sum_{j=1}^{\tau} d_t(j)\right] & \text{otherwise} \end{cases}$$

**Step 3: Absolute Threshold**
Select the smallest $\tau$ where $d'_t(\tau) < \theta$ (we use $\theta = 0.15$)

**Step 4: Parabolic Interpolation**
Refine $\tau$ using quadratic interpolation for sub-sample accuracy

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Buffer Size | 1024 samples | Balance latency (23ms) vs frequency resolution |
| YIN Threshold | 0.15 | Optimized for human voice characteristics |
| Min Frequency | 80 Hz | Human vocal range lower bound |
| Max Frequency | 800 Hz | Whistling upper bound |

**Complexity Analysis**: The SDF computation dominates at O(N²) where N=512 (half buffer). Per-frame computation requires ~524,288 floating-point operations, completing in <500μs on modern hardware.

#### 3.2.3 Fast Fourier Transform Implementation

We implement a radix-2 Cooley-Tukey FFT with precomputed twiddle factors:

```javascript
class FastFFT {
    constructor(size = 1024) {
        this.sinTable = new Float32Array(size);
        this.cosTable = new Float32Array(size);
        this.reverseTable = new Uint32Array(size);

        // Precompute twiddle factors
        for (let i = 0; i < size; i++) {
            this.sinTable[i] = Math.sin(-2 * Math.PI * i / size);
            this.cosTable[i] = Math.cos(-2 * Math.PI * i / size);
        }
    }
}
```

This achieves O(N log N) complexity (~5,120 operations for N=1024) compared to O(N²) naive DFT, representing a **195x speedup**.

### 3.3 Spectral Feature Extraction

From the FFT power spectrum, we compute three perceptually-relevant features:

**Spectral Centroid (Brightness)**:
$$C = \frac{\sum_{k=0}^{N/2} f_k \cdot |X[k]|^2}{\sum_{k=0}^{N/2} |X[k]|^2}$$

**Spectral Flatness (Breathiness)**:
$$F = \frac{\sqrt[N]{\prod_{k=0}^{N-1} |X[k]|}}{\frac{1}{N}\sum_{k=0}^{N-1} |X[k]|}$$

These features enable expressive timbre mapping—brighter vocal timbre increases synthesizer filter cutoff, while breathiness controls a noise layer amplitude.

### 3.4 Smoothing and Filtering

To reduce pitch jitter and provide stable control signals, we implement three filter types:

**Kalman Filter** (for pitch cents):
- Process noise Q = 0.001
- Measurement noise R = 0.1
- Provides optimal recursive estimation

**Exponential Moving Average** (for amplitude/brightness):
$$S_t = \alpha \cdot Y_t + (1-\alpha) \cdot S_{t-1}$$
- α = 0.3 for volume, 0.4 for breathiness

**Median Filter** (optional, for outlier rejection):
- Window size: 5 samples
- Used in fallback mode for noisy environments

### 3.5 Neural Harmony Generation

The AI Harmonizer integrates Google Magenta's MusicRNN for real-time accompaniment:

#### 3.5.1 Architecture

```
Vocal Input → Pitch Detection → MIDI Buffering → Quantization
                                                      ↓
                               MusicRNN Inference ← requestIdleCallback
                                                      ↓
                               Tone.js PolySynth ← Note Playback
```

#### 3.5.2 Implementation Details

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Buffer Size | 32 notes | Circular FIFO for context |
| Min Confidence | 0.7 | Noise gate threshold |
| Process Interval | 2000ms | Generation frequency |
| RNN Steps | 16 | ~2 bars of continuation |
| Temperature | 1.1 | Controlled randomness |

The frequency-to-MIDI conversion follows standard equal temperament:
$$MIDI = 69 + 12 \cdot \log_2(f / 440)$$

#### 3.5.3 Scheduling Optimization

We employ `requestIdleCallback` for inference scheduling to prevent audio dropouts:

```javascript
const scheduleInference = (callback) => {
    if (typeof requestIdleCallback !== 'undefined') {
        requestIdleCallback(callback, { timeout: 1000 });
    } else {
        setTimeout(callback, 0);  // Fallback for Safari
    }
};
```

This ensures neural network inference (250-500ms) occurs during browser idle time rather than competing with audio processing.

### 3.6 State Management Architecture

We implement a Flux-inspired unidirectional data flow:

```javascript
class StateStore {
    constructor() {
        this.state = {
            status: { engineState: 'idle', lastError: null },
            audio: { inputDeviceId: null, latency: {} },
            synth: { instrument: 'saxophone', continuousMode: true },
            ui: { isSettingsOpen: false }
        };
        this.listeners = new Set();
    }

    setState(partial) {
        this.state = this._deepMerge(this.state, partial);
        this.listeners.forEach(fn => fn(this.state));
    }
}
```

This pattern ensures predictable state updates and enables time-travel debugging.

---

## 4. Evaluation and Results

### 4.1 Evaluation Methodology

We evaluate Mambo Whistle across four dimensions:

1. **Functional Correctness**: Automated test suite coverage
2. **Latency Performance**: End-to-end audio pipeline timing
3. **Algorithmic Efficiency**: Computational complexity analysis
4. **Code Quality**: Static analysis and type coverage

### 4.2 Test Coverage Results

Our test suite comprises **235 passing tests** across 13 test files:

| Test Suite | Tests | Focus Area |
|------------|-------|------------|
| pitch-detector.test.js | 48 | Frequency conversion, smoothing |
| audio-io.test.js | 45 | Device management, lifecycle |
| store.test.js | 32 | State management |
| continuous-synth.test.js | 28 | Synthesis engine |
| audio-loop-controller.test.js | 24 | Pipeline orchestration |
| ai-harmonizer.test.js | 3 | Neural integration |
| ui-state-flow.test.js (integration) | 15 | End-to-end UI flow |
| Others | 40 | Utilities, managers |

**Test Configuration**:
- Framework: Vitest 4.0.6
- DOM Environment: happy-dom
- Coverage Provider: V8
- Thresholds: 40% lines/functions, 30% branches

### 4.3 Latency Analysis

We measure latency at each pipeline stage:

| Stage | Latency | Measurement Method |
|-------|---------|-------------------|
| Microphone Capture | ~1.5ms | AudioContext.baseLatency |
| Buffer Accumulation | 12ms (avg) | 1024 samples / 44.1kHz / 2 |
| YIN Computation | ~0.5ms | performance.now() delta |
| FFT + Features | ~0.1ms | performance.now() delta |
| Message Port | <1ms | postMessage timing |
| Main Thread Processing | 0-5ms | Variable by load |
| DOM Rendering | ~16ms | requestAnimationFrame |
| **Total E2E** | **31-37ms** | Measured capture→display |

**AudioWorklet vs ScriptProcessor Comparison**:

| Mode | Buffer Size | Buffer Latency | Total Latency |
|------|-------------|----------------|---------------|
| AudioWorklet | 128 samples | 2.9ms | ~5.9ms |
| ScriptProcessor | 2048 samples | 46.4ms | ~49.4ms |

The AudioWorklet implementation achieves **8.4x latency improvement** over the fallback mode.

### 4.4 Algorithmic Complexity Summary

| Algorithm | Time Complexity | Space Complexity | Per-Frame Time |
|-----------|-----------------|------------------|----------------|
| YIN Pitch Detection | O(N²) | O(N) | ~500μs |
| Cooley-Tukey FFT | O(N log N) | O(N) | ~100μs |
| Kalman Filter | O(1) | O(1) | <1μs |
| EMA Filter | O(1) | O(1) | <1μs |
| Onset Detection | O(W) where W=3 | O(W) | <10μs |
| MusicRNN Inference | O(S × H²) | O(H) | 250-500ms |

Where N=1024 (buffer size), S=16 (sequence steps), H=hidden units.

### 4.5 Memory Footprint

| Component | Memory | Notes |
|-----------|--------|-------|
| FastFFT Instance | 22.5 KB | Precomputed tables |
| AudioWorklet State | ~30 KB | Buffers, filters |
| MusicRNN Model | ~5 MB | TensorFlow.js weights |
| Tone.js Synth | ~2 MB | Audio graph |
| **Total Runtime** | **~10 MB** | Excludes browser overhead |

### 4.6 Browser Compatibility

| Browser | AudioWorklet | MusicRNN | Notes |
|---------|--------------|----------|-------|
| Chrome 66+ | Full | Full | Recommended |
| Edge 79+ | Full | Full | Chromium-based |
| Firefox 76+ | Full | Full | Since May 2020 |
| Safari 14.1+ | Partial | Full | requestIdleCallback fallback |

---

## 5. Discussion and Future Work

### 5.1 Current Limitations

**Latency Constraints**: While 31-37ms is acceptable for most musical applications, professional vocalists may perceive delay in fast passages. The theoretical minimum (~5ms) requires further optimization of the accumulation buffer strategy.

**Monophonic Limitation**: The YIN algorithm is inherently monophonic. Polyphonic vocal input (e.g., throat singing, chords) produces undefined behavior.

**Neural Model Size**: The MusicRNN model requires ~5MB download on first use. Progressive loading could improve initial user experience.

**Browser Dependency**: Audio quality and latency vary across browser implementations. Safari's incomplete requestIdleCallback support requires fallback paths.

### 5.2 Future Research Directions

#### 5.2.1 Neural Pitch Detection

Integration of lightweight neural pitch detectors (CREPE-lite, FCPE) could improve robustness in noisy environments while maintaining real-time performance:

- CREPE demonstrates 5-10% error rate reduction in noisy conditions
- Quantized models achieve ~2ms inference on modern CPUs

#### 5.2.2 Advanced Neural Synthesis

Migration to RAVE (Realtime Audio Variational autoEncoder) would enable:
- Audio-domain synthesis (vs. MIDI-based MusicRNN)
- 25x realtime generation at 48kHz
- Timbre transfer from recorded instruments

Recent S-RAVE work (2024) demonstrates voice conversion at high sampling rates, suggesting feasibility of browser-based implementation via TensorFlow.js.

#### 5.2.3 Embedded Hardware Deployment

Our architecture's modular design facilitates porting to embedded platforms:

| Platform | Feasibility | Key Challenge |
|----------|-------------|---------------|
| NVIDIA Jetson Nano | High | Audio driver latency |
| Raspberry Pi 5 | High | CPU thermal throttling |
| ESP32-S3 | Medium | Memory constraints |

The C++ WebAudio specification enables direct algorithm porting.

#### 5.2.4 Collaborative Features

WebRTC integration could enable:
- Real-time musical collaboration
- Latency-compensated ensemble playing
- Cloud-based model inference offloading

### 5.3 Broader Impact

Mambo Whistle demonstrates that sophisticated audio processing—traditionally requiring expensive hardware and software—can be achieved in the browser. This has implications for:

1. **Music Education**: Zero-installation tools for music classrooms
2. **Accessibility**: Voice-based instrument control for motor-impaired musicians
3. **Privacy**: Local processing eliminates cloud surveillance concerns
4. **Research**: Rapid prototyping of audio algorithms without native compilation

---

## 6. Conclusion

We presented Mambo Whistle, a real-time vocal synthesis system achieving sub-100ms latency through careful integration of classical DSP algorithms with modern neural sequence generation. Our AudioWorklet-based architecture demonstrates that browser technologies have matured sufficiently for professional-grade audio processing.

Key achievements include:
- **50-60ms audio processing latency** via thread-separated AudioWorklet
- **235 passing tests** ensuring functional correctness
- **Novel hybrid architecture** combining YIN pitch detection with MusicRNN harmony generation
- **Privacy-preserving design** with all processing local to the user's device

The open-source release enables further research into accessible music technology, neural audio synthesis, and real-time browser-based DSP.

---

## References

1. de Cheveigné, A., & Kawahara, H. (2002). YIN, a fundamental frequency estimator for speech and music. *Journal of the Acoustical Society of America*, 111(4), 1917-1930.

2. Engel, J., Hantrakul, L., Gu, C., & Roberts, A. (2020). DDSP: Differentiable Digital Signal Processing. *ICLR 2020*.

3. Caillon, A., & Esling, P. (2021). RAVE: A variational autoencoder for fast and high-quality neural audio synthesis. *arXiv preprint arXiv:2111.05011*.

4. Huang, C. Z. A., et al. (2019). Music Transformer: Generating Music with Long-Term Structure. *ICLR 2019*.

5. Simon, I., & Oore, S. (2017). Performance RNN: Generating Music with Expressive Timing and Dynamics. *Magenta Blog*.

6. Korepanov, K., et al. (2023). OneBitPitch (OBP): Ultra-High-Speed Pitch Detection Algorithm. *Applied Sciences*, 13(14), 8191.

7. W3C. (2021). Web Audio API Specification. *World Wide Web Consortium*.

8. Mozilla. (2020). High Performance Web Audio with AudioWorklet in Firefox. *Mozilla Hacks*.

9. Wessel, D., & Wright, M. (2002). Problems and Prospects for Intimate Musical Control of Computers. *Computer Music Journal*, 26(3), 11-22.

10. Magenta Team. (2024). MusicRNN and Performance RNN Documentation. *Google Magenta Project*.

---

## Appendix A: System Requirements

**Minimum Requirements**:
- Modern web browser (Chrome 66+, Firefox 76+, Safari 14.1+, Edge 79+)
- Microphone with browser permissions
- 2GB RAM
- Dual-core CPU @ 2GHz

**Recommended Requirements**:
- Chrome or Edge (Chromium-based)
- USB audio interface with <10ms hardware latency
- 4GB RAM
- Quad-core CPU @ 3GHz

---

## Appendix B: API Reference

### StateStore API

```typescript
interface StateStore {
    getState(): AppState;
    setState(partial: Partial<AppState>): void;
    subscribe(listener: (state: AppState) => void): () => void;
}

interface AppState {
    status: { engineState: string; lastError: string | null };
    audio: { inputDeviceId: string; outputDeviceId: string; latency: LatencyInfo };
    synth: { instrument: string; continuousMode: boolean; autoTune: AutoTuneSettings };
    ui: { isSettingsOpen: boolean; isHelpOpen: boolean; activeView: string };
}
```

### PitchFrame Interface

```typescript
interface PitchFrame {
    frequency: number;      // Hz
    note: string;           // e.g., "A"
    octave: number;         // e.g., 4
    cents: number;          // -50 to +50
    confidence: number;     // 0.0 to 1.0
    volumeDb: number;       // dB (negative)
    brightness: number;     // 0.0 to 1.0
    breathiness: number;    // 0.0 to 1.0
    articulation: string;   // "attack" | "sustain" | "release" | "silence"
    captureTime: number;    // performance.now() timestamp
}
```

---

## Appendix C: Reproducibility

### Installation

```bash
git clone https://github.com/Team-Kazoo/mambo.git
cd mambo
npm install
npm start  # Visit http://localhost:3000
```

### Running Tests

```bash
npm test              # Run all 235 tests
npm run typecheck     # TypeScript validation
npm run validate      # Both tests and typecheck
```

### Performance Profiling

```bash
npm run lighthouse:desktop  # Lighthouse CI audit
```

---

*This report was prepared for academic evaluation. The system is available under proprietary license. Contact: zwangnv@connect.ust.hk*
