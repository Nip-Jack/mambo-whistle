---
name: "Web Audio Performance Analyzer"
description: "Diagnose and optimize Web Audio API latency issues; use when debugging audio performance or latency exceeds 50ms target"
---

# Web Audio Performance Analyzer

Specialized skill for optimizing real-time Web Audio API applications with focus on end-to-end latency reduction.

## When to Use

Activate this skill when:
- User reports audio latency or performance issues
- Latency measurements exceed 50ms target
- Debugging audio pipeline bottlenecks
- Optimizing AudioWorklet or ScriptProcessor implementations
- Investigating audio glitches or distortion

## Core Instructions

### 1. Initial Diagnostics

Always start with these checks:

```javascript
// Check AudioWorklet mode (target: 'worklet')
window.container.get('audioIO').mode

// Measure end-to-end latency (target: <50ms)
window.app.getLatencyStats()

// List all services
window.container.getServiceNames()
```

**Critical**: ScriptProcessor fallback uses 2048 buffer = 46ms base latency. Ensure Worklet mode is active.

### 2. Performance Bottleneck Priority

Investigate bottlenecks in this order:

1. **AudioWorklet Fallback** (2048 buffer = 46ms)
   - Location: `js/audio-io.js`
   - Solution: Ensure HTTPS/localhost for Worklet support
   - Verify: `audioIO.mode === 'worklet'`

2. **FFT Computation** (SpectralFeatures)
   - Location: `js/features/spectral-features.js`
   - Optimization: Reduce FFT size or computation interval
   - Measurement: Profile FFT execution time

3. **Feature Extraction Pipeline**
   - Location: `js/expressive-features.js`
   - Optimization: Disable non-critical features
   - Consider: Conditional feature extraction based on mode

4. **Synthesizer Complexity**
   - Location: `js/continuous-synth.js`
   - Optimization: Reduce filter complexity, envelope parameters
   - Trade-off: Sound quality vs latency

### 3. Measurement Strategy

```javascript
// Get detailed statistics (focus on p95 for realistic worst-case)
const stats = window.app.getLatencyStats()
console.table({
  'Min': stats.min,
  'P50 (Median)': stats.p50,
  'P95': stats.p95,
  'Max': stats.max,
  'Average': stats.avg
})
```

**Note**:
- `performanceMonitor` measures processing time only
- `getLatencyStats()` measures end-to-end (capture → output)
- Need 100+ samples for accurate statistics

### 4. Architecture Constraints

**Dependency Injection**:
- All services accessed via: `window.container.get('serviceName')`
- Only global variables: `window.app` and `window.container`
- Check registration: `window.container.has('serviceName')`

**Configuration**:
- Single source of truth: `configManager.load()`
- Presets location: `js/config/instrument-presets.js`
- Changes require page reload

**Testing**:
- ALWAYS run `npm test` before/after changes
- Tests must be able to fail
- No predetermined success tests
- Location: `tests/unit/` or `tests/integration/`

### 5. Common Pitfalls

**AudioWorklet Issues**:
- May fall back to ScriptProcessor silently
- Check mode before debugging latency
- Worklet requires HTTPS or localhost

**Configuration Not Loading**:
- Must call `configManager.load()` before accessing
- Config is singleton, loaded once at startup
- Changes require page reload

**Service Not Found**:
- Service must be registered in AppContainer
- Registration location: `js/main.js` lines 735-843
- Verify: `window.container.has('serviceName')`

### 6. Optimization Workflow

1. **Baseline Measurement**
   ```bash
   npm start
   # In browser console:
   window.app.getLatencyStats()
   ```

2. **Identify Bottleneck**
   - Use Chrome DevTools Performance profiler
   - Focus on audio thread (AudioWorklet) timing
   - Check `about://tracing` for detailed Web Audio metrics

3. **Apply Targeted Fix**
   - Make ONE change at a time
   - Write test for the change
   - Measure impact on latency

4. **Verify Improvement**
   ```javascript
   // Before optimization
   const before = window.app.getLatencyStats()

   // After optimization
   const after = window.app.getLatencyStats()

   console.log(`Latency improvement: ${before.p95 - after.p95}ms`)
   ```

5. **Commit Focused Change**
   ```bash
   npm test  # Ensure tests pass
   git add .
   git commit -m "perf: Reduce FFT size from 2048 to 1024 (-15ms latency)"
   ```

## Performance Targets

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Latency | < 50ms | 180ms | 3.6x over target |
| Test Coverage | 40% | ~5% | Needs work |
| Console Logs | < 50 | 286 | Too many |

**Priority**: Performance > Architecture > Documentation

## Quick Reference Commands

```bash
# Development
npm start                       # Start dev server (localhost:3000)
npm test                        # Run tests
npm run test:watch              # Watch mode
npm run test:coverage           # Coverage report

# Browser Console (after starting audio)
window.app.getLatencyStats()    # Latency measurements
window.container.get('audioIO').mode  # Check worklet/script-processor
window.container.getServiceNames()    # List services
```

## Anti-Patterns to AVOID

1. **Over-Documentation**: Code > Docs. Only document if necessary.
2. **Fake Tests**: Every test must be able to fail.
3. **Mocking Audio Pipeline**: Test real implementations when possible.
4. **Premature Optimization**: Measure first, optimize second.
5. **Multiple Changes**: One focused change per commit.

## Resources

- Chrome DevTools: Performance profiler, Memory profiler
- Web Audio Panel: `chrome://webaudio-internals`
- Tracing: `about://tracing` (Web Audio category)
- Project docs: `docs/guides/troubleshooting.md`
- Cleanup plan: `docs/CLEANUP_PLAN.md`
