#!/usr/bin/env python3
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "lka09-ascii.svg"
lines = [
"██╗      ██╗  ██╗ █████╗  ██████╗  █████╗ ",
"██║      ██║ ██╔╝██╔══██╗██╔═████╗██╔══██╗",
"██║      █████╔╝ ███████║██║██╔██║╚██████║",
"██║      ██╔═██╗ ██╔══██║████╔╝██║ ╚═══██║",
"███████╗ ██║  ██╗██║  ██║╚██████╔╝ █████╔╝",
"╚══════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚════╝ ",
]
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="370" height="376" viewBox="0 0 370 376" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">','<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111722"/><stop offset="1" stop-color="#0d1117"/></linearGradient></defs>','<rect width="370" height="376" rx="12" fill="url(#bg)"/><rect x=".5" y=".5" width="369" height="375" rx="12" fill="none" stroke="#30363d"/><line x1="0" y1="30" x2="370" y2="30" stroke="#30363d"/>']
for i,c in enumerate(["#ff5f56","#ffbd2e","#27c93f"]): parts.append(f'<circle cx="{20+i*16}" cy="15" r="5" fill="{c}"/>')
parts.append('<text x="185" y="19" fill="#7d8590" font-size="12" text-anchor="middle">lka09@github: ~$ figlet LKA09</text>')
y=92
for i,line in enumerate(lines):
    parts.append(f'<text x="18" y="{y}" fill="#39d353" font-size="7.6" font-weight="700" opacity="0">{line}<animate attributeName="opacity" from="0" to="1" begin="{.15+i*.09:.2f}s" dur=".35s" fill="freeze"/></text>'); y+=18
commands=[("$ uname -a","#22d3ee"),("builder · learner · developer","#c9d1d9"),("$ pwd","#22d3ee"),("/home/lka09/projects","#c9d1d9"),("$ echo $STATUS","#22d3ee"),("always_learning=true","#39d353")]
y=235
for i,(line,color) in enumerate(commands):
    parts.append(f'<text x="22" y="{y}" fill="{color}" font-size="12.5" opacity="0">{line}<animate attributeName="opacity" from="0" to="1" begin="{.9+i*.12:.2f}s" dur=".35s" fill="freeze"/></text>'); y+=22
parts.append('</svg>')
OUT.write_text(''.join(parts), encoding='utf-8')
