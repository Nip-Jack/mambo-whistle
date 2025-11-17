---
name: audio-ui-integration
description: Build responsive, real-time audio UI without blocking audio processing
category: audio-frontend
tags: [web-audio, ui, canvas, visualization, real-time]
version: 1.0.0
---

# Audio UI Integration Skill

## Purpose
Create smooth, responsive UI for real-time audio applications without interfering with audio processing performance.

## When to Use
- Building audio visualizations (waveforms, spectrums, meters)
- Creating real-time audio parameter controls
- Displaying audio analysis results
- Synchronizing audio and visual feedback

## Core Principles

### 1. Separate Audio and UI Threads
- Audio processing: AudioWorklet (audio thread)
- UI updates: requestAnimationFrame (main thread)
- Communication: MessagePort (async, non-blocking)

### 2. Throttle UI Updates
- Audio runs at 44.1kHz or 48kHz
- UI updates at 60Hz (16.67ms) max
- Use requestAnimationFrame, not setInterval
- Batch multiple values per frame

### 3. Use Canvas for Performance
- Avoid DOM updates for real-time data
- Use OffscreenCanvas when possible
- Pre-render static elements
- Use requestAnimationFrame for smooth animation

### 4. Non-Blocking Communication
- Never use synchronous message passing
- Prefer SharedArrayBuffer for high-frequency data
- Use Atomics for lock-free coordination
- Keep messages small and focused

## Implementation Patterns

### Pattern 1: Audio Visualization
```javascript
class AudioVisualizer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.animationId = null;
    this.dataBuffer = new Float32Array(128);
  }

  start() {
    const render = () => {
      this.draw();
      this.animationId = requestAnimationFrame(render);
    };
    render();
  }

  updateData(newData) {
    // Called from audio callback (via message)
    this.dataBuffer.set(newData);
  }

  draw() {
    // 60Hz UI update
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw waveform or spectrum
    const width = this.canvas.width;
    const height = this.canvas.height;
    const step = width / this.dataBuffer.length;

    ctx.beginPath();
    ctx.strokeStyle = '#3b82f6'; // Blue
    ctx.lineWidth = 2;

    for (let i = 0; i < this.dataBuffer.length; i++) {
      const x = i * step;
      const y = (this.dataBuffer[i] + 1) * height / 2; // Normalize -1 to 1

      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }

    ctx.stroke();
  }

  stop() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }
}
```

### Pattern 2: Parameter Control with Smoothing
```javascript
class AudioParameter {
  constructor(audioNode, paramName) {
    this.param = audioNode[paramName];
    this.targetValue = this.param.value;
  }

  setValue(value, rampTime = 0.05) {
    // Smooth parameter changes to avoid clicks/pops
    this.targetValue = value;
    this.param.linearRampToValueAtTime(
      value,
      audioContext.currentTime + rampTime
    );
  }

  setValueImmediate(value) {
    // For non-audio-rate params
    this.param.setValueAtTime(value, audioContext.currentTime);
  }

  // UI calls this on slider change
  onSliderChange(event) {
    const value = parseFloat(event.target.value);
    this.setValue(value);
  }

  // UI calls this on wheel scroll (fine control)
  onWheelChange(event) {
    event.preventDefault();
    const delta = -event.deltaY * 0.01; // Invert and scale
    const newValue = Math.max(this.param.minValue,
                              Math.min(this.param.maxValue,
                                       this.targetValue + delta));
    this.setValue(newValue);
  }
}
```

### Pattern 3: Event-Driven UI Updates
```javascript
class UIManager extends EventTarget {
  constructor() {
    super();
    this.throttledUpdates = new Map();
  }

  // Emit audio events (called from audio callback)
  updateNote(note, frequency, clarity) {
    this.dispatchEvent(new CustomEvent('noteChange', {
      detail: { note, frequency, clarity }
    }));
  }

  updateLatency(latency) {
    // Throttle to 2Hz (every 500ms)
    this.throttle('latency', () => {
      this.dispatchEvent(new CustomEvent('latencyChange', {
        detail: { latency }
      }));
    }, 500);
  }

  throttle(key, fn, delay) {
    if (!this.throttledUpdates.has(key)) {
      fn();
      this.throttledUpdates.set(key, true);
      setTimeout(() => this.throttledUpdates.delete(key), delay);
    }
  }
}

// UI components listen for events
const uiManager = new UIManager();

uiManager.addEventListener('noteChange', (e) => {
  const { note, frequency, clarity } = e.detail;

  // Update DOM (throttled by rAF)
  requestAnimationFrame(() => {
    noteDisplay.textContent = note;
    freqDisplay.textContent = `${frequency.toFixed(1)} Hz`;
    clarityMeter.style.width = `${clarity * 100}%`;
  });
});

uiManager.addEventListener('latencyChange', (e) => {
  const { latency } = e.detail;

  // Update with color coding
  latencyDisplay.textContent = `${latency.toFixed(0)} ms`;
  latencyDisplay.className = latency < 50 ? 'low' :
                             latency < 100 ? 'medium' : 'high';
});
```

### Pattern 4: Circular Buffer for Pitch History
```javascript
class PitchHistory {
  constructor(size = 600) { // 10 seconds at 60Hz
    this.buffer = new Float32Array(size);
    this.index = 0;
    this.size = size;
  }

  add(pitch) {
    this.buffer[this.index] = pitch;
    this.index = (this.index + 1) % this.size;
  }

  getAll() {
    // Return in chronological order
    const result = new Float32Array(this.size);
    for (let i = 0; i < this.size; i++) {
      result[i] = this.buffer[(this.index + i) % this.size];
    }
    return result;
  }

  clear() {
    this.buffer.fill(0);
    this.index = 0;
  }
}

// Usage with canvas
class PitchCurveVisualizer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.history = new PitchHistory(600);
    this.animationId = null;
  }

  addPitch(pitch) {
    this.history.add(pitch);
  }

  start() {
    const render = () => {
      this.draw();
      this.animationId = requestAnimationFrame(render);
    };
    render();
  }

  draw() {
    const ctx = this.ctx;
    const width = this.canvas.width;
    const height = this.canvas.height;

    // Clear
    ctx.clearRect(0, 0, width, height);

    // Draw pitch curve
    const pitches = this.history.getAll();
    const step = width / pitches.length;

    ctx.beginPath();
    ctx.strokeStyle = '#8b5cf6'; // Purple
    ctx.lineWidth = 2;

    for (let i = 0; i < pitches.length; i++) {
      const x = i * step;
      // Map MIDI note (0-127) to canvas height
      const y = height - (pitches[i] / 127 * height);

      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }

    ctx.stroke();
  }
}
```

## Performance Checklist

- [ ] UI updates use requestAnimationFrame
- [ ] Update frequency ≤ 60Hz
- [ ] Canvas used for visualizations (not DOM)
- [ ] Audio thread never blocks on UI
- [ ] Parameter changes use audio-rate automation
- [ ] No synchronous message passing
- [ ] Shared buffers for high-frequency data

## Common Pitfalls

1. **Updating DOM too frequently**: Throttle to 60Hz
   - ❌ `audioWorklet.onmessage = () => updateDOM()`
   - ✅ `requestAnimationFrame(() => updateDOM())`

2. **Blocking audio thread**: Use async messages
   - ❌ `const result = Atomics.wait(...)`
   - ✅ `audioWorklet.port.postMessage(...)`

3. **Heavy computation in rAF**: Defer to idle callback
   - ❌ Complex calculations in every rAF call
   - ✅ `requestIdleCallback(() => heavyWork())`

4. **Creating objects in loops**: Pre-allocate buffers
   - ❌ `const data = new Float32Array(128)` (in draw loop)
   - ✅ `this.dataBuffer = new Float32Array(128)` (in constructor)

5. **Not using audio-rate automation**: Causes zipper noise
   - ❌ `gainNode.gain.value = newValue`
   - ✅ `gainNode.gain.linearRampToValueAtTime(newValue, time)`

## Kazoo Proto Specific Implementation

### Current Note Display (js/managers/ui-manager.js)

**Current Issues**:
- Updates on every pitch detection (potentially >60Hz)
- No throttling or batching
- Direct DOM manipulation

**Optimization**:
```javascript
class UIManager extends EventTarget {
  constructor() {
    super();
    this.pendingNoteUpdate = null;
    this.noteUpdateScheduled = false;
  }

  updateNote(note, frequency, clarity) {
    // Buffer the latest value
    this.pendingNoteUpdate = { note, frequency, clarity };

    // Schedule update if not already scheduled
    if (!this.noteUpdateScheduled) {
      this.noteUpdateScheduled = true;
      requestAnimationFrame(() => {
        if (this.pendingNoteUpdate) {
          this._flushNoteUpdate();
        }
        this.noteUpdateScheduled = false;
      });
    }
  }

  _flushNoteUpdate() {
    const { note, frequency, clarity } = this.pendingNoteUpdate;

    // Update DOM elements
    document.getElementById('currentNote').textContent = note;
    document.getElementById('currentFreq').textContent = `${frequency.toFixed(1)} Hz`;

    // Update clarity meter
    const clarityPercent = Math.round(clarity * 100);
    document.getElementById('confidence').textContent = `${clarityPercent}%`;

    this.pendingNoteUpdate = null;
  }
}
```

### Pitch Canvas (index.html)

**Current Issues**:
- Canvas exists but may not be optimized
- No circular buffer pattern
- Potential redraw inefficiency

**Optimization**: Use Pattern 4 (Circular Buffer) above

### Status Bar (Latency/Confidence)

**Current Issues**:
- Updates too frequently
- No color coding
- No debouncing

**Optimization**:
```javascript
class StatusBarManager {
  constructor() {
    this.latencyHistory = [];
    this.updateInterval = 500; // 2Hz
    this.lastUpdate = 0;
  }

  updateLatency(latency) {
    this.latencyHistory.push(latency);
    if (this.latencyHistory.length > 20) {
      this.latencyHistory.shift();
    }

    const now = performance.now();
    if (now - this.lastUpdate >= this.updateInterval) {
      this._flushLatencyUpdate();
      this.lastUpdate = now;
    }
  }

  _flushLatencyUpdate() {
    // Calculate average latency
    const avg = this.latencyHistory.reduce((a, b) => a + b, 0) / this.latencyHistory.length;

    // Update with color coding
    const latencyEl = document.getElementById('latency');
    latencyEl.textContent = `${avg.toFixed(0)} ms`;

    // Color code: green < 50ms, yellow < 100ms, red >= 100ms
    latencyEl.className = avg < 50 ? 'text-green-600' :
                          avg < 100 ? 'text-yellow-600' : 'text-red-600';
  }
}
```

## Testing Checklist

### Visual Smoothness
- [ ] Note display updates smoothly (no flicker)
- [ ] Pitch curve is smooth (no jitter)
- [ ] Status values update without lag
- [ ] No visual tearing or artifacts

### Performance
- [ ] UI updates capped at 60fps
- [ ] No frame drops during audio playback
- [ ] CPU usage reasonable (check DevTools Performance)
- [ ] Memory stable (no leaks after 5 min playback)

### Responsiveness
- [ ] Parameter changes feel immediate (<100ms perceived)
- [ ] No input lag on sliders/controls
- [ ] UI remains responsive during audio processing
- [ ] Browser doesn't freeze or stutter

## Resources

- requestAnimationFrame: https://developer.mozilla.org/en-US/docs/Web/API/window/requestAnimationFrame
- Canvas performance: https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas
- SharedArrayBuffer: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer
- AudioParam automation: https://developer.mozilla.org/en-US/docs/Web/API/AudioParam
- Web Audio best practices: https://www.html5rocks.com/en/tutorials/webaudio/intro/
