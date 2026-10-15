"""Renderiza um post do Cadê a Fonte a partir de um arquivo JSON de especificação.

Uso:  python3 tools/render.py spec.json
spec.json:
{
  "id": "cf0004",
  "carousel": ["<div class=\"s\">...</div>", ...],          # telas 1080x1350 (opcional)
  "reel": {"frames": ["<div class=\"r\">...</div>", ...],   # telas 1080x1920 (opcional)
           "durs": [4.5, 5.5, ...]},                        # segundos por tela (4 a 7 s)
  "story": "<div class=\"r\">...</div>"                     # Story 1080x1920 (opcional)
}
Saída em posts/<id>/: <id>-01.jpg..., <id>-reel.mp4, capa.jpg, <id>-story.jpg
"""
import asyncio, json, pathlib, subprocess, sys
TOOLS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from brand import CSS
from playwright.async_api import async_playwright

EXTRA = """
.stack{margin-top:70px;display:flex;flex-direction:column;gap:18px}
.seg{display:flex;align-items:center;gap:22px;font:500 32px Plex;color:#CFCAC0}
.seg .b{height:64px;flex:none}
.seg .v{font:800 40px Fraunces;color:#F4F1EA;width:190px;flex:none;white-space:nowrap}
.seg .tax{background:#FFD21F}.seg .oth{background:#3A3832}
.r{width:1080px;height:1920px;padding:0 90px;display:flex;flex-direction:column;justify-content:center;position:relative}
.r .h{font-size:104px}
.r .p{font-size:46px}
.r .top{position:absolute;top:150px;left:90px;font:600 30px Plex;letter-spacing:.14em;color:#FFD21F;text-transform:uppercase}
.r .bot{position:absolute;bottom:170px;left:90px;right:90px;display:flex;justify-content:space-between;font:500 30px Plex;color:#8C877E}
.r .proof{gap:44px;padding:56px}.r .row .l{font-size:28px}.r .row .t{font-size:42px}
.r .bot b{font:800 34px Fraunces;color:#F4F1EA}
"""

async def shoot(pg, html, path, w, h):
    f = path.parent / "_tmp.html"
    f.write_text(f"<html><head><meta charset='utf-8'><style>{CSS}{EXTRA}</style></head><body style='width:{w}px;height:{h}px'>{html}</body></html>")
    await pg.set_viewport_size({"width": w, "height": h})
    await pg.goto(f.as_uri()); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
    await pg.screenshot(path=str(path), type="jpeg", quality=92)
    f.unlink()

def build_reel(out, pid, n, durs):
    X = 0.6; inputs, filt = [], []
    for i, d in enumerate(durs):
        inputs += ["-loop", "1", "-t", str(d + X), "-i", str(out / f"_f{i+1}.jpg")]
        filt.append(f"[{i}:v]scale=1188:2112,zoompan=z='min(zoom+0.0004,1.06)':d={int((d+X)*30)}:s=1080x1920:fps=30,setsar=1,format=yuv420p[v{i}]")
    prev, off = "v0", 0.0
    for i in range(1, len(durs)):
        off += durs[i-1]
        filt.append(f"[{prev}][v{i}]xfade=transition=fade:duration={X}:offset={off:.2f}[x{i}]"); prev = f"x{i}"
    total = sum(durs) + X
    wav = out / "_music.wav"
    subprocess.run(["python3", str(TOOLS / "music.py"), f"{total:.2f}", str(wav)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-i", str(wav), "-filter_complex", ";".join(filt),
        "-map", f"[{prev}]", "-map", f"{len(durs)}:a", "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-r", "30", "-b:v", "6M", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
        str(out / f"{pid}-reel.mp4")], check=True)
    (out / "_f1.jpg").rename(out / "capa.jpg")
    for i in range(2, n + 1): (out / f"_f{i}.jpg").unlink()
    wav.unlink()

async def main(spec):
    pid = spec["id"]; out = TOOLS.parent / "posts" / pid; out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        for i, s in enumerate(spec.get("carousel", []), 1):
            await shoot(pg, s, out / f"{pid}-{i:02d}.jpg", 1080, 1350)
        reel = spec.get("reel")
        if reel:
            for i, s in enumerate(reel["frames"], 1):
                await shoot(pg, s, out / f"_f{i}.jpg", 1080, 1920)
        if spec.get("story"):
            await shoot(pg, spec["story"], out / f"{pid}-story.jpg", 1080, 1920)
        await b.close()
    if reel:
        build_reel(out, pid, len(reel["frames"]), reel["durs"])
    print("ok", out)

asyncio.run(main(json.load(open(sys.argv[1]))))
