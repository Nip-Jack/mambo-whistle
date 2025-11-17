# Claude Code Workflow Setup - Kazoo Proto Web

**Created**: 2025-11-17
**Purpose**: Complete workflow setup with Skills and MCP for frontend + audio optimization
**Priority**: Frontend excellence → Audio robustness → Low latency

---

## Current Status Analysis

### ✅ Branch Progress (feature/001-ui-modernization)
- **Completed**: Phase 1-2 (Hero + Navigation + Instrument cards)
- **Pending**: Phase 3-4 (Controls + Visualization)
- **Known Issues**:
  - Missing frontend UI polish (Phase 3-4 incomplete)
  - Audio processing needs robustness improvements
  - Latency measurement fixed but optimization needed

### 🎯 Project Goals
1. **Frontend Excellence**: Modern, responsive, accessible UI (Priority #1)
2. **Audio Robustness**: Handle fast pitch/timbre/rhythm changes reliably
3. **Audio Richness**: More expressive, pleasant, fun, adjustable sound
4. **Ultra-Low Latency**: <50ms target (currently 180ms)
5. **Shortest Processing Chain**: Minimize overhead everywhere

---

## Installed Skills (Current)

Located in `.claude/skills/`:

### Development Standards
- ✅ `kazoo-development-standards` - Project-specific best practices
- ✅ `web-audio-performance` - Audio latency optimization

### Code Quality
- ✅ `code-review-excellence` - PR review patterns
- ✅ `debugging-strategies` - Systematic debugging
- ✅ `error-handling-patterns` - Resilient error handling

### Testing
- ✅ `javascript-testing-patterns` - Jest/Vitest/Testing Library
- ✅ `e2e-testing-patterns` - Playwright/Cypress

### JavaScript/TypeScript
- ✅ `modern-javascript-patterns` - ES6+ best practices
- ✅ `typescript-advanced-types` - Advanced type safety
- ✅ `nodejs-backend-patterns` - Node.js patterns (future backend)

---

## Recommended Skills to Add

### 🎨 Frontend Design (High Priority)

#### 1. frontend-design (Official Anthropic)
```bash
# Installation
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/anthropics/skills.git temp-skills
mv temp-skills/frontend-design ./frontend-design
rm -rf temp-skills
```
**Use for**: Creating production-grade frontend interfaces with high design quality

#### 2. artifacts-builder (Official Anthropic)
```bash
# Already in official skills repo
cd ~/.claude/skills
git clone https://github.com/anthropics/skills.git temp-skills
mv temp-skills/artifacts-builder ./artifacts-builder
rm -rf temp-skills
```
**Use for**: Building complex UI with React, Tailwind CSS, shadcn/ui components

#### 3. canvas-design (Official Anthropic)
```bash
cd ~/.claude/skills
git clone https://github.com/anthropics/skills.git temp-skills
mv temp-skills/canvas-design ./canvas-design
rm -rf temp-skills
```
**Use for**: Designing visual elements, audio visualizations, waveform displays

### 🎵 Audio Processing (Custom - Create Below)

#### 4. web-audio-optimization (Custom Skill)
Create at `.claude/skills/web-audio-optimization/SKILL.md`
- Optimize Web Audio API processing chains
- Reduce AudioWorklet latency
- Profiling and performance measurement
- DSP algorithm optimization

#### 5. audio-ui-integration (Custom Skill)
Create at `.claude/skills/audio-ui-integration/SKILL.md`
- Real-time UI updates without blocking audio
- Canvas-based audio visualization
- Responsive audio parameter controls
- Audio-visual synchronization

### 🚀 Performance (High Priority)

#### 6. frontend-performance-optimization (Community)
Search at skillsmp.com for:
- Code splitting and lazy loading
- Bundle optimization
- Core Web Vitals optimization
- Measurement and monitoring

---

## Recommended MCP Servers

### 🎤 Audio Processing MCP

#### 1. audio-mcp-server
```bash
# Installation (requires Python)
pip install mcp-audio-server
```
**Features**:
- Audio input/output via microphone/speakers
- Real-time audio stream processing
- Uses sounddevice and soundfile

**Use cases**:
- Testing audio processing pipelines
- Debugging microphone input issues
- Analyzing audio latency

#### 2. voice-mcp (Optional - for future voice control)
```bash
npm install -g voice-mcp
```
**Features**:
- Voice interaction with Claude
- OpenAI Whisper integration
- Local speech-to-text (Whisper.cpp)
- Local text-to-speech (Kokoro)

**Use cases**:
- Voice-controlled UI testing
- Accessibility features
- Future voice command support

### 🎨 Frontend Development MCP

#### 3. browser-automation-mcp (Playwright-based)
```bash
npm install -g @playwright/mcp
```
**Features**:
- Automated browser testing
- Screenshot capture
- Visual regression testing
- Performance profiling

**Use cases**:
- Automated UI testing
- Visual QA for design changes
- Latency measurement automation

---

## Custom Skills to Create

### Skill 1: web-audio-optimization

**File**: `.claude/skills/web-audio-optimization/SKILL.md`

```markdown
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

## Resources

- MDN Web Audio API: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API
- AudioWorklet spec: https://webaudio.github.io/web-audio-api/#AudioWorklet
- Performance best practices: https://developer.chrome.com/blog/audio-worklet-design-pattern/
```

---

### Skill 2: audio-ui-integration

**File**: `.claude/skills/audio-ui-integration/SKILL.md`

```markdown
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
    // ... draw logic using this.dataBuffer
  }
}
```

### Pattern 2: Parameter Control
```javascript
class AudioParameter {
  constructor(audioNode, paramName) {
    this.param = audioNode[paramName];
    this.targetValue = this.param.value;
  }

  setValue(value, rampTime = 0.05) {
    // Smooth parameter changes
    this.targetValue = value;
    this.param.linearRampToValueAtTime(
      value,
      audioContext.currentTime + rampTime
    );
  }

  // UI calls this on slider change
  onSliderChange(event) {
    this.setValue(parseFloat(event.target.value));
  }
}
```

### Pattern 3: Event-Driven UI Updates
```javascript
class UIManager extends EventTarget {
  updateNote(note, frequency) {
    // Emit event instead of direct DOM manipulation
    this.dispatchEvent(new CustomEvent('noteChange', {
      detail: { note, frequency }
    }));
  }
}

// UI components listen for events
uiManager.addEventListener('noteChange', (e) => {
  noteDisplay.textContent = e.detail.note;
  freqDisplay.textContent = `${e.detail.frequency.toFixed(1)} Hz`;
});
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
2. **Blocking audio thread**: Use async messages
3. **Heavy computation in rAF**: Defer to idle callback
4. **Creating objects in loops**: Pre-allocate buffers
5. **Not using audio-rate automation**: Causes zipper noise

## Kazoo Proto Specific

### Current Note Display
- Update frequency: 60Hz max (currently uncapped)
- Use transition-free updates (no CSS animations on values)
- Batch note + frequency + confidence updates

### Pitch Canvas
- Buffer size: 600 points (10 seconds at 60Hz)
- Use circular buffer for efficient updates
- Clear and redraw each frame

### Status Bar
- Update latency/confidence at 2Hz (every 500ms)
- Use color-coded badges (green/yellow/red)
- Debounce status changes (avoid flicker)

## Resources

- requestAnimationFrame: https://developer.mozilla.org/en-US/docs/Web/API/window/requestAnimationFrame
- Canvas performance: https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas
- SharedArrayBuffer: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer
```

---

## Workflow Setup Steps

### Step 1: Install Missing Frontend Skills (15 min)

```bash
# Navigate to skills directory
cd ~/.claude/skills

# Clone official Anthropic skills repo
git clone https://github.com/anthropics/skills.git anthropic-skills

# Copy frontend-design skill
cp -r anthropic-skills/frontend-design ./frontend-design

# Copy artifacts-builder skill
cp -r anthropic-skills/artifacts-builder ./artifacts-builder

# Copy canvas-design skill
cp -r anthropic-skills/canvas-design ./canvas-design

# Clean up temp repo
rm -rf anthropic-skills

# Verify installation
ls -la ~/.claude/skills/
```

### Step 2: Create Custom Audio Skills (10 min)

```bash
# Create web-audio-optimization skill
mkdir -p .claude/skills/web-audio-optimization
# (Copy SKILL.md content from above)

# Create audio-ui-integration skill
mkdir -p .claude/skills/audio-ui-integration
# (Copy SKILL.md content from above)
```

### Step 3: (Optional) Install MCP Servers (30 min)

```bash
# Install audio MCP server (Python required)
pip install mcp-audio-server

# Install browser automation MCP (Node.js)
npm install -g @playwright/mcp

# Verify installation
mcp list
```

### Step 4: Update Project Skills List

Add to `.claude/skills/kazoo-development-standards/SKILL.md`:

```markdown
## Available Project Skills

- web-audio-optimization - Ultra-low latency audio processing
- audio-ui-integration - Real-time audio UI patterns
- frontend-design - Production-grade interface design
- artifacts-builder - Complex UI components
- canvas-design - Audio visualizations
```

---

## Using Skills in Workflow

### For Frontend Work
```bash
# Invoke frontend-design skill
/skill frontend-design

# Example prompt:
"Using frontend-design skill, modernize the instrument selection cards
with better hover states, focus indicators, and responsive layout."
```

### For Audio Optimization
```bash
# Invoke web-audio-optimization skill
/skill web-audio-optimization

# Example prompt:
"Using web-audio-optimization skill, analyze the current audio pipeline
and identify latency bottlenecks. Target: <50ms end-to-end."
```

### For Visualization Work
```bash
# Invoke canvas-design + audio-ui-integration
/skill canvas-design
/skill audio-ui-integration

# Example prompt:
"Using canvas-design and audio-ui-integration skills, create a smooth
pitch visualization that updates at 60Hz without blocking audio."
```

---

## Next Steps

### Immediate (This Session)
1. ✅ Install frontend-design, artifacts-builder, canvas-design skills
2. ✅ Create web-audio-optimization and audio-ui-integration custom skills
3. ⏳ Complete UI Phase 3-4 (Controls + Visualization)
4. ⏳ Test all UI features in browser

### Short Term (Next 1-2 Sessions)
1. Audit audio processing robustness (handle fast changes)
2. Enhance audio expressiveness (timbre, dynamics)
3. Optimize latency (180ms → <100ms first milestone)
4. Implement audio parameter controls

### Medium Term (Next 3-5 Sessions)
1. Add advanced visualizations (spectrum, waveform)
2. Implement preset system (save/load instrument configs)
3. Add audio effects chain (reverb, delay, etc.)
4. Optimize to <50ms latency target

---

## Monitoring Progress

### Key Metrics Dashboard

```javascript
// Run in browser console after starting audio
const metrics = {
  latency: window.app.getLatencyStats(),
  audioMode: window.container.get('audioIO').mode,
  bufferSize: audioContext.baseLatency * audioContext.sampleRate,
  cpu: performance.memory ? (performance.memory.usedJSHeapSize / 1024 / 1024).toFixed(2) + ' MB' : 'N/A'
};
console.table(metrics);
```

### Quality Gates
- [ ] UI feels modern and responsive (subjective)
- [ ] Audio latency p95 < 200ms (current), < 100ms (v0.4.0), < 50ms (v1.0)
- [ ] No audio glitches or dropouts during testing
- [ ] Smooth visualizations at 60fps
- [ ] All features work on Chrome, Firefox, Safari

---

## Troubleshooting

### Skills Not Loading
```bash
# Check skills directory structure
ls -la ~/.claude/skills/
ls -la .claude/skills/

# Verify SKILL.md format (YAML frontmatter required)
head -20 ~/.claude/skills/frontend-design/SKILL.md
```

### MCP Connection Issues
```bash
# Check MCP server status
mcp status

# Restart MCP server
mcp restart

# Check logs
mcp logs
```

### Audio Performance Degradation
```bash
# Check AudioWorklet mode
window.container.get('audioIO').mode // Should be 'worklet', not 'script-processor'

# Measure baseline
window.app.getLatencyStats()

# Profile audio processing
# Chrome DevTools → Performance → Record → Start Audio → Stop after 10s
```

---

**Last Updated**: 2025-11-17
**Maintainer**: Claude Code + Ziming Wang
**Status**: Active Development
