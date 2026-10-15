import pathlib
ROOT = pathlib.Path(__file__).parent
F = ROOT / "node_modules/@fontsource"
CSS = f"""
@font-face{{font-family:Fraunces;font-weight:600;src:url('file://{F}/fraunces/files/fraunces-latin-600-normal.woff2')}}
@font-face{{font-family:Fraunces;font-weight:800;src:url('file://{F}/fraunces/files/fraunces-latin-800-normal.woff2')}}
@font-face{{font-family:Fraunces;font-weight:900;src:url('file://{F}/fraunces/files/fraunces-latin-900-normal.woff2')}}
@font-face{{font-family:Plex;font-weight:400;src:url('file://{F}/ibm-plex-sans/files/ibm-plex-sans-latin-400-normal.woff2')}}
@font-face{{font-family:Plex;font-weight:500;src:url('file://{F}/ibm-plex-sans/files/ibm-plex-sans-latin-500-normal.woff2')}}
@font-face{{font-family:Plex;font-weight:600;src:url('file://{F}/ibm-plex-sans/files/ibm-plex-sans-latin-600-normal.woff2')}}
@font-face{{font-family:Plex;font-weight:700;src:url('file://{F}/ibm-plex-sans/files/ibm-plex-sans-latin-700-normal.woff2')}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1350px;background:#0E0E0E;color:#F4F1EA;font-family:Plex;overflow:hidden}}
.s{{width:1080px;height:1350px;padding:96px 88px 0;position:relative;display:flex;flex-direction:column}}
.kick{{font:600 26px Plex;letter-spacing:.14em;color:#FFD21F;text-transform:uppercase}}
.big{{font:900 380px/0.9 Fraunces;color:#FFD21F;letter-spacing:-.03em;margin-top:120px}}
.h{{font:800 92px/1.04 Fraunces;letter-spacing:-.015em}}
.h em{{font-style:normal;background:#FFD21F;color:#0E0E0E;padding:0 14px;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.p{{font:400 40px/1.4 Plex;color:#CFCAC0;margin-top:44px;max-width:860px}}
.p b{{color:#F4F1EA;font-weight:600}}
.chip{{position:absolute;left:88px;bottom:150px;display:flex;align-items:center;gap:16px;font:500 26px Plex;color:#0E0E0E;background:#F4F1EA;padding:14px 22px}}
.chip i{{display:inline-block;width:22px;height:28px;background:#0E0E0E;clip-path:polygon(0 0,70% 0,100% 25%,100% 100%,0 100%)}}
.foot{{position:absolute;left:88px;right:88px;bottom:56px;display:flex;justify-content:space-between;font:500 26px Plex;color:#8C877E;border-top:2px solid #2A2925;padding-top:22px}}
.foot b{{font:800 28px Fraunces;color:#F4F1EA}}
.bars{{margin-top:80px;display:flex;flex-direction:column;gap:30px}}
.bar{{display:flex;align-items:center;gap:24px;font:600 34px Plex}}
.bar span.y{{width:110px;color:#8C877E}}
.bar div{{height:90px;background:#3A3832}}
.bar div.hi{{background:#FFD21F}}
.bar span.v{{font:800 44px Fraunces;white-space:nowrap}}
ol{{list-style:none;margin-top:56px;display:flex;flex-direction:column;gap:36px}}
ol li{{display:flex;gap:28px;font:400 36px/1.35 Plex;color:#CFCAC0}}
ol li span{{flex:none;width:58px;height:58px;background:#FFD21F;color:#0E0E0E;font:900 34px/58px Fraunces;text-align:center}}
ol li b{{color:#F4F1EA;font-weight:600}}
.proof{{margin-top:56px;border:3px solid #FFD21F;padding:44px 48px;display:flex;flex-direction:column;gap:30px}}
.row .l{{font:600 22px Plex;letter-spacing:.12em;text-transform:uppercase;color:#FFD21F;margin-bottom:8px}}
.row .t{{font:400 32px/1.35 Plex;color:#F4F1EA}}
.stamp{{position:absolute;right:88px;top:96px;font:600 24px Plex;color:#8C877E}}
"""
