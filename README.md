# Visual Explainers

Open-source, reproducible visual explainers for AI and software concepts.

**Watch them. Reproduce them. Remix them.**

### [▶ Browse the explainers](#explainers) · [Reproduce one](#explore-and-reproduce-an-explainer) · [Create your own](#create-a-new-explainer)

Working with a coding agent? The rules it follows are in [AGENTS.md](AGENTS.md).

The code and templates are under [Apache-2.0](LICENSE). The original videos and soundtracks are licensed under [CC BY 4.0](LICENSE-CONTENT). If you build something cool with it, a link back to this project is always appreciated, but not required for the code.

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

The system packages need `sudo`, so the agent may ask you to run that one command yourself.

## Create a new explainer

Start a coding agent in the repository root (the new explainer's folder doesn't exist yet) and ask, for example:

> Create a new explainer about prefill vs decode.

It starts by writing a `brief.md` for you to review, then renders drafts (`v1`, `v2`, …) for your feedback. Once you approve a version, ask it to *prepare the Repro Bundle* before committing.

Or start by hand: copy [`templates/explainer/`](templates/explainer/) to `explainers/<name>/` and fill in the placeholders.

## Explainers

| Explainer | What it teaches | Watch | Built with |
|---|---|---|---|
| [neural-network-training](explainers/neural-network-training/) | How a network learns from its mistakes: forward pass, error, backpropagation, weight updates | *coming soon* | Manim (Python) |
