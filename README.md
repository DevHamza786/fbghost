# FB Ghost Agency v3.1 👻

A zero-risk, high-fidelity media engine for Meta Business Suite automation.

## 🚀 Quick Start

1. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

2. **Setup Environment**:
   - Rename `.env.example` to `.env` and add your API keys.

3. **Run the Dashboard**:
   ```bash
   streamlit run app.py
   ```

## 🧠 Architectural Overview

- **The Brain (Gemini 3.1 Pro)**: Orchestrates the entire production loop.
- **The Policy Crawler**: Autonomous scraping of `transparency.fb.com` to ensure 100% compliance.
- **The Creator (Veo 3.1)**: Generates 100% original 4K cinematic assets.
- **The Vision Auditor**: Pre-flight vision check for watermarks and logos.
- **The Executor (Computer Use)**: Stealth navigation via Playwright with human-mimicry.

## 🛡️ Stealth Modules

- **Metadata Injector**: Strips original EXIF and injects unique MD5 hashes + iPhone 15 Pro Max properties.
- **Stealth Browser**: Playwright integration with randomized interaction patterns to bypass bot detection.
