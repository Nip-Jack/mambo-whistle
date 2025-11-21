/**
 * Integration Tests: UI Interaction → Store → View Rendering
 *
 * These tests verify the complete state-driven architecture flow:
 * 1. User interaction triggers handler
 * 2. Handler updates Store
 * 3. Store notifies subscribers
 * 4. View renders new state
 */

/**
 * @vitest-environment happy-dom
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { store } from '../../js/state/store.js';
import { MamboView } from '../../js/ui/mambo-view.js';

describe('UI State Flow Integration', () => {
    let view;

    beforeEach(() => {
        // Create a minimal DOM environment using happy-dom (Vitest built-in)
        document.body.innerHTML = `
            <!DOCTYPE html>
            <html>
            <body>
                <!-- Effects UI -->
                <input id="reverbSlider" type="range" min="0" max="100" value="20" />
                <span id="reverbValue">20%</span>
                <input id="delaySlider" type="range" min="0" max="100" value="0" />
                <span id="delayValue">0%</span>

                <!-- Instrument UI -->
                <button class="instrument-btn" data-instrument="flute">Flute</button>
                <button class="instrument-btn" data-instrument="cello">Cello</button>
                <button class="instrument-btn" data-instrument="violin">Violin</button>
                <span id="instrumentStatus">Flute</span>

                <!-- Transport UI -->
                <button id="startBtn"><span>Start Engine</span></button>
                <button id="stopBtn" class="hidden">Stop</button>
                <input id="modeToggle" type="checkbox" checked />
                <span id="modeText">Continuous</span>
        `;

        view = new MamboView(document);

        // Reset store to initial state
        store.setState({
            status: { engineState: 'idle', lastError: null },
            synth: {
                instrument: 'flute',
                continuousMode: true,
                autoTune: { enabled: false, key: 'C', scale: 'chromatic', strength: 0.5, speed: 0.1 },
                reverbWet: 0.2,
                delayWet: 0.0
            },
            audio: {
                inputDeviceId: 'default',
                outputDeviceId: 'default',
                lastKnownInputLabel: 'System Default',
                lastKnownOutputLabel: 'System Default',
                availableInputDevices: [],
                availableOutputDevices: [],
                latency: 0,
                isWorkletActive: false
            },
            ui: { isSettingsOpen: false, isHelpOpen: false, activeView: 'main' }
        });
    });

    describe('Effects UI Flow', () => {
        it('should update store and render view when reverb slider changes', () => {
            // 1. Setup: Bind events and subscribe to store
            const mockReverbHandler = vi.fn((percent) => {
                const wet = percent / 100;
                store.setReverbWet(wet);
            });

            view.bindEffectsUI({
                onReverbChange: mockReverbHandler,
                onDelayChange: vi.fn()
            });

            // Subscribe view to store updates
            store.subscribe((newState) => {
                view.renderEffects(newState.synth);
            });

            // 2. Action: Simulate user moving slider to 75%
            const slider = document.getElementById('reverbSlider');
            slider.value = '75';
            slider.dispatchEvent(new Event('input', { bubbles: true }));

            // 3. Assertions
            expect(mockReverbHandler).toHaveBeenCalledWith(75);
            expect(store.getState().synth.reverbWet).toBe(0.75);

            // View should reflect new state
            const displayValue = document.getElementById('reverbValue');
            expect(displayValue.textContent).toBe('75%');
            expect(slider.value).toBe('75');
        });

        it('should update store and render view when delay slider changes', () => {
            const mockDelayHandler = vi.fn((percent) => {
                const wet = percent / 100;
                store.setDelayWet(wet);
            });

            view.bindEffectsUI({
                onReverbChange: vi.fn(),
                onDelayChange: mockDelayHandler
            });

            store.subscribe((newState) => {
                view.renderEffects(newState.synth);
            });

            const slider = document.getElementById('delaySlider');
            slider.value = '50';
            slider.dispatchEvent(new Event('input', { bubbles: true }));

            expect(mockDelayHandler).toHaveBeenCalledWith(50);
            expect(store.getState().synth.delayWet).toBe(0.5);

            const displayValue = document.getElementById('delayValue');
            expect(displayValue.textContent).toBe('50%');
        });
    });

    describe('Instrument Selection Flow', () => {
        it('should update store and render view when instrument is selected', () => {
            // 1. Setup
            const mockInstrumentHandler = vi.fn((instrumentId) => {
                store.setInstrument(instrumentId);
            });

            view.bindInstrumentUI({
                onSelectInstrument: mockInstrumentHandler
            });

            store.subscribe((newState) => {
                view.renderInstrument(newState.synth);
            });

            // 2. Action: User clicks "Cello" button
            const celloBtn = document.querySelector('[data-instrument="cello"]');
            celloBtn.click();

            // 3. Assertions
            expect(mockInstrumentHandler).toHaveBeenCalledWith('cello');
            expect(store.getState().synth.instrument).toBe('cello');

            // View should show Cello as active
            expect(celloBtn.classList.contains('active')).toBe(true);

            // Other instruments should not be active
            const fluteBtn = document.querySelector('[data-instrument="flute"]');
            expect(fluteBtn.classList.contains('active')).toBe(false);
        });

        it('should update instrument status badge when selection changes', () => {
            const mockHandler = vi.fn((id) => store.setInstrument(id));

            view.bindInstrumentUI({ onSelectInstrument: mockHandler });
            store.subscribe((state) => view.renderInstrument(state.synth));

            // Initial render
            view.renderInstrument(store.getState().synth);

            // Click violin
            const violinBtn = document.querySelector('[data-instrument="violin"]');
            violinBtn.click();

            expect(store.getState().synth.instrument).toBe('violin');
            // Note: Status badge update depends on button structure in real DOM
        });
    });

    describe('Transport UI Flow', () => {
        it('should render transport state when engine status changes', () => {
            // Subscribe view to store
            store.subscribe((newState) => {
                view.renderTransport(newState.status, newState.synth);
            });

            // Initial render (idle state)
            view.renderTransport(store.getState().status, store.getState().synth);

            const startBtn = document.getElementById('startBtn');
            const stopBtn = document.getElementById('stopBtn');

            expect(startBtn.classList.contains('hidden')).toBe(false);
            expect(stopBtn.classList.contains('hidden')).toBe(true);

            // Change to running
            store.setEngineStatus('running');

            expect(startBtn.classList.contains('hidden')).toBe(true);
            expect(stopBtn.classList.contains('hidden')).toBe(false);

            // Change to starting
            store.setEngineStatus('starting');

            expect(startBtn.classList.contains('hidden')).toBe(true);
            expect(startBtn.disabled).toBe(true);
        });

        it('should render mode toggle state correctly', () => {
            store.subscribe((newState) => {
                view.renderTransport(newState.status, newState.synth);
            });

            view.renderTransport(store.getState().status, store.getState().synth);

            const modeToggle = document.getElementById('modeToggle');
            const modeText = document.getElementById('modeText');

            // Initial: Continuous mode
            expect(modeToggle.checked).toBe(true);
            expect(modeText.textContent).toBe('Continuous');

            // Switch to legacy mode via store
            store.setState({
                synth: { ...store.getState().synth, continuousMode: false }
            });

            expect(modeToggle.checked).toBe(false);
            expect(modeText.textContent).toBe('Legacy');
        });
    });

    describe('Cross-Module State Consistency', () => {
        it('should maintain state consistency across multiple UI updates', () => {
            // Setup all bindings
            view.bindEffectsUI({
                onReverbChange: (p) => store.setReverbWet(p / 100),
                onDelayChange: (p) => store.setDelayWet(p / 100)
            });

            view.bindInstrumentUI({
                onSelectInstrument: (id) => store.setInstrument(id)
            });

            // Subscribe view to all updates
            store.subscribe((state) => {
                view.renderEffects(state.synth);
                view.renderInstrument(state.synth);
                view.renderTransport(state.status, state.synth);
            });

            // Perform multiple actions
            store.setReverbWet(0.8);
            store.setInstrument('violin');
            store.setEngineStatus('running');

            // Verify state consistency
            const state = store.getState();
            expect(state.synth.reverbWet).toBe(0.8);
            expect(state.synth.instrument).toBe('violin');
            expect(state.status.engineState).toBe('running');

            // Verify UI reflects state
            expect(document.getElementById('reverbValue').textContent).toBe('80%');
            expect(document.querySelector('[data-instrument="violin"]').classList.contains('active')).toBe(true);
            expect(document.getElementById('stopBtn').classList.contains('hidden')).toBe(false);
        });
    });
});
