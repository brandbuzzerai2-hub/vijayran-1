# The Vijayran Palace — Suján Style Luxury Heritage Resort Website

A high-performance, minimalist luxury heritage resort website for **The Vijayran Palace by Royal Quest Resorts** (Kukas, Jaipur), crafted with the aesthetic DNA and motion system of **[thesujanlife.com](https://thesujanlife.com/)**.

## Features & Highlights

- **Authentic Typography**: Full typographic suite of **Minion Pro** (display serif for headings & editorial quotes) and **Brandon Grotesque** (geometric sans-serif for navigation, labels, and buttons).
- **Motion & Interaction Engine**:
  - **Lenis Smooth Scroll**: Inertial, weighted scroll momentum synchronized with GSAP's ticker.
  - **Hero Scale Scrub**: Full-bleed background video zooms smoothly (`scale: 1.0` -> `1.25`) on scroll via GSAP ScrollTrigger.
  - **Line-Masked Text Reveals (`.d_y`)**: Heading lines glide up cleanly from masked containers as they enter the viewport.
  - **Dual-Text Rolling Hover**: Interactive CTAs feature Suján's 2-tier rolling text animation (`transition: transform 0.6s cubic-bezier(0.65, 0, 0.35, 1)`).
  - **Sticky Story Gallery Parallax**: Staggered floating photos drifting with individual `data-speed` values around sticky narrative copy.
  - **Continuous Moving Image Ribbon**: Infinite 75s horizontal gliding marquee above the footer with pause-on-hover.
- **Clean Minimalist Navigation**: Signature 3-element header (Menu trigger, centered brand crest wordmark, and gold Book Now dropdown) without distracting top bars.
- **Live Weather Widget**: Real-time temperature, condition, apparent temp, humidity, wind, sunset, and 5-day daily forecast for Kukas, Jaipur via the Open-Meteo API.
- **Instagram Feed Widget**: Embedded `@vijayranresorts` feed with high-res photography grid, follower badge, and expander.
- **Verbatim Old Site Content & SEO**: 20 static pages matching the exact URL hierarchy of `royalquestresorts.com`.

## Quick Start (Local Server)

Run the included multi-threaded HTTP server with HTTP 206 `Range` support (for smooth video streaming):

```bash
python server.py
```

Then visit [http://localhost:8000/](http://localhost:8000/) in your browser.

## Rebuilding Pages

To modify content, edit `build.py` and run:

```bash
python build.py
```
