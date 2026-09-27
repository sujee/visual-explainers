# How a Neural Network Learns

A visual explainer of how a neural network learns from its mistakes: forward pass, error, backpropagation, and weight updates.

The intent (what it teaches, for whom, and what must come across) is in [brief.md](brief.md). The approved implementation is in `src/`.

▶ Watch the finished explainer: *(coming soon)*

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/). It installs Python 3.11 and the pinned packages itself.
- System packages for Manim, audio and the font:

```bash
sudo apt-get install -y libcairo2-dev libpango1.0-dev pkg-config ffmpeg sox fonts-inter   # Debian/Ubuntu (tested)
brew install cairo pango pkg-config ffmpeg sox && brew install --cask font-inter          # macOS (untested)
```

## Run it yourself

```bash
./render.sh            # → workspace/preview/<timestamp>/  (4K landscape ~1:55 + Short ~0:59, with and without music)
./render.sh draft      # quick 720p draft, both formats → workspace/preview/<timestamp>/
./render.sh draft v7   # same, named version            → workspace/preview/v7/
./render.sh final v7   # everything, final quality      → workspace/preview/v7/
```

## Customize

- **Through the brief:** edit `brief.md` (e.g. a color preference under **Style**), then ask your agent to *update the explainer and render a draft*. Give notes on each draft until you approve one, then render it at final quality: `./render.sh final <version>`.
- **Directly:** edit `src/scene.py` (animation; colors are at the top) or `src/music.py`, then run `./render.sh draft <next version>`.

## Verification

Before committing, ask your agent for the *fresh-clone test* (or *repro test*): it renders from a copy of only the files Git tracks and checks that the output matches the approved version. It takes one full final render.
