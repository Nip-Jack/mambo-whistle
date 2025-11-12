# Feature Specification: UI Modernization with Tailwind CSS

**Feature Branch**: `feature/001-ui-modernization`
**Created**: 2025-11-12
**Status**: Draft
**Approach**: Progressive Enhancement (Preserve all existing functionality, enhance visual layer only)

## User Scenarios & Testing

### User Story 1 - Modern Visual Experience (Priority: P1)

As a musician trying Kazoo Proto for the first time, I want the interface to look modern and professional so that I trust the application's quality and feel motivated to explore its features.

**Why this priority**: First impressions are critical. A dated UI signals "abandoned project" or "low quality", even if the audio engine is excellent. This is the foundation that makes all other improvements worthwhile.

**Independent Test**: Can be tested by simply loading the page. Success = visual impression feels "2025 modern" not "2015 basic". Specific indicators: gradient backgrounds, smooth shadows, Tailwind utility styling visible in DevTools.

**Acceptance Scenarios**:

1. **Given** a user visits the application for the first time, **When** the page loads, **Then** they see a clean, modern interface with professional gradients, shadows, and spacing
2. **Given** a user hovers over an instrument card, **When** the cursor enters the card area, **Then** the card smoothly elevates with shadow transition and subtle scale effect
3. **Given** a user views the page on mobile, **When** they rotate device or resize browser, **Then** layout adapts fluidly without breaking or overlapping content

---

### User Story 2 - Enhanced Instrument Selection (Priority: P2)

As a user selecting an instrument, I want interactive visual feedback when I hover and click so that I feel confident about which instrument I've chosen and enjoy the selection process.

**Why this priority**: Instrument selection is the first interaction users perform. Making it delightful encourages exploration and sets a positive tone for the experience.

**Independent Test**: Can be tested by tabbing through and clicking instrument buttons. Success = each button has clear hover state, active state, and selected state with smooth transitions.

**Acceptance Scenarios**:

1. **Given** user hovers over an unselected instrument, **When** cursor enters button area, **Then** button shows subtle elevation, scale (1.02x), and glow effect within 200ms
2. **Given** user clicks an instrument button, **When** click completes, **Then** button shows selected state (colored ring, filled background) and previous selection de-highlights
3. **Given** user navigates via keyboard (Tab key), **When** focus lands on instrument button, **Then** button shows distinct focus ring (2px blue outline) that doesn't obscure content

---

### User Story 3 - Prominent Start/Stop Controls (Priority: P1)

As a user ready to play, I want the start button to be visually prominent and provide clear feedback so that I immediately know how to begin and what state the system is in.

**Why this priority**: The start button is the primary call-to-action. If users can't find it or don't feel confident clicking it, the app is unusable. Critical for conversion.

**Independent Test**: Can be tested by loading page and looking for start button. Success = button is impossible to miss, clearly labeled, and animates to draw attention.

**Acceptance Scenarios**:

1. **Given** user loads the page, **When** they scan the interface, **Then** the start button is the largest interactive element with a subtle pulse animation (1.5s cycle)
2. **Given** user clicks "Start Playing", **When** audio system initializes, **Then** button morphs into red "Stop" button with stop icon, animation pauses, and status badge updates to "Recording"
3. **Given** user hovers over start/stop button, **When** cursor enters button, **Then** button scales slightly (1.05x) and shadow deepens, indicating interactivity

---

### User Story 4 - Clear Status Communication (Priority: P2)

As a user who has started audio capture, I want real-time feedback about system status (latency, confidence, current note) so that I understand how well the detection is working and can adjust my input.

**Why this priority**: Without feedback, users don't know if the system is working or if they need to adjust microphone position, volume, or singing style. Reduces support burden.

**Independent Test**: Can be tested by starting audio and humming. Success = status bar shows updating values, current note displays prominently, and confidence meter changes color based on signal quality.

**Acceptance Scenarios**:

1. **Given** user has started audio capture, **When** they hum a note, **Then** current note display updates within 50ms showing note name (e.g., "C4") in large bold text with frequency in Hz below
2. **Given** audio is processing, **When** latency varies, **Then** latency value updates in status bar with color coding (green < 50ms, yellow 50-100ms, red > 100ms)
3. **Given** user sings too quietly, **When** confidence drops below 50%, **Then** confidence meter turns orange/red and helper text suggests "Sing louder or move closer to mic"

---

### User Story 5 - Accessible Keyboard Navigation (Priority: P2)

As a keyboard-only user (or musician with hands on instrument), I want to navigate and control the entire interface without a mouse so that I can use the app efficiently and accessibly.

**Why this priority**: Accessibility is a constitutional requirement (Principle IV). Many musicians prefer keyboard workflows. Also improves general usability.

**Independent Test**: Can be tested by unplugging mouse and navigating with Tab, Enter, Space, Escape keys. Success = all interactive elements reachable, focus states visible, actions work as expected.

**Acceptance Scenarios**:

1. **Given** user presses Tab key repeatedly, **When** focus moves through interface, **Then** focus order is logical (top to bottom, left to right), focus ring is always visible (no invisible focus), and user can reach all buttons and controls
2. **Given** focus is on an instrument button, **When** user presses Enter or Space, **Then** instrument is selected as if clicked with mouse
3. **Given** focus is on start button, **When** user presses Enter, **Then** audio capture starts without mouse interaction required

---

### User Story 6 - Improved Visual Hierarchy (Priority: P3)

As a new user scanning the interface, I want clear visual hierarchy (what's important, what's secondary) so that I can understand the app's structure without reading every word.

**Why this priority**: Good hierarchy reduces cognitive load and improves perceived simplicity. Lower priority because app already has decent structure, this is enhancement not fix.

**Independent Test**: Can be tested with "5-second test" - show page for 5 seconds, hide it, ask what user remembers. Success = users recall "big start button, instrument grid, status info" in correct importance order.

**Acceptance Scenarios**:

1. **Given** user views the page, **When** they scan top-to-bottom, **Then** visual weight decreases appropriately: hero section (largest), instrument selection (medium), status bar (smallest/subtle)
2. **Given** user looks at instrument cards, **When** comparing selected vs unselected, **Then** selected card is clearly distinguishable through color, border weight, or background fill
3. **Given** user reads help text, **When** they compare it to primary content, **Then** help text is visually secondary (smaller font, muted color, collapsible section)

---

### Edge Cases

- **What happens when CSS fails to load?** Page must remain functional with unstyled HTML. All buttons still clickable, text readable, layout not broken.
- **What happens on very narrow screens (< 320px)?** Instrument grid switches to single column, buttons stack vertically, canvas visualizer scales proportionally or hides.
- **What happens with slow network (3G)?** Tailwind CSS loads from CDN with appropriate caching headers. If CDN fails, fallback to inline critical CSS or unstyled but functional HTML.
- **What happens if user has motion-reduced preferences?** All animations (pulse, hover scale, transitions) respect `prefers-reduced-motion` media query and show instant state changes instead.
- **What happens on high contrast mode?** Focus rings and borders must have sufficient contrast (3:1 minimum) against background in Windows High Contrast Mode.

## Requirements

### Functional Requirements

- **FR-001**: System MUST integrate Tailwind CSS via CDN without requiring build step (preserve `npx serve` workflow)
- **FR-002**: All existing audio functionality MUST remain 100% operational after UI changes (no regressions)
- **FR-003**: Users MUST be able to select instruments via mouse, touch, or keyboard (maintain multi-input support)
- **FR-004**: Start/Stop button MUST show clear visual state (Ready → Recording → Ready cycle)
- **FR-005**: Current note display MUST update in real-time when audio is active (< 100ms refresh rate)
- **FR-006**: Status bar MUST show latency, confidence, and system status with color-coded indicators
- **FR-007**: All interactive elements MUST have visible focus states for keyboard navigation (meet WCAG 2.1 AA)
- **FR-008**: Hover effects MUST be smooth (CSS transitions, not instant state changes)
- **FR-009**: Layout MUST be responsive (mobile 320px+, tablet 768px+, desktop 1024px+)
- **FR-010**: Dark mode toggle MUST NOT be implemented in this phase (deferred to future feature)

### Non-Functional Requirements

- **NFR-001**: Audio latency MUST NOT increase by more than 10ms after UI changes
- **NFR-002**: Page load time MUST remain under 2 seconds on 4G connection
- **NFR-003**: Total added CSS/JS MUST be under 50KB gzipped (Tailwind CDN + custom styles)
- **NFR-004**: Lighthouse Performance score MUST be ≥ 90
- **NFR-005**: Lighthouse Accessibility score MUST be ≥ 95
- **NFR-006**: Browser support: Chrome 90+, Firefox 88+, Safari 14+ (no IE11)
- **NFR-007**: All CSS transitions MUST complete within 300ms to feel instant
- **NFR-008**: No new npm dependencies required (Tailwind via CDN only)

### Key Entities

- **Visual Theme**: Colors (primary, secondary, accent, neutral scales), shadows (sm, md, lg, xl), spacing scale (consistent Tailwind spacing)
- **Component States**: Default, Hover, Active, Focus, Disabled, Selected (each with defined visual treatment)
- **Instrument Card**: Icon, name, description, state indicator (CSS classes)
- **Status Badge**: Label, value, color variant (success/warning/error), update frequency

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users rate visual appeal 4/5 or higher in user testing (5-user sample)
- **SC-002**: Instrument selection time decreases by 20% (measured via click analytics or manual timing)
- **SC-003**: First-time users successfully start audio on first attempt without help (90% success rate in usability test)
- **SC-004**: Audio latency remains within ±10ms of baseline (measured via `window.app.getLatencyStats()` before/after)
- **SC-005**: Zero keyboard navigation issues reported in accessibility audit (tested with screen reader + keyboard-only)
- **SC-006**: Lighthouse Accessibility score ≥ 95 (automated test)
- **SC-007**: Page load (FCP) remains under 1.5 seconds on 4G throttled network (Chrome DevTools)
- **SC-008**: Zero visual regressions on mobile devices (tested on iOS Safari, Android Chrome)

### Quality Gates

Before merging to main:
1. All Vitest tests pass (`npm test`)
2. Manual audio test confirms latency unchanged
3. Keyboard-only navigation test completed (all features accessible)
4. Visual inspection on 3 browsers (Chrome, Firefox, Safari)
5. Mobile responsive test on 2 screen sizes (375px phone, 768px tablet)

## Technical Constraints (from Constitution)

- **NO frameworks**: Must remain vanilla JavaScript + ES Modules
- **NO build tools**: Must work with `npx serve` (no Vite/Webpack in this phase)
- **Tailwind CDN only**: Use Play CDN (https://cdn.tailwindcss.com) for fastest integration
- **Audio core is READ-ONLY**: Cannot modify js/audio-io.js, js/pitch-detector.js, js/synthesizer.js, etc.
- **Use UIManager events**: All UI updates must go through existing event system (no direct DOM manipulation from audio modules)
- **Performance gates**: Latency +10ms max, page weight +50KB max, Lighthouse Performance ≥ 90

## Out of Scope

The following are explicitly NOT included in this feature:
- Dark mode implementation (future feature)
- Vite/Webpack build setup (deferred to Phase 2)
- Audio engine optimization (separate effort)
- New instruments beyond existing 6 (separate feature)
- Recording/export functionality (separate feature)
- User accounts or settings persistence (separate feature)
- Mobile app (PWA) capabilities (separate feature)
- Frequency spectrum analyzer (deferred, performance concern)

## Implementation Phases

### Phase 1: Foundation (Day 1)
- Add Tailwind CSS via CDN to index.html
- Convert hero section to Tailwind utilities
- Convert navigation bar to Tailwind utilities
- Test: Verify all existing functionality works

### Phase 2: Instrument Selection (Day 2)
- Redesign instrument button cards with Tailwind
- Add hover/focus states with CSS transitions
- Implement selected state visual indicator
- Test: Verify keyboard navigation and selection logic

### Phase 3: Controls & Status (Day 2-3)
- Enhance start/stop button styling (size, color, pulse animation)
- Redesign status bar with color-coded badges
- Improve visual hierarchy (spacing, sizing, contrast)
- Test: Verify button state transitions and status updates

### Phase 4: Visualization & Polish (Day 3-4)
- Style current note display with larger typography
- Add subtle animations (fade-in, slide transitions)
- Enhance pitch canvas styling (border, shadow)
- Test: Verify animations don't impact performance

### Phase 5: Testing & Optimization (Day 4-5)
- Run full accessibility audit (keyboard, screen reader)
- Measure audio latency before/after comparison
- Test on mobile devices (responsive layout)
- Run Lighthouse audits (Performance, Accessibility, Best Practices)
- Fix any issues found, optimize if needed

## Review & Acceptance Checklist

- [ ] All user stories have clear acceptance criteria
- [ ] Edge cases are identified and handled
- [ ] Functional requirements are testable and complete
- [ ] Non-functional requirements (performance, accessibility) are measurable
- [ ] Success criteria are specific and measurable
- [ ] Technical constraints from constitution are respected
- [ ] Out-of-scope items are documented to prevent scope creep
- [ ] Implementation phases are realistic (3-5 day timeline)
- [ ] No ambiguous language ("should", "might", "probably")
- [ ] All placeholders have been replaced with actual content

## Notes

This specification focuses on visual enhancement without touching the audio pipeline. The goal is quick delivery (3-5 days) of a modern, accessible interface that makes the excellent audio engine more appealing to new users. All changes are reversible and can be AB-tested before full rollout.
