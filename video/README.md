# PayMesh AI — Remotion Video Studio

Programmatic, code-driven video creation and rendering using **Remotion**, React, and TypeScript for **PayMesh AI** (PayPal AI Hackathon 2026).

---

## 🎬 Available Compositions

| Composition ID | Resolution | Frame Rate | Duration | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **`PayMeshDemo`** | 1920 × 1080 (1080p) | 30 fps | 1800 frames (60.0s) | Complete Hackathon Demo: Problem, Solution, 7 Live UI Screens, Architecture & Outro |
| **`PayMeshTeaser`** | 1920 × 1080 (1080p) | 30 fps | 450 frames (15.0s) | High-energy social media / pitch teaser video |

---

## 🚀 Quick Start Commands

Run these commands inside the `video/` directory:

### 1. Interactive Preview Studio (GUI)
Launch the interactive Remotion Studio in your browser to scrub the timeline, preview animations, and inspect frames:

```bash
cd video
npm run dev
# or: npm start
```
*Opens automatically at `http://localhost:3000`.*

---

### 2. Render Full 60s Demo Video (MP4)
Render the complete 1080p demo video to `video/out/paymesh-demo.mp4`:

```bash
cd video
npm run render
```

---

### 3. Render 15s Teaser Video (MP4)
Render the 15-second teaser video to `video/out/paymesh-teaser.mp4`:

```bash
cd video
npm run render:teaser
```

---

### 4. Render a Single High-Resolution Still Frame
Render an individual frame (e.g. for video thumbnail or presentation slide):

```bash
cd video
npm run still
```
*Outputs to `video/out/still-preview.png`.*

---

## 📁 Directory Structure

```
video/
├── package.json              # Remotion CLI, React, TypeScript scripts
├── remotion.config.ts        # Rspack bundler and headless Chromium configs
├── tsconfig.json             # TypeScript compiler options
├── public/
│   └── screenshots/          # 7 high-res UI screenshots from docs/assets/
│       ├── 01-agent-workspace.png
│       ├── 02-l402-challenge.png
│       ├── 03-unlocked-intelligence.png
│       ├── 04-spending-policy.png
│       ├── 05-marketplace-catalogue.png
│       ├── 06-financial-ledger.png
│       └── 07-merchant-studio.png
└── src/
    ├── index.ts              # Remotion registration entrypoint
    ├── Root.tsx              # Composition definitions (width, height, fps, frames)
    ├── PayMeshDemo.tsx       # 6-scene sequential timeline for 60s pitch
    ├── PayMeshTeaser.tsx     # 4-scene rapid teaser
    ├── types.ts              # Slide metadata and scene type definitions
    ├── components/
    │   ├── NeoCard.tsx       # Neo-tech card container with tactile drop-shadow
    │   └── HeaderBadge.tsx   # Top-bar status badges and pills
    └── scenes/
        ├── IntroScene.tsx        # Kinetic logo reveal and hackathon title
        ├── ProblemScene.tsx      # HTTP 402 Paywall bottleneck explanation
        ├── SolutionScene.tsx     # L402 + PayPal Vault v3 3-step solution
        ├── ShowcaseScene.tsx     # Animated walkthrough of all 7 UI screens
        ├── ArchitectureScene.tsx # FinTech, MCP, and security deep dive
        └── OutroScene.tsx        # GitHub links and hackathon closing card
```

---

## 🎨 Customizing the Video

1. **Change Scene Durations**: Edit the frame ranges in `video/src/PayMeshDemo.tsx` `<Sequence from={...} durationInFrames={...}>`.
2. **Update Slide Content**: Edit `slides` array in `video/src/scenes/ShowcaseScene.tsx` to alter descriptions, titles, or badges.
3. **Add Audio / Background Music**: Place an MP3 file into `video/public/audio.mp3` and include `<Audio src={staticFile("audio.mp3")} />` inside `PayMeshDemo.tsx`.
