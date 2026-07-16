# Specification

> **Source of truth.** GitHub Issues are intake; this file is the contract the
> agent obeys. When the two disagree, this file (and its owners) decide.

## Overview

The image gallery system consists of a logical Core and a Visual Shell. The Python Core validates and serves photo metadata and state, while the HTML/CSS/JS Shell displays this data and handles presentational layouts and micro-interactions.

## Domain model

- **Request** — the input. Fields:
  - `event: str` — the event triggering the request (one of `"load_gallery"`, `"hover_photo"`, `"click_photo"`)
  - `photo_id: str` — optional identifier of a specific photo
  - `viewport_width: int` — the screen width in pixels
- **Photo** — the core photo model. Fields:
  - `id: str` — unique photo identifier
  - `title: str` — display name of the photo
  - `category: str` — category classification (e.g., `"Nature"`, `"Urban"`, `"Minimal"`)
  - `image_url: str` — link to high-resolution asset
  - `likes: int` — current like count (defaults to `0`)
- **Decision** — the output. Fields:
  - `outcome: str` — the logical decision (one of `"SERVE_PHOTOS"`, `"ZOOM_PHOTO"`, `"OPEN_LIGHTBOX"`)
  - `photos: list[Photo]` — the list of photos relevant to the outcome (populated for `SERVE_PHOTOS`, or single photo in list for `OPEN_LIGHTBOX`)
  - `rule_ids: list[str]` — the rules that determined the outcome
  - `evaluated_at: str` — timestamp of evaluation

## Global constraints

- **Photo Collection Invariant** — The system must host exactly 6 default photos on initial gallery load.
- **Photo Metadata Completeness** — Every `Photo` record served must have non-empty `id`, `title`, `category`, and `image_url` fields, and `likes >= 0`.
- **Evaluation Determinism** — Serve and action evaluations are deterministic: same `Request` $\rightarrow$ same `Decision`.
- **Mobile Breakpoint** — Viewport widths strictly less than `768` pixels trigger a mobile layout state.
- **Hover Scale Factor** — Visual scaling transitions on hover must be exactly `1.05` times the standard card scale.

## Rules

### R1: Served Default Photos on Load

- **Behavior:** On a `"load_gallery"` event, the Core serves a collection of exactly 6 default photos, each populated with valid ID, title, category, image URL, and a default like count of 0.
- **Example:** `evaluate(event="load_gallery", viewport_width=1200)` → `SERVE_PHOTOS` with 6 valid photos, `["R1"]`
- **Precedence:** Overrides none. Defers to none.
- **Source:** issue #9

### R2: Mobile Grid Collapse

- **Behavior:** On gallery load, the Visual Shell queries the served photo data. If the viewport width is strictly less than 768px, the grid collapses to a single-column layout; otherwise, it renders in a multi-column CSS responsive grid.
- **Example:** `evaluate(event="load_gallery", viewport_width=375)` → `SERVE_PHOTOS` with mobile single-column layout instructions, `["R1", "R2"]`
- **Precedence:** Overrides R1 on mobile viewports.
- **Source:** issue #10

### R3: Smooth Hover Micro-Animation

- **Behavior:** When the cursor hovers over any photo card, the image smoothly zooms to a scale of 1.05 using a CSS transition effect.
- **Example:** `evaluate(event="hover_photo", photo_id="photo_1", viewport_width=1200)` → `ZOOM_PHOTO`, `["R3"]`
- **Precedence:** Overrides none.
- **Source:** issue #10

### R4: Interactive Lightbox View

- **Behavior:** When a visitor clicks on any photo card, a full-screen dark semi-transparent overlay (Lightbox) opens, displaying the high-resolution image, title, and category badge. Clicking the "X" button or the background overlay closes it smoothly.
- **Example:** `evaluate(event="click_photo", photo_id="photo_1", viewport_width=1200)` → `OPEN_LIGHTBOX` with the matched photo in `photos` array, `["R4"]`
- **Precedence:** Overrides none.
- **Source:** issue #6

## Precedence order

Rules are evaluated as an ordered list, with the highest priority first:

1. R4 — Interactive Lightbox View
2. R3 — Smooth Hover Micro-Animation
3. R2 — Mobile Grid Collapse
4. R1 — Served Default Photos on Load


## Glossary

- **Photo Model** — The core logical representation of a photo's metadata and state.
- **Visual Shell** — The frontend interface (HTML/CSS/JS) that interacts with users and renders Core data.
- **Mobile Breakpoint** — The screen width boundary (768px) that separates mobile single-column layout from tablet/desktop multi-column grid layouts.
- **Smooth Hover Zoom** — A presentational micro-animation that scales a photo card's image to 1.05 times its size over a smooth transition duration.
