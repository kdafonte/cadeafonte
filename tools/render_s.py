"""Renderizador genérico (marca S). A marca entra só pelo spec, nada de nome de marca neste arquivo.

Uso:  python3 tools/render_s.py spec.json
spec.json:
{
  "id": "s-0511",                       # pasta de saída: tmp-s/<id>/
  "mark": "NOME DA MARCA",              # texto do logo
  "handle": "@perfil · Cidade/UF",      # rodapé
  "carousel": ["<html da tela>", ...],  # 1080x1350, opcional -> <id>-01.jpg ...
  "reel": {"frames": [...], "durs": [5, 6, ...]},   # 1080x1920, opcional -> <id>-reel.mp4 + capa.jpg
  "stories": {"nome": "<html>", ...}    # 1080x1920, opcional -> <id>-<nome>.jpg
}
Componentes (dentro de cada tela):
  <div class="tag">Rótulo</div>
  <div class="h">Título com <em>destaque</em></div>
  <div class="p">Texto de apoio</div>
  <ol class="list"><li><b>1</b><div>Item</div></li></ol>
  <div class="myth">Mito riscado</div><div class="truth">Resposta</div>
  <div class="cta">Envie sua conta pelo link da bio</div>
  <div class="num">01</div>                 # número grande da tela
O logo, o rodapé e o contador (n/total) são postos automaticamente.
"""
import asyncio, json, pathlib, subprocess, sys
TOOLS = pathlib.Path(__file__).resolve().parent
FONTS = TOOLS / "node_modules/@fontsource/arimo/files"
from playwright.async_api import async_playwright

CSS = f"""
@font-face{{font-family:A;font-weight:400;src:url({(FONTS/'arimo-latin-400-normal.woff2').as_uri()})}}
@font-face{{font-family:A;font-weight:700;src:url({(FONTS/'arimo-latin-700-normal.woff2').as_uri()})}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0F1215;font-family:A;color:#fff;overflow:hidden;position:relative}}
body:before{{content:"";position:absolute;right:-260px;top:-260px;width:760px;height:760px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,184,28,.16) 0,rgba(255,184,28,.05) 45%,transparent 70%)}}
.logo{{position:absolute;left:84px;display:flex;align-items:center;gap:18px;font:700 30px A;letter-spacing:6px;text-transform:uppercase}}
.logo i{{width:30px;height:30px;border-radius:50%;background:#FFB81C;box-shadow:0 0 0 7px rgba(255,184,28,.18)}}
.foot{{position:absolute;left:84px;right:84px;display:flex;justify-content:space-between;font:400 28px A;color:#8C96A0;border-top:2px solid #252B31;padding-top:26px}}
.w{{position:absolute;left:84px;right:84px}}
.tag{{display:inline-block;background:#FFB81C;color:#0F1215;font:700 28px A;letter-spacing:3px;text-transform:uppercase;padding:12px 20px}}
.num{{font:700 150px/1 A;color:#FFB81C;margin-bottom:10px}}
.h{{margin-top:44px;font:700 84px/1.08 A}} .h em{{font-style:normal;color:#FFB81C}}
.p{{margin-top:40px;font:400 42px/1.42 A;color:#C9D0D6}} .p b{{color:#fff}}
.list{{list-style:none;margin-top:46px;display:flex;flex-direction:column;gap:30px}}
.list li{{display:flex;gap:28px;align-items:flex-start;font:400 40px/1.35 A;color:#DDE2E6}}
.list li b{{flex:none;width:62px;height:62px;border-radius:50%;background:#FFB81C;color:#0F1215;font:700 32px A;display:flex;align-items:center;justify-content:center}}
.myth{{margin-top:46px;padding:6px 0 6px 30px;border-left:8px solid #8C96A0;font:400 44px/1.35 A;color:#C9D0D6;text-decoration:line-through;text-decoration-color:#8C96A0}}
.truth{{margin-top:40px;padding:6px 0 6px 30px;border-left:8px solid #FFB81C;font:700 50px/1.3 A}}
.cta{{margin-top:60px;display:inline-flex;align-items:center;gap:20px;font:700 44px A}}
.cta:after{{content:"";width:46px;height:4px;background:#FFB81C;box-shadow:12px 0 0 #FFB81C}}
"""

def page(html, mark, handle, w, h, counter=""):
    tall = h > 1500
    top = 210 if tall else 90
    body_top = 520 if tall else 250
    foot_bottom = 250 if tall else 70
    return (f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body style='width:{w}px;height:{h}px'>"
            f"<div class='logo' style='top:{top}px'><i></i>{mark}</div>"
            f"<div class='w' style='top:{body_top}px'>{html}</div>"
            f"<div class='foot' style='bottom:{foot_bottom}px'><span>{handle}</span><span>{counter}</span></div></body></html>")

async def shoot(pg, html, path, w, h):
    f = path.parent / "_tmp.html"; f.write_text(html)
    await pg.set_viewport_size({"width": w, "height": h})
    await pg.goto(f.as_uri()); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
    await pg.screenshot(path=str(path), type="jpeg", quality=92); f.unlink()

def build_reel(out, pid, durs):
    X = 0.6; inputs, filt = [], []
    for i, d in enumerate(durs):
        inputs += ["-loop", "1", "-t", str(d + X), "-i", str(out / f"_f{i+1}.jpg")]
        filt.append(f"[{i}:v]scale=1188:2112,zoompan=z='min(zoom+0.0004,1.06)':d={int((d+X)*30)}:s=1080x1920:fps=30,setsar=1,format=yuv420p[v{i}]")
    prev, off = "v0", 0.0
    for i in range(1, len(durs)):
        off += durs[i-1]
        filt.append(f"[{prev}][v{i}]xfade=transition=fade:duration={X}:offset={off:.2f}[x{i}]"); prev = f"x{i}"
    wav = out / "_music.wav"
    subprocess.run(["python3", str(TOOLS / "music.py"), f"{sum(durs)+X:.2f}", str(wav)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-i", str(wav), "-filter_complex", ";".join(filt),
        "-map", f"[{prev}]", "-map", f"{len(durs)}:a", "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-r", "30", "-b:v", "6M", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
        str(out / f"{pid}-reel.mp4")], check=True)
    (out / "_f1.jpg").rename(out / "capa.jpg")
    for i in range(2, len(durs) + 1): (out / f"_f{i}.jpg").unlink()
    wav.unlink()

async def main(spec):
    pid, mark, handle = spec["id"], spec["mark"], spec["handle"]
    out = TOOLS.parent / "tmp-s" / pid; out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        car = spec.get("carousel", [])
        for i, s in enumerate(car, 1):
            await shoot(pg, page(s, mark, handle, 1080, 1350, f"{i}/{len(car)}"), out / f"{pid}-{i:02d}.jpg", 1080, 1350)
        reel = spec.get("reel")
        if reel:
            for i, s in enumerate(reel["frames"], 1):
                await shoot(pg, page(s, mark, handle, 1080, 1920), out / f"_f{i}.jpg", 1080, 1920)
        for name, s in spec.get("stories", {}).items():
            await shoot(pg, page(s, mark, handle, 1080, 1920), out / f"{pid}-{name}.jpg", 1080, 1920)
        await b.close()
    if reel: build_reel(out, pid, reel["durs"])
    print("ok", out)

asyncio.run(main(json.load(open(sys.argv[1]))))
