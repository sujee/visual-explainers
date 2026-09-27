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

- Edit `brief.md` and ask your coding agent to adapt the explainer.
- For a small tweak, skip the brief: edit the source directly and run `./render.sh draft <next version>`. The animation is in `src/scene.py` (colors are named hex values at the top), the music in `src/music.py`.

To change it through the brief:
1. Edit `brief.md`, e.g. add a color preference under **Style**.
2. Ask your agent: *"I updated brief.md. Update the explainer to match and render a draft."*
3. Review the draft in `workspace/preview/vN/` and give notes; each round bumps the version (vN+1, …).
4. Once you approve a version, render it at final quality: `./render.sh final vN`.

Once you're happy with a version, ask the agent to *prepare the Repro Bundle* before committing.
