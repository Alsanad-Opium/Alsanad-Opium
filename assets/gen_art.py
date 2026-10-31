import math, random

SEED = 2006  # reproducible
random.seed(SEED)

# --- seeded value noise (the "Neural Drift" field) ---
G = 64
grid = [[random.random() for _ in range(G)] for _ in range(G)]
def lerp(a,b,t): return a+(b-a)*t
def fade(t): return t*t*t*(t*(t*6-15)+10)
def noise(x,y):
    xi,yi=int(math.floor(x)),int(math.floor(y)); xf,yf=x-xi,y-yi
    u,v=fade(xf),fade(yf)
    g=lambda i,j:grid[j%G][i%G]
    return lerp(lerp(g(xi,yi),g(xi+1,yi),u),lerp(g(xi,yi+1),g(xi+1,yi+1),u),v)
def fbm(x,y):
    return noise(x,y)*0.6+noise(x*2.1,y*2.1)*0.3+noise(x*4.3,y*4.3)*0.1

# Theme: "Neon Neural Dusk" (custom theme-factory theme)
T = dict(bg1="#070516", bg2="#150b35", violet="#7c3aed", cyan="#22d3ee",
         pink="#f472b6", amber="#fbbf24", text="#e2e8f0", mute="#94a3b8")
COLORS = [T["violet"], T["cyan"], T["pink"], T["cyan"], T["violet"], T["amber"]]

W,H = 1200,340
def flow_paths(n, steps, step_len, scale):
    out=[]
    for _ in range(n):
        x,y = random.uniform(-20,W+20), random.uniform(-20,H+20)
        pts=[(x,y)]
        for _ in range(steps):
            a = fbm(x*scale, y*scale)*math.pi*4
            x += math.cos(a)*step_len; y += math.sin(a)*step_len
            pts.append((x,y))
        out.append(pts)
    return out

def poly(pts):
    return "M"+" L".join(f"{x:.0f},{y:.0f}" for x,y in pts)

def banner():
    paths = flow_paths(85, 48, 9, 0.0035)
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%">']
    s.append(f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{T['bg1']}"/><stop offset="1" stop-color="{T['bg2']}"/></linearGradient>
<linearGradient id="title" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{T['cyan']}"/><stop offset=".5" stop-color="{T['violet']}"/><stop offset="1" stop-color="{T['pink']}"/></linearGradient>
<radialGradient id="glow" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#000" stop-opacity=".75"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<filter id="blur"><feGaussianBlur stdDeviation="1.2"/></filter>
</defs>
<style>
.f{{fill:none;stroke-linecap:round;stroke-dasharray:60 240;animation:flow linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-600}}}}
.t{{font-family:'Segoe UI',Helvetica,Arial,sans-serif;font-weight:800;fill:url(#title)}}
.s{{font-family:'Courier New',monospace;fill:{T['text']};animation:pulse 3s ease-in-out infinite}}
.m{{font-family:'Courier New',monospace;fill:{T['mute']}}}
@keyframes pulse{{0%,100%{{opacity:.75}}50%{{opacity:1}}}}
</style>''')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    s.append('<g filter="url(#blur)" opacity=".55">')
    for i,p in enumerate(paths):
        c=COLORS[i%len(COLORS)]; w=random.choice([1,1.5,2,2.5])
        d=random.uniform(5,12); off=-random.uniform(0,300)
        s.append(f'<path class="f" d="{poly(p)}" stroke="{c}" stroke-width="{w}" style="animation-duration:{d:.1f}s;animation-delay:{off/100:.1f}s"/>')
    s.append('</g><g opacity=".9">')
    for i,p in enumerate(paths[:40]):
        c=COLORS[(i+2)%len(COLORS)]
        d=random.uniform(6,14)
        s.append(f'<path class="f" d="{poly(p)}" stroke="{c}" stroke-width=".8" style="animation-duration:{d:.1f}s;animation-delay:-{random.uniform(0,8):.1f}s"/>')
    s.append('</g>')
    s.append(f'<ellipse cx="{W/2}" cy="{H/2}" rx="560" ry="130" fill="url(#glow)"/>')
    s.append(f'<text x="{W/2}" y="165" text-anchor="middle" class="t" font-size="76">ALSANAD SHEIKH</text>')
    s.append(f'<text x="{W/2}" y="212" text-anchor="middle" class="s" font-size="22">&gt; Full Stack Dev  ×  ML Deployment  ×  AI Products_</text>')
    s.append(f'<text x="{W/2}" y="250" text-anchor="middle" class="m" font-size="14">generative seed #{SEED} · neural drift field</text>')
    s.append('</svg>')
    open('assets/banner.svg','w').write("\n".join(s))

def divider(name, flip=False):
    w,h=1200,60
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%">',
       f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{T["cyan"]}" stop-opacity="0"/><stop offset=".3" stop-color="{T["cyan"]}"/><stop offset=".5" stop-color="{T["violet"]}"/><stop offset=".7" stop-color="{T["pink"]}"/><stop offset="1" stop-color="{T["pink"]}" stop-opacity="0"/></linearGradient></defs>',
       '<style>.w{fill:none;stroke:url(#g);stroke-linecap:round;stroke-dasharray:120 600;animation:d linear infinite}@keyframes d{to{stroke-dashoffset:-1440}}</style>']
    for k,(amp,fr,sp,sw) in enumerate([(14,.012,7,2),(9,.02,5,1.4),(6,.03,9,1)]):
        ph=random.uniform(0,6)
        pts=[(x, h/2+math.sin(x*fr+ph)*amp+math.sin(x*fr*2.3+ph)*amp*.3) for x in range(0,w+1,12)]
        s.append(f'<path class="w" d="{poly(pts)}" stroke-width="{sw}" style="animation-duration:{sp}s"/>')
        s.append(f'<path d="{poly(pts)}" fill="none" stroke="{T["violet"]}" stroke-opacity=".25" stroke-width=".8"/>')
    s.append('</svg>')
    open(f'assets/{name}.svg','w').write("\n".join(s))

def footer():
    paths=flow_paths(45,40,8,0.004)
    h=160
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="100%">',
       f'<defs><linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["bg2"]}"/><stop offset="1" stop-color="{T["bg1"]}"/></linearGradient><linearGradient id="t" x1="0" x2="1"><stop offset="0" stop-color="{T["cyan"]}"/><stop offset="1" stop-color="{T["pink"]}"/></linearGradient></defs>',
       '<style>.f{fill:none;stroke-dasharray:50 250;animation:a linear infinite}@keyframes a{to{stroke-dashoffset:-600}}.q{font-family:\'Courier New\',monospace;font-size:22px;font-weight:700;fill:url(#t)}</style>',
       f'<rect width="{W}" height="{h}" fill="url(#b)"/>']
    for i,p in enumerate(paths):
        p=[(x,y*h/H) for x,y in p]
        s.append(f'<path class="f" d="{poly(p)}" stroke="{COLORS[i%6]}" stroke-width="1.2" opacity=".6" style="animation-duration:{random.uniform(6,13):.1f}s;animation-delay:-{random.uniform(0,8):.1f}s"/>')
    s.append(f'<text x="{W/2}" y="88" text-anchor="middle" class="q">⚡ Turning ML models into real-world applications ⚡</text></svg>')
    open('assets/footer.svg','w').write("\n".join(s))

banner(); divider('divider'); footer()