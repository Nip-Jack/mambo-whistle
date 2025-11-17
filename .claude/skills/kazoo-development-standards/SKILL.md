---
name: "Kazoo Project Standards"
description: "Enforce Kazoo Proto Web project standards and best practices; use for all development tasks in this project"
---

# Kazoo Project Development Standards

Project-specific development standards for Kazoo Proto Web voice-to-instrument system.

## When to Use

Activate this skill when:
- Starting any development task in Kazoo Proto Web
- Reviewing or modifying existing code
- Adding new features or fixing bugs
- Writing tests or documentation

## Core Principles

**Project Goal**: End-to-end latency < 50ms (currently 180ms - 3.6x over target)

**Priority Order**:
1. Performance > Architecture > Documentation
2. Working code > Beautiful code
3. Real tests > Documentation
4. Code quality matters, but working code matters more

## Architecture Rules (Must Follow)

### 1. Dependency Injection (STRICT)

**Required Pattern**:
```javascript
// Register service in AppContainer (js/main.js lines 735-843)
container.register('serviceName', () => {
  return new ServiceClass(dependencies);
}, { singleton: true });

// Access service
const service = window.container.get('serviceName');

// Check if service exists
if (window.container.has('serviceName')) {
  // use service
}
```

**Prohibited**:
- Global variables (except `window.app` and `window.container`)
- Direct instantiation of services
- Singleton patterns outside AppContainer

### 2. Configuration Management

**Single Source of Truth**:
```javascript
// Load configuration once at startup
const config = configManager.load();

// Extend presets in: js/config/instrument-presets.js
// Never hardcode configuration values
```

**Rules**:
- All config in `js/config/app-config.js`
- Instrument presets in `js/config/instrument-presets.js`
- Changes require page reload
- No configuration in component code

### 3. UI Updates (Event-Driven Only)

**Required Pattern**:
```javascript
// Use UIManager events
uiManager.emit('eventName', data);

// Listen to events
uiManager.on('eventName', (data) => {
  // Update UI
});
```

**Prohibited**:
- Direct DOM manipulation in business logic
- Imperative UI updates
- Bypassing UIManager for UI changes

### 4. Testing Requirements (CRITICAL)

**Workflow**:
```bash
# ALWAYS before making changes
npm test

# Write test that FAILS
# Implement feature to make test PASS
# Verify test passes

# ALWAYS before committing
npm test
```

**Test Quality Rules**:
- Every test MUST be able to fail
- No predetermined success tests
- No fake tests with mocked results
- Test real implementations when possible
- Location: `tests/unit/` or `tests/integration/`
- Use Vitest only (no custom frameworks)

**Coverage Target**: 40% (currently ~5%)

### 5. Audio Pipeline Architecture

```
Microphone → AudioWorklet → YIN Detection → Feature Extraction → Synthesizer → Output
             (128 samples)    (pitch, clarity)  (volume, timbre)   (Tone.js)
```

**Key Files**:
- `js/main.js` - KazooApp main application
- `js/audio-io.js` - Audio I/O abstraction
- `js/pitch-detector.js` - YIN algorithm wrapper
- `js/pitch-worklet.js` - AudioWorklet processor
- `js/continuous-synth.js` - Continuous mode synth
- `js/expressive-features.js` - Feature extraction
- `js/performance.js` - Performance monitoring

## Anti-Patterns (AVOID)

### 1. Zombie Code
**Problem**: Leaving old code when replacing functionality

**Bad**:
```javascript
// Old implementation (commented out)
// function oldWay() { ... }

// New implementation
function newWay() { ... }
```

**Good**:
```javascript
// New implementation (old code DELETED)
function newWay() { ... }
```

**Rule**: DELETE old code in SAME commit that adds replacement

### 2. Untested Changes
**Problem**: Adding code without verifying it works

**Bad**:
```javascript
// Add feature without testing in browser
container.register('newService', ...);
// Commit without verification
```

**Good**:
```javascript
// Add feature
container.register('newService', ...);
// npm start
// Test in browser console: window.container.get('newService')
// Verify functionality works
// npm test
// Commit with confidence
```

**Rule**: Test EVERY change in browser before committing

### 3. Partial Completion
**Problem**: Marking tasks done when subtasks remain

**Bad**:
```markdown
- [x] Update audio pipeline
  - [x] Modify pitch detection
  - [ ] Modify synthesizer (skipped - will do later)
```

**Good**:
```markdown
- [x] Update pitch detection in audio pipeline
- [ ] Update synthesizer in audio pipeline (deferred - reason: X)
```

**Rule**: Complete ALL parts of task or explicitly defer with justification

### 4. Over-Documentation
**Problem**: Writing docs instead of fixing code

**Bad**:
```bash
# Create detailed performance analysis document
# Write optimization plan in docs/
# Create stage summaries
# Write completion reports
```

**Good**:
```bash
# Measure current latency
# Apply one optimization
# Measure new latency
# Commit if improved
```

**Rule**: Code first, docs only if necessary

## Documentation Standards

### Root Directory (3 files ONLY)
1. `README.md` - User guide (< 300 lines)
2. `PROJECT_STATUS.md` - Current state (< 250 lines)
3. `CLAUDE.md` - AI agent guide (< 200 lines)

### Prohibited
- Creating `docs/phase*/` or `docs/step*/` directories
- Writing "completion reports" or "stage summaries"
- Using emoji in documentation
- Execution plans > 200 lines

### Update Principles
1. Code > Docs - Only write if absolutely necessary
2. README first - User-facing information
3. PROJECT_STATUS second - Developer information
4. Long-term plans → GitHub issues, not docs

## Commit Guidelines

**Format**:
```bash
git commit -m "type: Description of change (impact)"
```

**Types**:
- `feat:` - New feature
- `fix:` - Bug fix
- `perf:` - Performance improvement (include latency impact)
- `test:` - Add/update tests
- `refactor:` - Code restructuring
- `docs:` - Documentation only

**Examples**:
```bash
git commit -m "perf: Reduce FFT size to 1024 (-15ms latency)"
git commit -m "fix: Prevent double initialization in audio-io"
git commit -m "test: Add unit tests for pitch detection (15% coverage)"
```

**Rules**:
- One logical change per commit
- Be brutally honest about what was NOT done
- Never claim completion when work is incomplete

## Development Workflow

### Before Starting Work
```bash
npm test                        # Ensure baseline works
```

```javascript
// In browser console
window.app.getLatencyStats()    // Check current latency
window.container.get('audioIO').mode  // Verify Worklet mode
```

### During Development
1. Write failing test first
2. Implement minimal code to pass test
3. Test in browser (`npm start`)
4. Measure performance impact
5. One commit per logical change

### Before Committing
```bash
npm test                        # Tests must pass
```

```javascript
// Verify no regression
window.app.getLatencyStats()
```

```bash
git add .
git commit -m "type: description (impact)"
```

## Quick Reference

### Common Commands
```bash
npm start                       # Dev server (localhost:3000)
npm test                        # Run tests
npm run test:watch              # Watch mode
npm run test:coverage           # Coverage report
```

### Browser Console
```javascript
window.app.getLatencyStats()    # Latency stats (min/max/avg/p50/p95)
window.container.get('audioIO').mode  # Check worklet/script-processor
window.container.getServiceNames()    # List all services
window.container.has('serviceName')   # Check if service exists
```

### Service Registration Locations
- `js/main.js` lines 735-843 - All service registrations
- `js/core/app-container.js` - DI container implementation

## Performance Targets

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Latency | < 50ms | 180ms | 3.6x over |
| Test Coverage | 40% | ~5% | Needs work |
| Global Variables | 0 | 2 | Acceptable |
| Console Logs | < 50 | 286 | Too many |

## Remember

**This project's goal is "working with low latency", not "looks professional".**

**Fix bugs > Write docs**
