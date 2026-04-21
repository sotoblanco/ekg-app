# EKG Master

An interactive programmed-learning web application based on **Dubin's Rapid Interpretation of EKGs, 6th Edition**.

Built as a static single-page app that runs entirely on GitHub Pages — no backend, no build step, no dependencies to install.

---

## What It Is

The app follows Dubin's proven fill-in-the-blank (programmed learning) format:

1. A visual aid is shown (EKG strip, diagram, or schematic).
2. A sentence with a blank appears — type your answer.
3. If correct, a "Continue" button unlocks (or press Enter / →).
4. Hints and a reveal option are always available.

Progress is tracked per session (localStorage-free — resets on reload by design, encouraging re-reading).

---

## Chapters Covered

| # | Chapter | Frames |
|---|---------|--------|
| 1 | Basic Principles | 12 |
| 2 | Recording the EKG | 10 |
| 3 | Rate | 8 |
| 4 | Rhythm | 8 |
| 5 | The P Wave | 8 |
| 6 | The PR Interval | 8 |
| 7 | The QRS Complex | 9 |
| 8 | The ST Segment | 7 |
| 9 | The T Wave | 7 |
| 10 | Axis | 8 |
| 11 | Hypertrophy | 8 |
| 12 | Infarction | 9 |
| 13 | Arrhythmias | 9 |

**Total: 109 programmed learning frames**

---

## Deploying to GitHub Pages

```bash
# 1. Create a GitHub repo named anything (e.g., app-ekg or ekg-master)
# 2. Push this directory
git add .
git commit -m "feat: initial EKG Master app"
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main

# 3. In GitHub: Settings > Pages > Source: Deploy from branch > main / root
# 4. Your app will be live at: https://<your-username>.github.io/<repo-name>/
```

---

## Structure

```
app-ekg/
├── index.html        # The entire app (self-contained)
├── README.md
├── .gitignore
└── scripts/          # PDF analysis tools (dev only)
    └── extract_pdf.py
```

## Technology

- React 18 (UMD/CDN — no build step)
- Tailwind CSS (CDN)
- Lucide React (CDN)
- Babel Standalone (JSX transpilation in-browser)
- Google Fonts (Inter, Outfit)

All assets loaded from CDN. Works offline after first load with a service worker (not included by default).

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Enter` or `→` | Continue to next frame (when correct) |
| `←` | Go back one frame |
| `Escape` | Close mobile sidebar |

---

## Notes on PDF

The original PDF (`318216295-Dubin-Rapid-Interpretation-of-EKGs-6th-Ed.pdf`) is a fully scanned image-based document. Text cannot be extracted programmatically. The content in this app was authored based on the well-established published content of Dubin's 6th edition.

The PDF is excluded from the repository (`.gitignore`).
