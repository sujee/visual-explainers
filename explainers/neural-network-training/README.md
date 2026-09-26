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
./render.sh             # → workspace/preview/<timestamp>/  (4K landscape ~1:55 + Short ~0:57, with and without music)
./render.sh v7 draft    # quick 720p draft → workspace/preview/v7/
```

## Customize

Edit `brief.md` and ask your coding agent to adapt the explainer, or modify the source directly: the animation is in `src/scene.py`, the music in `src/music.py`. 

Once you're happy with a version, ask the agent to *prepare the Repro Bundle* before committing.
