"""Procedural bouncy cartoon backing track, synced to the scene's timeline events.

Usage: uv run python src/music.py workspace/tmp/events_landscape.json out.wav
Structure: oom-pah bass + xylophone tune from the start -> snare/woodblock groove at pass 1 ->
"wah-wah" trombone on wrong answers, slide whistle when the error flows backward,
xylophone run on "correct" -> "shave and a haircut" button at "end".
Everything is synthesized here (no samples, no licensing); the tune is original, the button is traditional.
"""
import json
import subprocess
import sys
import wave
import os

import numpy as np

SR = 48000
BPM = 132.0
BEAT = 60.0 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(5)

ev = json.load(open(sys.argv[1]))
out = sys.argv[2]
DUR = ev["end"] + 1.0
N = int(DUR * SR)


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def add(buf, start, sig):
    i = int(start * SR)
    if i >= len(buf) or i < 0:
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i]


def secs(n_sec):
    return np.arange(int(n_sec * SR)) / SR


# ---------------------------------------------------------------- instruments
def xylo(m, amp=1.0):
    """Bright mallet: fundamental + inharmonic 3rd/4th partials, fast decay."""
    tt = secs(1.0)
    f = hz(m)
    s = (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 7)
         + 0.35 * np.sin(2 * np.pi * f * 3.93 * tt) * np.exp(-tt * 22)
         + 0.15 * np.sin(2 * np.pi * f * 9.2 * tt) * np.exp(-tt * 40))
    return s * np.minimum(1, tt / 0.002) * amp


def tuba(m, length, amp=1.0):
    """Round, buzzy low brass for the oom-pah bass."""
    tt = secs(length + 0.08)
    f = hz(m)
    s = sum(np.sin(2 * np.pi * f * h * tt) / h ** 1.3 for h in range(1, 7))
    e = np.minimum(1, tt / 0.018) * np.exp(-tt * 3.0)
    e *= np.clip((length + 0.08 - tt) / 0.08, 0, 1)
    return s * e * amp


def plink(chord, amp=1.0):
    """Short, bouncy piano-ish chord for the 'pah'."""
    tt = secs(0.35)
    s = np.zeros(len(tt))
    for m in chord:
        f = hz(m)
        s += (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(4 * np.pi * f * tt) * np.exp(-tt * 15))
    return s * np.minimum(1, tt / 0.003) * np.exp(-tt * 14) * amp


def brass(m_from, length, amp=1.0, vib=0.0, bend=0.0):
    """Muted trombone-ish tone with optional vibrato and downward bend (for 'wah-wah')."""
    tt = secs(length)
    f = hz(m_from) * 2 ** ((-bend * tt / length) / 12) * (1 + vib * np.sin(2 * np.pi * 5.5 * tt))
    ph = 2 * np.pi * np.cumsum(f) / SR
    wah = 0.5 + 0.5 * np.minimum(1, tt / 0.12)  # brightness opens up: the "wah"
    s = sum(np.sin(h * ph) * (wah ** (h - 1)) / h for h in range(1, 9))
    e = np.minimum(1, tt / 0.03) * np.clip((length - tt) / 0.06, 0, 1)
    return s * e * amp


# ---------------------------------------------------------------- harmony + tune (C major, original)
# I - vi - IV - V7, one chord per bar
ROOTS = [36, 33, 29, 31]
FIFTHS = [43, 40, 36, 38]
CHORDS = [[60, 64, 67], [57, 60, 64], [57, 60, 65], [59, 62, 65, 67]]
# tune: (beat offset, midi, length in beats) per bar; a bouncy, hoppy line
TUNE = [
    [(0, 72, 0.5), (0.5, 76, 0.5), (1, 79, 0.5), (2, 76, 0.5), (2.5, 72, 0.5), (3, 74, 0.5), (3.5, 76, 0.5)],
    [(0, 76, 0.5), (0.5, 72, 0.5), (1, 69, 1.0), (2.5, 72, 0.5), (3, 76, 0.5), (3.5, 77, 0.5)],
    [(0, 77, 0.5), (0.5, 81, 0.5), (1, 77, 0.5), (1.5, 76, 0.5), (2, 74, 0.5), (3, 72, 0.5), (3.5, 74, 0.5)],
    [(0, 79, 0.5), (0.5, 77, 0.5), (1, 74, 0.5), (1.5, 71, 0.5), (2, 74, 1.0), (3.5, 67, 0.5)],
]
# answer phrase for every other 4-bar loop, so the tune doesn't just repeat
TUNE_B = [
    [(0, 79, 0.5), (1, 79, 0.5), (1.5, 76, 0.5), (2, 72, 0.5), (3, 76, 0.5), (3.5, 79, 0.5)],
    [(0, 81, 0.5), (0.5, 79, 0.5), (1, 76, 0.5), (2, 72, 1.0), (3.5, 69, 0.5)],
    [(0, 72, 0.5), (0.5, 77, 0.5), (1, 81, 0.5), (2, 84, 0.5), (2.5, 81, 0.5), (3, 77, 0.5)],
    [(0, 79, 0.5), (1, 74, 0.5), (1.5, 77, 0.5), (2, 71, 0.5), (2.5, 74, 0.5), (3, 79, 0.5), (3.5, 83, 0.5)],
]

bass = np.zeros(N)
comp = np.zeros(N)
lead = np.zeros(N)
drums = np.zeros(N)
fx = np.zeros(N)

t_groove = ev.get("pass1", 8.0)
t_end = ev["end"]
BUTTON = 7 * BEAT + 0.4              # length of the final "shave and a haircut" button
t_button = t_end - BUTTON - 0.9
t_stop = t_button - 0.15            # the groove stops just before the button

nbars = int(np.ceil(DUR / BAR)) + 1
for b in range(nbars):
    t0 = b * BAR
    if t0 >= t_stop:
        break
    c = b % 4
    groove = t0 + BAR > t_groove

    def beat_ok(bt):
        return t0 + bt * BEAT < t_stop

    # --- oom-pah: tuba on 1 and 3 (root, fifth), plinky chords on 2 and 4
    for bt, m in ((0, ROOTS[c]), (2, FIFTHS[c])):
        if beat_ok(bt):
            add(bass, t0 + bt * BEAT, tuba(m, BEAT * 0.7, 0.20))
    if groove and b % 2 == 1 and beat_ok(3.5):  # walk-up pickup into the next chord
        add(bass, t0 + 3.5 * BEAT, tuba(ROOTS[(c + 1) % 4] - 1, BEAT * 0.4, 0.14))
    for bt in (1, 3):
        if beat_ok(bt):
            add(comp, t0 + bt * BEAT, plink(CHORDS[c], 0.05))
    # --- xylophone tune (A phrase, then B phrase)
    phrase = TUNE if (b // 4) % 2 == 0 else TUNE_B
    for bt, m, ln in phrase[c]:
        if beat_ok(bt):
            add(lead, t0 + bt * BEAT, xylo(m, 0.11))
            add(lead, t0 + bt * BEAT, xylo(m - 12, 0.035))  # low double for body

    if not groove:
        continue
    # --- drums: soft kick, snappy snare on 2/4, brushy hats, woodblock pops
    for bt in (0, 2):
        if beat_ok(bt):
            tt = secs(0.3)
            f = 55 + 90 * np.exp(-tt * 35)
            add(drums, t0 + bt * BEAT, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 12) * 0.45)
    for bt in (1, 3):
        if beat_ok(bt):
            tt = secs(0.16)
            nz = rng.normal(0, 1, len(tt))
            nz = nz - np.convolve(nz, np.ones(6) / 6, mode="same")
            body = np.sin(2 * np.pi * 220 * tt) * np.exp(-tt * 35)
            add(drums, t0 + bt * BEAT, (nz * 0.4 * np.exp(-tt * 30) + body * 0.35) * 0.35)
    for k in range(8):
        if beat_ok(k / 2):
            tt = secs(0.05)
            nz = np.diff(rng.normal(0, 1, len(tt) + 1))
            add(drums, t0 + k * BEAT / 2, nz * np.exp(-tt * 80) * (0.03 if k % 2 == 0 else 0.018))
    for bt in (1.5, 3.5) if b % 2 else (3.5,):
        if beat_ok(bt):
            tt = secs(0.12)
            wb = (np.sin(2 * np.pi * 880 * tt) + 0.5 * np.sin(2 * np.pi * 1320 * tt)) * np.exp(-tt * 45)
            add(drums, t0 + bt * BEAT, wb * 0.07)

# ---------------------------------------------------------------- cartoon stingers
duck = np.ones(N)


def dip(t, length, depth=0.35):
    """Pull the band down while a stinger plays."""
    tt = secs(length)
    ramp = 0.08
    seg = 1 - (1 - depth) * np.clip(np.minimum(tt / ramp, (length - tt) / ramp), 0, 1)
    i = int(t * SR)
    j = min(N, i + len(seg))
    duck[i:j] = np.minimum(duck[i:j], seg[: j - i])


# wrong answer: "wah wah wah waaah" (descending semitones, last note bends and wobbles)
for key in ("wrong1", "wrong2"):
    if key in ev:
        t = ev[key]
        for k, m in enumerate((58, 57, 56)):
            add(fx, t + k * 0.28, brass(m, 0.26, 0.09))
        add(fx, t + 3 * 0.28, brass(55, 0.95, 0.09, vib=0.012, bend=0.6))
        dip(t, 2.0)

# backpropagation: a slide whistle down, as the error travels backward
for key in ("backprop1", "backprop2"):
    if key in ev:
        tt = secs(0.7)
        f = 1400 * 2 ** (-1.4 * tt / 0.7) * (1 + 0.01 * np.sin(2 * np.pi * 7 * tt))
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, tt / 0.04) * np.clip((0.7 - tt) / 0.1, 0, 1)
        add(fx, ev[key] + 0.2, s * 0.05)

# correct answer: xylophone run up two octaves, then a bright C major chord
tc = ev.get("correct")
if tc is not None:
    run = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84]
    for k, m in enumerate(run):
        add(fx, tc + k * 0.035, xylo(m, 0.07))
    for m in (72, 76, 79, 84):
        add(fx, tc + len(run) * 0.035 + 0.02, xylo(m, 0.09))
    dip(tc, 1.2, 0.5)

# the button: "shave and a haircut ... two bits" (traditional), band hits the last two notes; offsets in beats
BTN = [(0, 72, 1), (1, 67, 0.5), (1.5, 67, 0.5), (2, 69, 1), (3, 67, 1), (5, 71, 1), (6, 72, 1)]
for bt, m, ln in BTN:
    add(lead, t_button + bt * BEAT, xylo(m, 0.14))
    add(lead, t_button + bt * BEAT, xylo(m - 12, 0.05))
for bt, root, ch in ((5, 31, [59, 62, 67]), (6, 36, [60, 64, 67, 72])):
    add(bass, t_button + bt * BEAT, tuba(root, BEAT * (0.4 if bt == 5 else 1.2), 0.22))
    add(comp, t_button + bt * BEAT, plink(ch, 0.07))
tt = secs(0.3)
add(drums, t_button + 6 * BEAT, np.sin(2 * np.pi * np.cumsum(55 + 90 * np.exp(-tt * 35)) / SR) * np.exp(-tt * 12) * 0.5)

band = duck

def stereo(x, width=0.0, delay_ms=0.0):
    d = int(delay_ms * SR / 1000)
    L = x.copy()
    R = np.concatenate([np.zeros(d), x[:-d]]) if d else x.copy()
    return np.stack([L * (1 - width), R * (1 + width)], axis=1)


wet = stereo(lead * band, 0.12, 6) + stereo(comp * band, -0.1, 9) + stereo(fx, 0, 4)
dry = stereo(bass * band) + stereo(drums * band)

# sox -R (repeatable mode) keeps its dither noise deterministic, so the same source gives the same audio.
tmp = os.path.join(os.path.dirname(out) or ".", "_music_tmp")
os.makedirs(tmp, exist_ok=True)


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


write_wav(f"{tmp}/wet.wav", wet)
write_wav(f"{tmp}/dry.wav", dry)
subprocess.run(["sox", "-R", f"{tmp}/wet.wav", f"{tmp}/wet_rev.wav", "reverb", "30", "50", "60", "100", "10"], check=True)
fade_out = 0.5   # the button ends the tune; just a short tail fade
subprocess.run(["sox", "-R", "-m", f"{tmp}/wet_rev.wav", f"{tmp}/dry.wav", f"{tmp}/mix.wav",
                "lowpass", "9000", "trim", "0", f"{t_end:.3f}",       # end exactly with the video,
                "fade", "t", "0.3", f"{t_end:.3f}", f"{fade_out}"], check=True)  # fully faded out
# Loudness-normalize to -14 LUFS integrated, true peak <= -1 dBTP (see AGENTS.md).
# Two passes: measure, then apply linearly. The peak target leaves headroom for AAC encoding.
LN = "loudnorm=I=-14:TP=-2:LRA=11"
probe = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{tmp}/mix.wav", "-af", LN + ":print_format=json",
                        "-f", "null", "-"], check=True, capture_output=True, text=True).stderr
m = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
LN += (f":measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
       f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{tmp}/mix.wav", "-af", LN, "-ar", str(SR), out], check=True)
print("wrote", out, f"{DUR:.1f}s")
