"""Synthesize a subtle 33s ambient-tech bed (pad + pluck arp + soft kick/hat) and transition whooshes."""
import numpy as np, wave

SR, DUR, BPM = 44100, 33.0, 104
N = int(SR * DUR)
t = np.arange(N) / SR
beat = 60 / BPM
rng = np.random.default_rng(7)

def note(m): return 440 * 2 ** ((m - 69) / 12)

def lowpass(x, a):
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += a * (v - acc); y[i] = acc
    return y

# Chord progression Am - F - C - G, 2 bars each (8 beats)
chords = [[57, 60, 64, 69], [53, 57, 60, 65], [48, 55, 60, 64], [55, 59, 62, 67]]
bar = 4 * beat
pad = np.zeros(N)
for i in range(int(DUR / (2 * bar)) + 1):
    s, e = i * 2 * bar, (i + 1) * 2 * bar
    idx = (t >= s) & (t < e + 0.6)
    tt = t[idx] - s
    env = np.minimum(1, tt / 0.8) * np.clip((e + 0.6 - s - tt) / 0.6, 0, 1)
    for m in chords[i % 4]:
        f = note(m)
        for det in (-0.12, 0.12):
            pad[idx] += env * np.sin(2 * np.pi * f * (1 + det / 100) * tt + 0.3 * np.sin(2 * np.pi * 0.3 * tt))
pad *= 0.05

# Pluck arpeggio in 8ths
arp = np.zeros(N)
step = beat / 2
for k in range(int(DUR / step)):
    s = k * step
    ch = chords[int(s // (2 * bar)) % 4]
    m = ch[[0, 2, 1, 3, 2, 1, 3, 2][k % 8]] + 12
    n = int(0.35 * SR); i0 = int(s * SR)
    if i0 + n > N: break
    tt = np.arange(n) / SR
    arp[i0:i0 + n] += np.sin(2 * np.pi * note(m) * tt) * np.exp(-tt * 11) * (0.6 + 0.4 * np.sin(2 * np.pi * note(m) * 2 * tt))
arp *= 0.06

# Soft kick on beats, hats on offbeats (drums enter at 3s, i.e. after the hook)
drums = np.zeros(N)
kn = int(0.3 * SR); kt = np.arange(kn) / SR
kick = np.sin(2 * np.pi * (45 + 80 * np.exp(-kt * 30)) * kt) * np.exp(-kt * 9)
hn = int(0.05 * SR); hat = rng.standard_normal(hn) * np.exp(-np.arange(hn) / SR * 90)
hat = np.diff(hat, prepend=0)
for k in range(int(DUR / beat)):
    s = k * beat
    if s < 3.0 or s > 30.0: continue
    i0 = int(s * SR)
    if i0 + kn < N: drums[i0:i0 + kn] += kick * 0.22
    j0 = int((s + beat / 2) * SR)
    if j0 + hn < N: drums[j0:j0 + hn] += hat * 0.05

# Whooshes at scene changes
fx = np.zeros(N)
wn = int(0.7 * SR)
for s in (2.85, 11.85, 17.85, 23.85, 29.8):
    noise = lowpass(rng.standard_normal(wn), 0.08)
    env = np.sin(np.linspace(0, np.pi, wn)) ** 2
    i0 = int(s * SR); fx[i0:i0 + wn] += noise * env * 0.35

# Rising impact at CTA
mix = pad + arp + drums + fx
fade = np.minimum(1, t / 0.4) * np.clip((DUR - t) / 1.2, 0, 1)
mix *= fade
mix /= np.max(np.abs(mix)) * 1.05
st = np.stack([mix, np.roll(mix, 220)], 1)  # tiny stereo widening
with wave.open("audio/music.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
