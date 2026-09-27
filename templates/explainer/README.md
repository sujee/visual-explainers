# <Title>

<One sentence: what the explainer teaches.>

The intent (what it teaches, for whom, and what must come across) is in [brief.md](brief.md). The approved implementation is in `src/`.

▶ Watch the finished explainer: <link, or *(coming soon)*>

## Prerequisites

<Only what the lockfile can't install: the package manager, system packages (at least ffmpeg, which render.sh uses), fonts. Exact commands, with the tested OS noted.>

## Run it yourself

```bash
./render.sh            # → workspace/preview/<timestamp>/  (<what the final deliverables are>)
./render.sh draft      # <what a draft produces>  → workspace/preview/<timestamp>/
./render.sh draft v2   # same, named version      → workspace/preview/v2/
./render.sh final v2   # everything, final quality → workspace/preview/v2/
```

## Customize

- **Through the brief:** edit `brief.md` (e.g. <an example change and the brief section it goes under>), then ask your agent to *update the explainer and render a draft*. Give notes on each draft until you approve one, then render it at final quality: `./render.sh final <version>`.
- **Directly:** edit <the main source files>, then run `./render.sh draft <next version>`.

## Verification

Before committing, ask your agent for the *fresh-clone test* (or *repro test*): it renders from a copy of only the files Git tracks and checks that the output matches the approved version. It takes one full final render.
