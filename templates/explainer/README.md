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

- Edit `brief.md` and ask your coding agent to adapt the explainer.
- For a small tweak, skip the brief: edit the source directly and run `./render.sh draft <next version>`. <Name the main source files.>

To change it through the brief:
1. Edit `brief.md`, e.g. <an example change and the brief section it goes under>.
2. Ask your agent: *"I updated brief.md. Update the explainer to match and render a draft."*
3. Review the draft in `workspace/preview/vN/` and give notes; each round bumps the version (vN+1, …).
4. Once you approve a version, render it at final quality: `./render.sh final vN`.

Once you're happy with a version, ask the agent to *prepare the Repro Bundle* before committing.
