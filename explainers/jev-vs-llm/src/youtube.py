"""YouTube descriptions for both videos, with chapters from the scene's own timeline.

Usage: uv run python src/youtube.py workspace/tmp/events_landscape.json workspace/tmp/events_portrait.json
Prints Markdown, which render.sh saves as youtube-description.md: a title, the landscape description
with chapter timestamps (one per section, the first starting at 0:00 so the title card is part of
it), and the Short's description. Edit the text below;
the timestamps come from the render, so they always match the video. Fails if the chapters break
YouTube's rules (first at 0:00, at least 3, each at least 10 seconds), since YouTube would then show none.
"""
import json
import sys

REPO = "https://github.com/sujee/visual-explainers/tree/main/explainers/jev-vs-llm"
SOURCE = "https://typesafe.ai/blog/introducing-system-one-models-and-jev"

TITLE = "Jev vs. LLMs: a model that decides instead of writing"

ABOUT = """\
Most AI models write their answers. Jev, TypeSafe AI's new "System One" model, doesn't write at all: it reads \
your program's state and returns typed decisions, with a calibrated probability for every option. This \
explainer shows what that means for developers: why it's fast, how to act on its confidence, and where an LLM \
is still the right tool."""

NOTES = f"""\
Facts and performance figures are TypeSafe AI's own, from its launch post (September 2026): {SOURCE}
They are the company's benchmarks; no independent evaluation had been published at the time of making.
Probabilities and counts shown on screen are illustrative.

Source, brief and how to reproduce or remix it: {REPO}
Video and music: CC BY 4.0. Code: Apache-2.0.

Created by sujee.dev"""

SHORT = f"""\
Most AI models write. Jev doesn't: it picks from the answers you define, with a probability for each, in one pass.

Full 2-minute explainer: <link to the full video>
Facts from TypeSafe AI's launch post: {SOURCE}

Created by sujee.dev"""


def stamp(t):
    t = int(t)   # floor: the chapter starts at or just before its title card
    return f"{t // 60}:{t % 60:02d}"


land = json.load(open(sys.argv[1]))
chapters = [[t, title] for t, title in land.get("chapters", [])]
if chapters:
    chapters[0][0] = 0.0   # the title card belongs to the first chapter
ends = [t for t, _ in chapters[1:]] + [land["end"]]
problems = []
if len(chapters) < 3:
    problems.append(f"only {len(chapters)} chapters (YouTube needs at least 3)")
for (t, title), e in zip(chapters, ends):
    if int(e) - int(t) < 10:
        problems.append(f"chapter '{title}' at {stamp(t)} is {e - t:.1f} s (YouTube needs at least 10 s)")
if problems:
    sys.exit("youtube.py: chapters would be ignored by YouTube:\n  " + "\n  ".join(problems))

print(f"# YouTube descriptions\n")
print(f"## Full video ({stamp(land['end'])})\n")
print(f"**Title:** {TITLE}\n")
print("```text")
print(ABOUT + "\n")
print("Chapters")
for t, title in chapters:
    print(f"{stamp(t)} {title}")
print("\n" + NOTES)
print("```\n")
if len(sys.argv) > 2:
    short = json.load(open(sys.argv[2]))
    print(f"## Short ({stamp(short['end'])})\n")
    print("**Title:** Most AI models write. Jev doesn't.\n")
    print("```text")
    print(SHORT)
    print("```")
