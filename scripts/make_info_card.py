#!/usr/bin/env python3
import html
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "info-card.svg"
rows=[("host",),("kv","Role","Developer / Student"),("kv","Focus","Web, Backend, Mobile, Game"),("kv","OS","Windows, Ubuntu, Kali Linux"),("gap",),("sec","Stack"),("kv","Frontend","React, Next.js, TypeScript"),("kv","Backend","Node.js, NestJS, Spring Boot"),("kv","Mobile","Flutter, Dart"),("kv","Game","Unity, C#, Blender"),("kv","Data","PostgreSQL, Supabase, Firebase"),("gap",),("sec","Languages"),("kv","Code","Python, Java, C#, Rust, JS/TS"),("gap",),("sec","Tools"),("kv","DevOps","Git, GitHub, Docker"),("kv","Shell","PowerShell, Bash")]
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="490" height="376" viewBox="0 0 490 376" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">','<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111722"/><stop offset="1" stop-color="#0d1117"/></linearGradient></defs>','<rect width="490" height="376" rx="12" fill="url(#bg)"/><rect x=".5" y=".5" width="489" height="375" rx="12" fill="none" stroke="#30363d"/><line x1="0" y1="30" x2="490" y2="30" stroke="#30363d"/>']
for i,c in enumerate(["#ff5f56","#ffbd2e","#27c93f"]): parts.append(f'<circle cx="{20+i*16}" cy="15" r="5" fill="{c}"/>')
parts.append('<text x="245" y="19" fill="#7d8590" font-size="12" text-anchor="middle">lka09@github: ~$ neofetch</text>')
y=60
for i,row in enumerate(rows):
    kind=row[0]
    if kind=="gap": y+=10; continue
    if kind=="host": inner=f'<text x="20" y="{y}" font-size="14" font-weight="700"><tspan fill="#3fb950">lka09</tspan><tspan fill="#7d8590">@</tspan><tspan fill="#22d3ee">github</tspan></text><line x1="132" y1="{y-4}" x2="470" y2="{y-4}" stroke="#30363d"/>'
    elif kind=="sec": inner=f'<text x="20" y="{y}" fill="#58a6ff" font-size="12.5" font-weight="700">— {html.escape(row[1])}</text>'
    else: inner=f'<text x="20" y="{y}" fill="#ffa657" font-size="12.5" font-weight="700">{html.escape(row[1])}</text><text x="124" y="{y}" fill="#c9d1d9" font-size="12.5">{html.escape(row[2])}</text>'
    delay=.15+i*.055
    parts.append(f'<g opacity="0" transform="translate(0,5)">{inner}<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur=".4s" fill="freeze"/><animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="{delay:.2f}s" dur=".4s" fill="freeze"/></g>'); y+=20.5
parts.append('</svg>')
OUT.write_text(''.join(parts), encoding='utf-8')
