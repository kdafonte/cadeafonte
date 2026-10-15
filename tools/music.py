"""Trilha original e livre de direitos: pad suave em Lá menor + pulso discreto."""
import sys, wave, numpy as np

dur = float(sys.argv[1]); out = sys.argv[2]
sr = 44100
t = np.arange(int(sr * dur)) / sr
bpm = 76; beat = 60 / bpm; bar = 4 * beat
# Am - F - C - G (notas em Hz)
chords = [[220.00, 261.63, 329.63], [174.61, 220.00, 261.63], [196.00, 261.63, 329.63], [196.00, 246.94, 293.66]]
pad = np.zeros_like(t)
for i in range(int(dur / bar) + 1):
    s, e = int(i * bar * sr), int(min((i + 1) * bar, dur) * sr)
    if s >= len(t): break
    seg = t[s:e] - i * bar
    env = np.minimum(1, seg / 0.8) * np.minimum(1, (bar - seg) / 0.8)
    for f in chords[i % 4]:
        for h, a in ((1, 1.0), (2, 0.25), (0.5, 0.35)):
            pad[s:e] += a * env * np.sin(2 * np.pi * f * h * seg + 0.3 * np.sin(2 * np.pi * 0.2 * seg))
# pulso grave a cada tempo
pulse = np.zeros_like(t)
for k in range(int(dur / beat) + 1):
    s = int(k * beat * sr); n = int(0.35 * sr)
    if s >= len(t): break
    seg = np.arange(min(n, len(t) - s)) / sr
    pulse[s:s + len(seg)] += np.sin(2 * np.pi * 55 * seg) * np.exp(-seg * 9) * (1.0 if k % 2 == 0 else 0.6)
mix = 0.11 * pad / 3 + 0.35 * pulse
# fade in/out
fade = np.minimum(1, t / 1.5) * np.minimum(1, (dur - t) / 2.0)
mix = mix * fade
mix = mix / np.max(np.abs(mix)) * 0.7
st = np.stack([mix, np.roll(mix, 220)], axis=1)
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
