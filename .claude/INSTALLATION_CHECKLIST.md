# Installation Checklist - Additional Skills (Optional)

**Status**: Core skills complete, optional frontend skills pending
**Priority**: Low (can install later when needed)

---

## Already Installed ✅

- [x] kazoo-development-standards
- [x] web-audio-performance
- [x] code-review-excellence
- [x] debugging-strategies
- [x] error-handling-patterns
- [x] javascript-testing-patterns
- [x] e2e-testing-patterns
- [x] modern-javascript-patterns
- [x] typescript-advanced-types
- [x] nodejs-backend-patterns
- [x] web-audio-optimization (custom)
- [x] audio-ui-integration (custom)

**Total**: 12 skills active

---

## Optional: Frontend Design Skills

Install these from official Anthropic repository when working on advanced UI features.

### Installation Commands

```bash
# Navigate to home skills directory
cd ~/.claude/skills

# Clone official Anthropic skills repo (temporary)
git clone https://github.com/anthropics/skills.git anthropic-skills

# Copy frontend-design skill
cp -r anthropic-skills/frontend-design ./frontend-design

# Copy artifacts-builder skill
cp -r anthropic-skills/artifacts-builder ./artifacts-builder

# Copy canvas-design skill
cp -r anthropic-skills/canvas-design ./canvas-design

# Clean up temporary repo
rm -rf anthropic-skills

# Verify installation
ls -la ~/.claude/skills/
```

### Expected Result

```
~/.claude/skills/
├── frontend-design/      # Production-grade frontend interfaces
├── artifacts-builder/    # Complex UI with React, Tailwind
└── canvas-design/        # Visual art and visualizations
```

### When to Install

**frontend-design**:
- Building new UI sections from scratch
- Major redesign projects
- Need design system guidance

**artifacts-builder**:
- Creating complex interactive components
- Building React-based features (future)
- Need shadcn/ui component examples

**canvas-design**:
- Advanced audio visualizations
- Generative art for UI elements
- Custom graphics/animations

---

## Optional: MCP Servers

Install these if you need external tool integration.

### audio-mcp-server (Python)

**Purpose**: Audio I/O testing, recording, playback

```bash
# Requires Python 3.8+
pip install mcp-audio-server

# Verify installation
python -c "import mcp_audio_server; print('OK')"
```

**Use cases**:
- Testing microphone input
- Debugging audio processing
- Recording test samples

### voice-mcp (Node.js)

**Purpose**: Voice control, speech-to-text, text-to-speech

```bash
# Requires Node.js 18+
npm install -g voice-mcp

# Verify installation
voice-mcp --version
```

**Use cases**:
- Voice-controlled testing
- Accessibility features (future)
- Voice command support (future)

### browser-automation-mcp (Playwright)

**Purpose**: Automated browser testing, screenshots, profiling

```bash
# Requires Node.js 18+
npm install -g @playwright/mcp

# Install browsers
npx playwright install

# Verify installation
npx playwright --version
```

**Use cases**:
- Automated UI testing
- Visual regression testing
- Performance profiling automation

---

## Current Status

### Production Ready ✅
The project is fully functional with 12 installed skills:
- Development standards
- Testing patterns
- Audio optimization (custom)
- Audio UI integration (custom)

### Optional Enhancements 🔵
Additional skills can be installed later:
- Frontend design skills (3 skills)
- MCP servers (3 servers)

### Recommendation 💡
**Don't install optional skills yet**. They add complexity and may not be needed for current priorities (UI completion, audio robustness, latency optimization).

Install on-demand when you encounter:
- Need for design system guidance → Install frontend-design
- Building complex visualizations → Install canvas-design
- Need automated testing → Install browser-automation-mcp

---

## Verification

### Check Installed Skills

```bash
# List all skills
ls -la .claude/skills/

# Should show 12 directories (current)
# Will show 15 directories if optional frontend skills installed
```

### Check Skill Metadata

```bash
# Verify a skill has proper YAML frontmatter
head -20 .claude/skills/web-audio-optimization/SKILL.md

# Should show:
# ---
# name: web-audio-optimization
# description: ...
# ---
```

### Test Skill Invocation

In Claude Code chat:
```
/skill web-audio-optimization

"List the 5 critical bottlenecks for latency optimization in Kazoo Proto"
```

Expected: Skill loads and provides detailed bottleneck analysis

---

## Troubleshooting

### Skill Not Found

**Problem**: `/skill frontend-design` returns "skill not found"

**Solution**:
```bash
# Check if skill exists
ls -la ~/.claude/skills/frontend-design/

# If not, install from Anthropic repo (see above)
```

### Skill Loads But Doesn't Work

**Problem**: Skill invokes but doesn't provide relevant context

**Cause**: Missing or malformed YAML frontmatter in SKILL.md

**Solution**:
```bash
# Check SKILL.md format
head -20 ~/.claude/skills/<skill-name>/SKILL.md

# Must start with:
# ---
# name: skill-name
# description: ...
# ---
```

### MCP Server Installation Fails

**Problem**: `pip install mcp-audio-server` fails

**Solution**:
```bash
# Check Python version (requires 3.8+)
python --version

# Try with pip3
pip3 install mcp-audio-server

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install mcp-audio-server
```

---

## Summary

### ✅ Complete (No Action Needed)
- 12 core skills installed and documented
- Custom audio skills created
- Workflow documentation complete

### 🔵 Optional (Install When Needed)
- Frontend design skills (3 skills)
- MCP servers (3 servers)

### 📋 Next Steps
1. **Review documentation**: [.claude/QUICK_START_GUIDE.md](.claude/QUICK_START_GUIDE.md)
2. **Start development**: Complete UI Phase 3 (Controls + Status Bar)
3. **Install optional skills**: Only if/when needed for specific tasks

---

**Installation Status**: Production Ready ✅
**Optional Enhancements**: Available but not required
**Recommendation**: Proceed with development using current skill set
