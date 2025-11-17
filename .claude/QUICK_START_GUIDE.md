# Quick Start Guide - Claude Code Workflow for Kazoo Proto

**Last Updated**: 2025-11-17
**Reading Time**: 5 minutes

---

## TL;DR - What Was Set Up

✅ **12 Skills Installed** (10 existing + 2 new custom skills)
✅ **Complete Workflow Documentation** (`.claude/WORKFLOW_SETUP.md`)
✅ **Current State Analysis** (`CURRENT_STATE_ANALYSIS.md`)
✅ **Custom Audio Skills** Created for latency optimization and UI integration

---

## Installed Skills Overview

### Project Standards (2)
- `kazoo-development-standards` - Project-specific best practices
- `web-audio-performance` - Audio latency optimization guidance

### Code Quality (3)
- `code-review-excellence` - PR review patterns
- `debugging-strategies` - Systematic debugging
- `error-handling-patterns` - Resilient error handling

### Testing (2)
- `javascript-testing-patterns` - Jest/Vitest/Testing Library
- `e2e-testing-patterns` - Playwright/Cypress E2E tests

### JavaScript/TypeScript (3)
- `modern-javascript-patterns` - ES6+ best practices
- `typescript-advanced-types` - Advanced type safety
- `nodejs-backend-patterns` - Node.js patterns

### Audio Processing (2) - NEW!
- `web-audio-optimization` - Ultra-low latency audio processing
- `audio-ui-integration` - Real-time audio UI without blocking

**Total**: 12 skills active

---

## How to Use Skills in This Project

### Invoking a Skill

```bash
# In Claude Code chat
/skill <skill-name>
```

### Example Workflows

#### 1. Complete UI Modernization
```
/skill kazoo-development-standards

"Using the kazoo-development-standards skill, complete Phase 3 and 4
of the UI modernization:

1. Enhance Start/Stop button (gradient, pulse animation, hover effects)
2. Modernize status bar (color-coded latency badges)
3. Improve pitch visualization
4. Add subtle animations

Reference: .specify/specs/001-ui-modernization/tasks.md (T038-T074)"
```

#### 2. Optimize Audio Latency
```
/skill web-audio-optimization

"Using the web-audio-optimization skill, reduce latency from 180ms to <100ms:

1. Verify AudioWorklet mode is active
2. Profile audio pipeline bottlenecks
3. Optimize FFT size and feature extraction
4. Reduce YIN buffer size
5. Simplify synthesizer chain

Target: p95 latency <100ms"
```

#### 3. Improve Audio UI Responsiveness
```
/skill audio-ui-integration

"Using the audio-ui-integration skill, optimize UI updates for real-time audio:

1. Throttle note display updates to 60Hz
2. Add circular buffer for pitch history
3. Color-code latency badges (green/yellow/red)
4. Ensure UI doesn't block audio processing

Test: Smooth 60fps visualization, no audio glitches"
```

#### 4. Debug Issues
```
/skill debugging-strategies

"Using the debugging-strategies skill, investigate why audio glitches
occur when switching instruments mid-playback.

Current behavior: Clicks/pops when changing from Saxophone to Violin.
Expected: Smooth crossfade, no audible artifacts."
```

---

## Key Files to Know

### Documentation
- **WORKFLOW_SETUP.md** - Complete workflow setup guide (this is the master doc)
- **CURRENT_STATE_ANALYSIS.md** - Detailed current state analysis
- **QUICK_START_GUIDE.md** - This file (quick reference)
- **CLAUDE.md** - Project constraints and development rules
- **PROJECT_STATUS.md** - Current progress tracker

### Specs (UI Modernization)
- `.specify/specs/001-ui-modernization/spec.md` - Feature specification
- `.specify/specs/001-ui-modernization/tasks.md` - Task breakdown
- `.specify/specs/001-ui-modernization/plan.md` - Implementation plan
- `.specify/specs/001-ui-modernization/SESSION_HANDOVER.md` - Session notes

### Skills
- `.claude/skills/web-audio-optimization/SKILL.md` - Audio latency optimization
- `.claude/skills/audio-ui-integration/SKILL.md` - Audio UI integration
- `.claude/skills/kazoo-development-standards/SKILL.md` - Project standards

---

## Current Branch Status

### feature/001-ui-modernization

**Completed**:
- ✅ Phase 1: Hero section modernization
- ✅ Phase 2: Navigation + Instrument cards modernization
- ✅ Bug fixes: Instrument selection, dual AudioIO instances

**Pending**:
- ⏳ Phase 3: Controls + Status Bar (T038-T053)
- ⏳ Phase 4: Visualization + Polish (T058-T074)
- ⏳ Phase 5: Testing + Quality Gates (T075-T108)

**Progress**: 28/108 tasks (26%)

### main

**Stable version**: v0.3.0 (Performance First)
**Status**: All tests passing, audio functional, latency 180ms

---

## Quick Commands Reference

### Development
```bash
npm start                    # Start dev server (http://localhost:3000)
npm test                     # Run Vitest tests
npm run test:coverage        # Run with coverage report
```

### Browser Console (After Starting Audio)
```javascript
// Check latency stats
window.app.getLatencyStats()

// Verify AudioWorklet mode
window.container.get('audioIO').mode  // Should be 'worklet'

// List all services
window.container.getServiceNames()

// Check audio context
audioContext.baseLatency * 1000  // Base latency in ms
audioContext.sampleRate          // Sample rate (44100 or 48000)
```

### Git Workflow
```bash
# Check current branch
git status

# View recent commits
git log --oneline -10

# View changes in UI branch
git diff main...feature/001-ui-modernization --stat
```

---

## Priority Action Items

### Immediate (This Session)
1. ✅ Skills installed and documented
2. ⏳ Complete UI Phase 3 (Controls + Status Bar)
3. ⏳ Test in browser (visual + functional)
4. ⏳ Verify no audio regression

### Next Session
1. Complete UI Phase 4 (Visualization polish)
2. Run full browser testing (desktop + mobile)
3. Clean up zombie CSS
4. Run Lighthouse audit
5. Merge UI branch if quality gates pass

### Following Sessions
1. **Audio Robustness** (2-3 sessions):
   - Add pitch smoothing
   - Tune onset detection
   - Enhance timbre extraction
   - Add instrument crossfade

2. **Latency Optimization** (3-4 sessions):
   - Verify Worklet mode
   - Optimize FFT and feature extraction
   - Reduce YIN buffer
   - Simplify synthesizer
   - Target: <100ms first, <50ms final

---

## Troubleshooting

### Skills Not Loading
```bash
# Check if skill exists
ls -la .claude/skills/<skill-name>/

# Verify SKILL.md has proper YAML frontmatter
head -10 .claude/skills/<skill-name>/SKILL.md
```

### Audio Issues
```javascript
// Verify AudioWorklet mode (in browser console)
window.container.get('audioIO').mode
// Should return: 'worklet'
// If 'script-processor': Major latency issue (46ms base)

// Check for errors
// Open DevTools → Console → Look for red errors
```

### UI Not Updating
```bash
# Hard refresh browser
# Chrome/Firefox: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
# Safari: Cmd+Option+R

# Check Tailwind CDN loaded
# DevTools → Network → Look for cdn.tailwindcss.com (should be 200 OK)
```

### Tests Failing
```bash
# Run verbose tests
npm test -- --reporter=verbose

# Run specific test file
npm test -- tests/unit/app-container.test.js

# Check for uncommitted changes
git status
```

---

## Next Steps After This Session

### If UI Phase 3 Complete
1. **Test thoroughly** in browser (visual + functional)
2. **Take screenshots** of before/after for documentation
3. **Measure latency** to ensure no regression
4. **Continue to Phase 4** (Visualization polish)

### If Audio Issues Found
1. **Use debugging-strategies skill** to investigate
2. **Check browser console** for errors
3. **Verify AudioWorklet mode** is active
4. **Measure latency impact** of any changes

### Before Merging to Main
- [ ] All Phase 1-4 tasks complete
- [ ] Browser testing passed (Chrome, Firefox, Safari)
- [ ] Mobile responsive (320px+)
- [ ] Latency ≤ 200ms (no regression)
- [ ] Lighthouse Performance ≥ 90
- [ ] Lighthouse Accessibility ≥ 95
- [ ] All tests passing (npm test)
- [ ] No zombie CSS remaining

---

## Resources

### Internal Documentation
- [WORKFLOW_SETUP.md](.claude/WORKFLOW_SETUP.md) - Complete workflow guide
- [CURRENT_STATE_ANALYSIS.md](../CURRENT_STATE_ANALYSIS.md) - Detailed analysis
- [CLAUDE.md](../CLAUDE.md) - Development constraints
- [PROJECT_STATUS.md](../PROJECT_STATUS.md) - Progress tracker

### External Resources
- Claude Code Skills Marketplace: https://skillsmp.com
- Official Anthropic Skills Repo: https://github.com/anthropics/skills
- Web Audio API MDN: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API
- Tailwind CSS Docs: https://tailwindcss.com/docs

### MCP Resources (Future)
- MCP Official Site: https://modelcontextprotocol.io
- Audio MCP Server: https://github.com/BatchLion/mcp-audio-server
- MCP Marketplace: https://mcpmarket.com

---

## Questions?

### How do I...

**...use a skill for a specific task?**
```
/skill <skill-name>
"[Describe your task clearly, referencing relevant files/code]"
```

**...see all available skills?**
```bash
ls -la .claude/skills/
```

**...check current project status?**
```bash
cat PROJECT_STATUS.md
```

**...measure audio latency?**
```javascript
// In browser console after starting audio
window.app.getLatencyStats()
```

**...find UI modernization tasks?**
```bash
cat .specify/specs/001-ui-modernization/tasks.md
```

---

**Happy coding! 🎵**

**Remember**:
1. Frontend excellence first (complete UI Phase 3-4)
2. Audio robustness second (handle fast changes)
3. Latency optimization third (180ms → <50ms)
