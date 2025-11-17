---
name: web-audio-optimization
description: Optimize Web Audio API performance for ultra-low latency audio processing
category: audio
tags: [web-audio, performance, latency, dsp, audioworklet]
version: 1.0.0
---

# Web Audio Optimization Skill

## Purpose
Optimize Web Audio API implementations to achieve <50ms end-to-end latency for real-time audio processing applications.

## When to Use
- Reducing audio processing latency
- Optimizing AudioWorklet performance
- Profiling audio pipeline bottlenecks
- Debugging audio glitches or dropouts

## Core Principles

### 1. Minimize Buffer Sizes
- Use smallest stable buffer (128-256 samples)
- Verify AudioWorklet is active (not ScriptProcessor fallback)
- Check: `audioContext.baseLatency` and `audioContext.outputLatency`

### 2. Optimize AudioWorklet Code
- Avoid allocations in `process()` method
- Pre-allocate all Float32Arrays in constructor
- Use typed arrays, avoid object creation
- Keep processing logic minimal and fast

### 3. Reduce Processing Chain
- Minimize nodes between input and output
- Combine filters when possible
- Avoid unnecessary gain/analyzer nodes
- Direct connections: Input → Worklet → Output

### 4. Profile and Measure
- Use `performance.now()` for timing
- Track p50, p95, p99 latency percentiles
- Monitor CPU usage in audio thread
- Check for buffer underruns

## Implementation Checklist

- [ ] Verify AudioWorklet mode (not ScriptProcessor)
- [ ] Buffer size ≤ 256 samples
- [ ] Zero allocations in process() loop
- [ ] Minimal node chain (< 5 nodes)
- [ ] Latency measurement instrumented
- [ ] CPU usage < 30% on target device

## Common Bottlenecks

1. **FFT Computation**: Use smaller FFT size or reduce frequency
2. **Feature Extraction**: Defer non-critical features to requestAnimationFrame
3. **Synthesizer Complexity**: Simplify filter chains, reduce oscillators
4. **UI Updates**: Throttle DOM updates to 60Hz max
5. **ScriptProcessor Fallback**: Fix HTTPS/localhost requirement

## Measurement Commands

```javascript
// In browser console
window.app.getLatencyStats() // End-to-end latency
window.container.get('audioIO').mode // Verify 'worklet'
audioContext.baseLatency * 1000 // Base latency in ms
audioContext.outputLatency * 1000 // Output latency in ms
```

## Target Latency Budget (50ms total)

- Input capture: 5-10ms
- AudioWorklet processing: 10-15ms
- Feature extraction: 5-10ms
- Synthesizer: 10-15ms
- Output: 5-10ms

## Kazoo Proto Specific Optimizations

### Current Bottlenecks (180ms → <50ms target)

1. **Buffer Size**: Check if using optimal size
   - Location: `js/audio-config.js` - AUDIO_CONFIG.BUFFER_SIZE
   - Current: May be too large (2048 = 46ms at 44.1kHz)
   - Target: 128 samples (2.9ms at 44.1kHz)

2. **YIN Algorithm**: Pitch detection overhead
   - Location: `js/pitch-detector.js`, `js/pitch-worklet.js`
   - Optimization: Reduce buffer size, optimize autocorrelation
   - Consider: Faster algorithm (MPM, AMDF) for lower latency

3. **Feature Extraction Pipeline**
   - Location: `js/expressive-features.js`
   - Spectral features: `js/features/spectral-features.js` (FFT heavy)
   - Optimization: Reduce FFT size, increase interval, skip non-critical features

4. **Continuous Synthesizer**
   - Location: `js/continuous-synth.js`
   - Tone.js overhead: Multiple nodes, filters
   - Optimization: Simplify filter chain, reduce oscillators, direct audio routing

5. **UI Update Blocking**
   - Location: `js/managers/ui-manager.js`
   - Risk: DOM updates blocking audio thread
   - Optimization: Throttle updates to 60Hz, use requestAnimationFrame

### Profiling Workflow

```bash
# 1. Start dev server
npm start

# 2. Open Chrome DevTools → Performance
# 3. Start recording
# 4. Click "Start Playing" in app
# 5. Hum/sing for 10 seconds
# 6. Stop recording
# 7. Analyze:
#    - Look for long tasks (>50ms yellow blocks)
#    - Check audio thread CPU usage
#    - Identify bottleneck functions
```

### Quick Wins (Easy Optimizations)

1. **Verify Worklet Mode**
   ```javascript
   // In console
   console.log(window.container.get('audioIO').mode)
   // Should be 'worklet', not 'script-processor'
   ```

2. **Reduce FFT Size**
   ```javascript
   // js/features/spectral-features.js
   // Change FFT_SIZE from 2048 to 1024 or 512
   ```

3. **Increase Feature Extraction Interval**
   ```javascript
   // js/expressive-features.js
   // Change extraction interval from every frame to every 2-3 frames
   ```

4. **Disable Non-Critical Features** (temporary test)
   ```javascript
   // Comment out in js/expressive-features.js:
   // - Spectral centroid
   // - Spectral rolloff
   // - Zero crossing rate
   // Keep only: volume, pitch, clarity
   ```

### Measurement Strategy

```javascript
// Add to js/main.js for detailed profiling
class LatencyProfiler {
  constructor() {
    this.stages = {
      capture: [],
      detection: [],
      extraction: [],
      synthesis: [],
      output: []
    };
  }

  measureStage(stage, fn) {
    const start = performance.now();
    const result = fn();
    const duration = performance.now() - start;
    this.stages[stage].push(duration);
    return result;
  }

  getReport() {
    const report = {};
    for (const [stage, times] of Object.entries(this.stages)) {
      times.sort((a, b) => a - b);
      report[stage] = {
        avg: times.reduce((a, b) => a + b, 0) / times.length,
        p50: times[Math.floor(times.length * 0.5)],
        p95: times[Math.floor(times.length * 0.95)],
        p99: times[Math.floor(times.length * 0.99)]
      };
    }
    return report;
  }
}

// Usage
window.profiler = new LatencyProfiler();
```

## Resources

- MDN Web Audio API: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API
- AudioWorklet spec: https://webaudio.github.io/web-audio-api/#AudioWorklet
- Performance best practices: https://developer.chrome.com/blog/audio-worklet-design-pattern/
- YIN algorithm paper: http://audition.ens.fr/adc/pdf/2002_JASA_YIN.pdf
- Real-time audio in JS: https://www.html5rocks.com/en/tutorials/webaudio/intro/
