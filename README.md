# Visual Explainers

Open-source, reproducible visual explainers for AI, software, and technical concepts.

**Watch them. Reproduce them. Remix them.**

### [▶ YouTube Playlist](https://www.youtube.com/playlist?list=PLUs9fKO_C_uw)

### [Browse the explainers](#explainers) · [Reproduce one](#explore-and-reproduce-an-explainer) · [Create your own](#create-a-new-explainer)

The code and templates are under [Apache-2.0](LICENSE). The original videos and soundtracks are licensed under [CC BY 4.0](LICENSE-CONTENT). If you build something cool with it, a link back to this project is always appreciated, but not required for the code.

Note: some videos / content may not by fully open source.  Check the notes.

## Working with Agents

[AGENTS.md](AGENTS.md)

## Explore and reproduce an explainer

Each explainer is self-contained.

**Yourself:**

```bash
git clone https://github.com/sujee/visual-explainers.git
cd visual-explainers/explainers/neural-network-training
# install the prerequisites listed in its README.md, then:
./render.sh          # all deliverables, final quality (4K, takes a while)
./render.sh draft    # quick draft preview
```

**With a coding agent:** start it in the explainer's folder (or the repository root) and ask:

> Read AGENTS.md and README.md. Install the prerequisites and render the final video.

## Create a new explainer

Start a coding agent in the repository root (the new explainer's folder doesn't exist yet) and ask, for example:

> Create a new explainer about prefill vs decode.

It starts by writing a `brief.md` for you to review, then renders drafts (`v1`, `v2`, …) for your feedback. Once you approve a version, ask it to *prepare the Repro Bundle* before committing.

Or start by hand: copy [`templates/explainer/`](templates/explainer/) to `explainers/<name>/` and fill in the placeholders.

## Explainers

All the videos are in one [YouTube playlist](https://www.youtube.com/playlist?list=PLUs9fKO_C_uw).

| Explainer | What it teaches | Watch | Built with |
|---|---|---|---|
| [neural-network-training](explainers/neural-network-training/) | How a network learns - forward pass, error, backpropagation, weight updates | [Video](https://youtu.be/BJC3FuMHRvs) · [Short](https://youtube.com/shorts/0fBcojHo-SI) · [4K release](https://github.com/sujee/visual-explainers/releases/tag/neural-network-training-v1) | Manim (Python) |
| [neural-network-training-cartoon](explainers/neural-network-training-cartoon/) | The same explainer in a bright cartoon style, with a bouncy soundtrack | [Video](https://youtu.be/11BqOZ9HJeY) ·   [Short](https://youtube.com/shorts/wK1GNcRc8jY) · [4K release](https://github.com/sujee/visual-explainers/releases/tag/neural-network-training-cartoon-v1) | Manim (Python) |
