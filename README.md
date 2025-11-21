<div align="center">
  <h1>🎵 MAMBO Whistle</h1>
  <p>
    <strong>Makes Any Mouth Become Orchestra</strong>
  </p>
  <p>
    A web-based vocal-to-instrument synthesis engine powered by real-time audio processing.
  </p>

  <p>
    <a href="#features">Features</a> •
    <a href="#getting-started">Getting Started</a> •
    <a href="#tech-stack">Tech Stack</a> •
    <a href="#roadmap">Roadmap</a>
  </p>

  <br>

  <img src="images/readme/app-interface.png" alt="MAMBO Whistle Interface" width="100%">
</div>

<br>

## 🚀 Introduction

**MAMBO Whistle** is an experimental web application that transforms your voice into synthesized instrument sounds in real-time. Using the Web Audio API and custom DSP algorithms, it enables anyone to "play" virtual instruments by simply humming, singing, or whistling into their microphone.

This project explores the intersection of vocal expression and digital synthesis, aiming to create an intuitive and responsive musical interface that feels like a real instrument.

## ✨ Key Features

-   **Real-Time Synthesis**: Low-latency audio processing using Web Audio API's AudioWorklet
-   **Multiple Instruments**: Choose from various instrument presets (Flute, Saxophone, Violin, Cello, etc.)
-   **Dual Synthesis Modes**:
    -   **Continuous Mode**: Smooth pitch tracking for expressive slides and vibrato
    -   **Stepped Mode**: Quantized notes for traditional scale playing
-   **Smart Auto-Tune**: Built-in pitch correction with adjustable settings
-   **Visual Feedback**: Real-time pitch visualization and audio analysis
-   **Privacy-First**: All processing happens locally in your browser

## 🛠 Tech Stack

-   **Frontend**: Vanilla JavaScript (ES Modules)
-   **Styling**: Tailwind CSS with custom glassmorphism design
-   **Audio**: Web Audio API, Tone.js
-   **Testing**: Vitest
-   **Tooling**: Node.js, npm

## 🏁 Getting Started

### Prerequisites

-   Node.js (v14 or higher)
-   npm (v6 or higher)
-   A modern web browser (Chrome/Edge recommended)

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Team-Kazoo/mambo-whistle.git
    cd mambo-whistle
    ```

2.  **Install dependencies**
    ```bash
    npm install
    ```

3.  **Start the development server**
    ```bash
    npm start
    ```
    The application will be available at `http://localhost:3000`.

4.  **Run tests** (Optional)
    ```bash
    npm test
    ```

## 📖 Usage Guide

1.  **Select an Instrument**: Choose from the available instrument presets
2.  **Start Engine**: Click "Start Engine" and grant microphone permissions
    *   *Tip: Use headphones to prevent audio feedback!*
3.  **Play**: Hum, sing, or whistle into your microphone
4.  **Adjust Settings**:
    *   Toggle Auto-Tune and select musical scales
    *   Add reverb or delay effects
    *   Switch between Continuous and Stepped modes

## 🛣 Roadmap

-   [ ] Core audio processing pipeline
-   [ ] Instrument preset system
-   [ ] Visual feedback interface
-   [ ] Auto-tune and effects
-   [ ] Performance optimization
-   [ ] Mobile browser support
-   [ ] MIDI export capability
-   [ ] Advanced synthesis models

## 🤝 Contributing

This is an experimental project. Contributions, ideas, and feedback are welcome!

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feat/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'feat: Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feat/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👥 Team

-   **Ziming Wang** - Project Lead
-   **Chuyue Gong** - Audio Research
-   **Tianxing Chang** - Development

---

<div align="center">
  <sub>Built with ❤️ using Web Audio API</sub>
</div>
