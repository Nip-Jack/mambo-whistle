export class MamboView {
    /**
     * @param {Document} rootDocument
     */
    constructor(rootDocument = document) {
        this.doc = rootDocument;

        // Cache Elements
        this.reverbSlider = this.doc.getElementById('reverbSlider');
        this.reverbValue = this.doc.getElementById('reverbValue');
        this.delaySlider = this.doc.getElementById('delaySlider');
        this.delayValue = this.doc.getElementById('delayValue');

        // Transport Elements
        this.startBtn = this.doc.getElementById('startBtn');
        this.stopBtn = this.doc.getElementById('stopBtn');
        this.modeToggle = this.doc.getElementById('modeToggle');
        this.modeText = this.doc.getElementById('modeText');

        // Instrument Elements
        this.instrumentBtns = this.doc.querySelectorAll('.instrument-btn');
        this.instrumentStatus = this.doc.getElementById('instrumentStatus');
    }

    /**
     * Bind UI events (Delegate logic to handlers)
     * @param {object} handlers
     * @param {(percent: number) => void} handlers.onReverbChange
     * @param {(percent: number) => void} handlers.onDelayChange
     */
    bindEffectsUI(handlers) {
        if (this.reverbSlider && handlers.onReverbChange) {
            this.reverbSlider.addEventListener('input', (e) => {
                const val = parseInt(e.target.value, 10);
                if (!isNaN(val)) handlers.onReverbChange(val);
            });
        }
        
        if (this.delaySlider && handlers.onDelayChange) {
            this.delaySlider.addEventListener('input', (e) => {
                const val = parseInt(e.target.value, 10);
                if (!isNaN(val)) handlers.onDelayChange(val);
            });
        }
    }

    /**
     * Bind Instrument Selection events
     * @param {object} handlers
     * @param {(instrumentId: string) => void} handlers.onSelectInstrument
     */
    bindInstrumentUI(handlers) {
        if (this.instrumentBtns && handlers.onSelectInstrument) {
            this.instrumentBtns.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const instrumentId = e.currentTarget.dataset.instrument;
                    if (instrumentId) {
                        handlers.onSelectInstrument(instrumentId);
                    }
                });
            });
        }
    }

    /**
     * Bind Transport events
     * @param {object} handlers
     * @param {() => void} handlers.onStart
     * @param {() => void} handlers.onStop
     * @param {(isContinuous: boolean) => void} handlers.onModeChange
     */
    bindTransportUI(handlers) {
        if (this.startBtn && handlers.onStart) {
            this.startBtn.addEventListener('click', handlers.onStart);
        }
        if (this.stopBtn && handlers.onStop) {
            this.stopBtn.addEventListener('click', handlers.onStop);
        }
        if (this.modeToggle && handlers.onModeChange) {
            this.modeToggle.addEventListener('change', (e) => {
                handlers.onModeChange(e.target.checked);
            });
        }
    }

    /**
     * Render state to UI
     * @param {object} synthState - The 'synth' slice of the app state
     */
    renderEffects(synthState) {
        if (!synthState) return;

        const reverbPercent = Math.round((synthState.reverbWet ?? 0) * 100);
        const delayPercent = Math.round((synthState.delayWet ?? 0) * 100);

        // Reverb
        if (this.reverbSlider && this.reverbSlider.value !== String(reverbPercent)) {
            this.reverbSlider.value = reverbPercent;
        }
        if (this.reverbValue && this.reverbValue.textContent !== `${reverbPercent}%`) {
            this.reverbValue.textContent = `${reverbPercent}%`;
        }

        // Delay
        if (this.delaySlider && this.delaySlider.value !== String(delayPercent)) {
            this.delaySlider.value = delayPercent;
        }
        if (this.delayValue && this.delayValue.textContent !== `${delayPercent}%`) {
            this.delayValue.textContent = `${delayPercent}%`;
        }
    }

    /**
     * Render Transport State
     * @param {object} statusState - The 'status' slice
     * @param {object} synthState - The 'synth' slice
     */
    renderTransport(statusState, synthState) {
        // 1. Engine State (Start/Stop buttons)
        if (statusState && statusState.engineState) {
            const isRunning = statusState.engineState === 'running';
            const isStarting = statusState.engineState === 'starting';
            
            // Simple visibility toggle
            if (this.startBtn) {
                const shouldHide = isRunning || isStarting;
                this.startBtn.classList.toggle('hidden', shouldHide);
                
                // Disable during starting, but DO NOT overwrite innerHTML with textContent
                this.startBtn.disabled = isStarting;
                this.startBtn.classList.toggle('opacity-50', isStarting);
                this.startBtn.classList.toggle('cursor-not-allowed', isStarting);
                
                // Optional: If you really want to change text, find the span inside
                const textSpan = this.startBtn.querySelector('span');
                if (textSpan) {
                    textSpan.textContent = isStarting ? 'Starting...' : 'Start Engine';
                }
            }

            if (this.stopBtn) {
                // Show stop button only if running
                const shouldShow = isRunning;
                this.stopBtn.classList.toggle('hidden', !shouldShow);
            }
        }

        // 2. Mode Toggle
        if (synthState && this.modeToggle) {
            const isContinuous = synthState.continuousMode;
            if (this.modeToggle.checked !== isContinuous) {
                this.modeToggle.checked = isContinuous;
            }
            if (this.modeText) {
                this.modeText.textContent = isContinuous ? 'Continuous' : 'Legacy';
            }
        }
    }

    /**
     * Render Instrument State
     * @param {object} synthState - The 'synth' slice
     */
    renderInstrument(synthState) {
        if (!synthState || !synthState.instrument) return;

        const activeId = synthState.instrument;

        // 1. Update active class on buttons
        if (this.instrumentBtns) {
            this.instrumentBtns.forEach(btn => {
                if (btn.dataset.instrument === activeId) {
                    btn.classList.add('active');
                    // Update Status Badge if this is the active button
                    if (this.instrumentStatus) {
                         const nameEl = btn.querySelector('.font-semibold');
                         if (nameEl) this.instrumentStatus.textContent = nameEl.textContent;
                    }
                } else {
                    btn.classList.remove('active');
                }
            });
        }
    }
}
