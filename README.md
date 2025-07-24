# 🎙️ Whisper Speech-to-Text (Offline Transcription on macOS M3 Pro)

This project leverages OpenAI's Whisper model to perform high-accuracy speech-to-text transcription **entirely offline** on Apple Silicon hardware. Built using [`whisper.cpp`](https://github.com/ggerganov/whisper.cpp), optimized for the **Apple M3 Pro**.

<p align="center">
  <img src="https://img.shields.io/badge/Platform-macOS-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Model-Whisper%20Medium-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/GPU-Apple%20M3%20Pro-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Accuracy-%E2%89%8892%25-lightgrey?style=for-the-badge"/>
</p>

---

## 🧠 Features

- ✅ Offline, privacy-friendly transcription with OpenAI's Whisper model
- 🧠 Uses the **Whisper Medium** model (approx. **769 million parameters**)
- ⚡ GPU-accelerated via Apple Metal (M3 Pro)
- 🗣️ Multilingual support (supports 99+ languages)
- ⏱️ Outputs time-stamped text (e.g., `.txt`, `.srt`)

---

## 💻 System Requirements

| Component     | Specs                         |
|--------------|-------------------------------|
| Device        | MacBook Pro (Apple M3 Pro)    |
| CPU           | 11-core                       |
| GPU           | 14-core Apple GPU             |
| RAM           | 18 GB unified memory          |
| OS            | macOS Sonoma or later         |
| Tools         | Homebrew, CMake, Git, FFmpeg  |

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Ahmet-Ruchan/whisper-speech-to-text.git
cd whisper-speech-to-text
```

### 1. Clone the repository

```bash
brew install cmake ffmpeg git
```

### 2. Install dependencies

```bash
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp
make
```

### 3. Clone and build whisper.cpp

```bash
./models/download-ggml-model.sh medium
```

### 4. Download the model

```bash
ffmpeg -i input.mp3 output.wav
```

### 5. Convert audio to WAV (if needed)

```bash
./build/bin/whisper-cli \
  -m ./models/ggml-medium.bin \
  -f ./samples/demo.wav \
  -l tr
```

---

This `README.md` file is optimized for clarity, aesthetics, and technical completeness. You can place it in the root of your repository. Let me know if you'd like help adding screenshots, demos, or embedding terminal GIFs!
