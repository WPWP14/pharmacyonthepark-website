# Generates product-style illustrations of dosage forms (generic shapes, no brand marks).
import os
os.makedirs('forms', exist_ok=True)
W, H = 480, 360
DEFS = '''<defs>
<radialGradient id="bg" cx="50%" cy="38%" r="75%"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E4EDF1"/></radialGradient>
<radialGradient id="sh" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#0B2230" stop-opacity=".28"/><stop offset="1" stop-color="#0B2230" stop-opacity="0"/></radialGradient>
<linearGradient id="white" x1="0" x2="1"><stop offset="0" stop-color="#E9EEF1"/><stop offset=".35" stop-color="#FFFFFF"/><stop offset=".7" stop-color="#F3F6F8"/><stop offset="1" stop-color="#C9D3D9"/></linearGradient>
<linearGradient id="gray" x1="0" x2="1"><stop offset="0" stop-color="#9AA8B1"/><stop offset=".4" stop-color="#DCE3E7"/><stop offset="1" stop-color="#7E8C95"/></linearGradient>
<linearGradient id="blue" x1="0" x2="1"><stop offset="0" stop-color="#003B5E"/><stop offset=".4" stop-color="#1B78B0"/><stop offset="1" stop-color="#003B5E"/></linearGradient>
<linearGradient id="green" x1="0" x2="1"><stop offset="0" stop-color="#3E8E34"/><stop offset=".4" stop-color="#7FD072"/><stop offset="1" stop-color="#3E8E34"/></linearGradient>
<linearGradient id="amber" x1="0" x2="1"><stop offset="0" stop-color="#6B3A0A"/><stop offset=".35" stop-color="#C9731E"/><stop offset=".6" stop-color="#A95A12"/><stop offset="1" stop-color="#4E2906"/></linearGradient>
<linearGradient id="clear" x1="0" x2="1"><stop offset="0" stop-color="#DDEAF0" stop-opacity=".9"/><stop offset=".4" stop-color="#FFFFFF" stop-opacity=".6"/><stop offset="1" stop-color="#C7D7DF" stop-opacity=".9"/></linearGradient>
<linearGradient id="pink" x1="0" x2="1"><stop offset="0" stop-color="#D9577E"/><stop offset=".45" stop-color="#F7A1BB"/><stop offset="1" stop-color="#C54670"/></linearGradient>
<linearGradient id="cream" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EDE7DC"/></linearGradient>
<linearGradient id="gloss" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".75"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="treat" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#B7773A"/><stop offset=".5" stop-color="#D89A5B"/><stop offset="1" stop-color="#8E5524"/></linearGradient>
</defs>'''

def wrap(inner, shadow=(240, 300, 170, 18)):
    cx, cy, rx, ry = shadow
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img">' + DEFS +
            f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
            f'<g id="c"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#sh)"/>' + inner + '</g></svg>')

LOGO = 'data:image/webp;base64,' + open('labellogo.b64').read()
LR = float(open('labellogo.ratio').read())

def logo(cx, y, w):
    h = w / LR
    return f'<image href="{LOGO}" x="{cx-w/2:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" preserveAspectRatio="xMidYMid meet"/>'

def label(x, y, w, h, lines=3, accent='#005687'):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#fff"/>'
    lw = min(w * 0.88, (h * 0.52) * LR)
    s += logo(x + w / 2, y + h * 0.05, lw)
    top = y + h * 0.05 + lw / LR + h * 0.05
    for i in range(2 if lines > 1 else 1):
        yy = top + i * h * 0.11
        s += f'<rect x="{x+w*0.16:.1f}" y="{yy:.1f}" width="{w*(0.68 - i*0.2):.1f}" height="{max(2,h*0.045):.1f}" rx="1.5" fill="#C9D6DD"/>'
    s += f'<rect x="{x}" y="{y+h*0.9:.1f}" width="{w}" height="{h*0.1:.1f}" fill="{accent}"/>'
    return s

def capsule(x, y, l, r, rot, c1='url(#blue)', c2='url(#white)'):
    return (f'<g transform="translate({x} {y}) rotate({rot})">'
            f'<rect x="{-l/2}" y="{-r}" width="{l}" height="{2*r}" rx="{r}" fill="{c2}"/>'
            f'<path d="M{-l/2+r} {-r} H0 V{r} H{-l/2+r} A{r} {r} 0 0 1 {-l/2+r} {-r}Z" fill="{c1}"/>'
            f'<rect x="{-l/2+r*0.6}" y="{-r*0.7}" width="{l-r*1.2}" height="{r*0.45}" rx="{r*0.2}" fill="url(#gloss)"/></g>')

forms = {}

# Unodose-style metered cream applicator: squat white cylinder with blue dial top and nozzle
forms['unodose'] = wrap(
    '<rect x="170" y="110" width="140" height="180" rx="22" fill="url(#white)"/>'
    '<rect x="170" y="250" width="140" height="40" rx="18" fill="url(#gray)"/>'
    + ''.join(f'<rect x="{176+i*9}" y="256" width="4" height="28" rx="2" fill="#6F7E87" opacity=".5"/>' for i in range(15)) +
    '<rect x="182" y="86" width="116" height="34" rx="14" fill="url(#blue)"/>'
    '<rect x="226" y="62" width="28" height="30" rx="8" fill="url(#blue)"/>'
    '<rect x="236" y="52" width="8" height="14" rx="4" fill="#003B5E"/>'
    + label(190, 150, 100, 70, 3) +
    '<rect x="178" y="118" width="18" height="160" rx="9" fill="url(#gloss)" opacity=".6"/>'
    , (240, 296, 110, 16))

# Topi-CLICK style dispenser: tall cylinder, clicking base, applicator dome
forms['topiclick'] = wrap(
    '<rect x="190" y="80" width="100" height="200" rx="16" fill="url(#white)"/>'
    '<rect x="190" y="250" width="100" height="38" rx="12" fill="url(#green)"/>'
    + ''.join(f'<rect x="{196+i*8}" y="256" width="3" height="26" rx="1.5" fill="#2E6B27" opacity=".45"/>' for i in range(11)) +
    '<rect x="200" y="60" width="80" height="30" rx="12" fill="url(#gray)"/>'
    '<ellipse cx="240" cy="62" rx="34" ry="10" fill="#EEF2F4"/>'
    + label(204, 120, 72, 90, 4, '#3E8E34') +
    '<rect x="196" y="88" width="14" height="160" rx="7" fill="url(#gloss)" opacity=".7"/>', (240, 296, 90, 14))

# Pearl-style vaginal applicator/dispenser: rounded egg with nozzle
forms['pearl'] = wrap(
    '<ellipse cx="240" cy="200" rx="70" ry="88" fill="url(#white)"/>'
    '<path d="M170 222 Q240 250 310 222 L306 238 Q300 280 240 288 Q180 280 174 238Z" fill="url(#pink)"/>'
    + ''.join(f'<rect x="{186+i*9}" y="{240+abs(i-6)*1.2:.1f}" width="3" height="{30-abs(i-6)*2.4:.1f}" rx="1.5" fill="#fff" opacity=".35"/>' for i in range(13)) +
    '<path d="M222 116 Q222 92 240 84 Q258 92 258 116Z" fill="url(#white)" stroke="#D5DEE3"/>'
    '<ellipse cx="240" cy="84" rx="9" ry="5" fill="#EEF2F4" stroke="#D5DEE3"/>'
    '<ellipse cx="212" cy="160" rx="16" ry="40" fill="url(#gloss)" opacity=".85"/>'
    '<rect x="194" y="166" width="92" height="46" rx="6" fill="#fff" stroke="#E3E9EC"/>' + logo(240, 169, 84) +
    '<rect x="194" y="206" width="92" height="6" fill="#D9577E"/>', (240, 296, 100, 14))

# Micro pen: slim pen-style dispenser with dial and cap
forms['micropen'] = wrap(
    '<g transform="rotate(-18 240 190)">'
    '<rect x="90" y="170" width="300" height="40" rx="20" fill="url(#white)"/>'
    '<rect x="90" y="170" width="70" height="40" rx="20" fill="url(#blue)"/>'
    + ''.join(f'<rect x="{104+i*7}" y="174" width="3" height="32" rx="1.5" fill="#fff" opacity=".35"/>' for i in range(7)) +
    '<rect x="330" y="172" width="70" height="36" rx="18" fill="url(#gray)"/>'
    '<rect x="184" y="173" width="130" height="34" rx="5" fill="#fff"/>' + logo(249, 175, 70) +
    '<rect x="100" y="174" width="280" height="10" rx="5" fill="url(#gloss)" opacity=".7"/></g>', (240, 270, 160, 14))

# Troches: translucent square lozenges in a molded tray
tro = ('<g transform="translate(120 130) skewX(-18)"><rect x="0" y="0" width="250" height="170" rx="10" fill="#E9EFF2" stroke="#CFDAE0"/>'
       '<rect x="66" y="128" width="118" height="36" rx="5" fill="#fff"/>' + logo(125, 130, 74))
cols = ['#F2B34A', '#E97A8F', '#9FCF8E', '#F2B34A', '#E97A8F', '#9FCF8E', '#F2B34A', '#E97A8F']
for i in range(8):
    x = 14 + (i % 4) * 58; y = 12 + (i // 4) * 58
    tro += f'<rect x="{x}" y="{y}" width="50" height="50" rx="8" fill="#D5DEE3"/>'
    if i != 7:
        tro += f'<rect x="{x+4}" y="{y+2}" width="42" height="42" rx="7" fill="{cols[i]}" opacity=".92"/><rect x="{x+8}" y="{y+6}" width="30" height="10" rx="4" fill="#fff" opacity=".45"/>'
tro += '</g>'
tro += '<g transform="translate(372 250) rotate(12)"><rect x="-22" y="-22" width="44" height="44" rx="8" fill="#9FCF8E"/><rect x="-16" y="-17" width="30" height="10" rx="4" fill="#fff" opacity=".45"/></g>'
forms['troche'] = wrap(tro, (250, 296, 170, 16))

# Capsules with amber vial
cap = ('<rect x="110" y="120" width="120" height="160" rx="12" fill="url(#amber)"/>'
       '<rect x="102" y="96" width="136" height="36" rx="10" fill="url(#white)"/>'
       + label(122, 168, 96, 70, 3) +
       '<rect x="116" y="132" width="14" height="140" rx="7" fill="url(#gloss)" opacity=".5"/>')
for (x, y, rot, c) in [(300, 250, -20, 'url(#blue)'), (350, 280, 15, 'url(#green)'), (275, 290, 8, 'url(#blue)'), (380, 232, -40, 'url(#green)'), (320, 212, 30, 'url(#blue)')]:
    cap += capsule(x, y, 74, 14, rot, c)
forms['capsule'] = wrap(cap, (250, 298, 170, 16))

# Tablets: white scored round tablets
tab = ('<rect x="330" y="96" width="100" height="140" rx="16" fill="url(#white)"/><rect x="344" y="76" width="72" height="26" rx="8" fill="url(#blue)"/>'
       + label(338, 128, 84, 76, 2) + '<rect x="336" y="104" width="12" height="120" rx="6" fill="url(#gloss)" opacity=".7"/>')
for (x, y) in [(170, 230), (240, 250), (310, 228), (205, 185), (275, 195), (345, 262), (140, 268)]:
    tab += (f'<ellipse cx="{x}" cy="{y+6}" rx="32" ry="13" fill="#C6D0D6"/><ellipse cx="{x}" cy="{y}" rx="32" ry="13" fill="#FFFFFF" stroke="#DCE3E7"/>'
            f'<path d="M{x-24} {y} H{x+24}" stroke="#D0D9DE" stroke-width="2"/>')
forms['tablet'] = wrap(tab, (250, 290, 170, 16))

# Rapid-dissolve tablets: small pink discs in a blister card
rdt = '<g transform="translate(120 105) skewX(-14)"><rect x="0" y="0" width="240" height="200" rx="12" fill="url(#white)" stroke="#D5DEE3"/>' + logo(120, 158, 88)
for i in range(12):
    x = 30 + (i % 4) * 58; y = 30 + (i // 4) * 50
    rdt += f'<ellipse cx="{x}" cy="{y}" rx="22" ry="17" fill="url(#clear)" stroke="#C7D7DF"/><ellipse cx="{x}" cy="{y}" rx="15" ry="11" fill="url(#pink)"/><ellipse cx="{x-4}" cy="{y-4}" rx="6" ry="3" fill="#fff" opacity=".5"/>'
rdt += '</g>'
forms['rdt'] = wrap(rdt, (240, 296, 150, 14))

# Oral suspension: amber bottle with oral syringe
def bottle(x, y, w, h, lab_accent='#005687', pet=False):
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w*0.18}" fill="url(#amber)"/>'
         f'<rect x="{x+w*0.22}" y="{y-h*0.14}" width="{w*0.56}" height="{h*0.18}" rx="6" fill="url(#white)"/>'
         + label(x + w * 0.12, y + h * 0.3, w * 0.76, h * 0.42, 3, lab_accent) +
         f'<rect x="{x+6}" y="{y+10}" width="{w*0.12}" height="{h-20}" rx="6" fill="url(#gloss)" opacity=".45"/>')
    if pet:
        cx, cy = x + w * 0.5, y + h * 0.86
        s += ''.join(f'<circle cx="{cx+dx*0.8}" cy="{cy+dy*0.8}" r="3.4" fill="#F4EBD6"/>' for dx, dy in [(-9, -8), (-3, -12), (3, -12), (9, -8)])
        s += f'<ellipse cx="{cx}" cy="{cy+1}" rx="6.5" ry="5" fill="#F4EBD6"/>'
    return s
def syringe(x, y, rot, l=190):
    return (f'<g transform="translate({x} {y}) rotate({rot})">'
            f'<rect x="0" y="-11" width="{l}" height="22" rx="6" fill="url(#clear)" stroke="#B9CBD4"/>'
            f'<rect x="4" y="-8" width="{l*0.55}" height="16" rx="4" fill="#E9B26A" opacity=".85"/>'
            + ''.join(f'<rect x="{12+i*14}" y="-11" width="1.5" height="8" fill="#6F7E87"/>' for i in range(int(l/14)-1)) +
            f'<rect x="{l}" y="-4" width="18" height="8" rx="3" fill="#D0DAE0"/>'
            f'<rect x="-40" y="-4" width="44" height="8" rx="3" fill="#E6ECEF"/><rect x="-50" y="-15" width="12" height="30" rx="4" fill="#E6ECEF"/></g>')
forms['suspension'] = wrap(bottle(140, 120, 120, 170) + syringe(250, 270, -22), (250, 298, 170, 16))
forms['suspension-pet'] = wrap(bottle(140, 120, 120, 170, '#3E8E34', True) + syringe(250, 270, -22), (250, 298, 170, 16))

# Cream jar
forms['cream'] = wrap(
    '<rect x="150" y="190" width="180" height="96" rx="16" fill="url(#white)"/>'
    '<rect x="150" y="208" width="180" height="64" fill="#fff"/><rect x="150" y="208" width="180" height="4" fill="#5FBA51"/><rect x="150" y="266" width="180" height="6" fill="#005687"/>'
    + logo(240, 214, 118) +
    '<g transform="rotate(-10 330 150)"><rect x="248" y="130" width="170" height="44" rx="12" fill="url(#gray)"/>'
    + ''.join(f'<rect x="{254+i*8}" y="136" width="3" height="32" rx="1.5" fill="#6F7E87" opacity=".35"/>' for i in range(20)) + '</g>'
    '<ellipse cx="240" cy="190" rx="90" ry="16" fill="url(#cream)" stroke="#E2DACB"/>'
    '<path d="M205 188 q20 -22 40 -4 q12 10 30 -2" fill="none" stroke="#E2DACB" stroke-width="5" stroke-linecap="round"/>', (240, 292, 140, 16))

# PLO transdermal gel in 1 mL syringes
forms['plo'] = wrap(
    '<rect x="300" y="64" width="126" height="104" rx="10" fill="url(#white)" stroke="#D5DEE3"/><rect x="300" y="150" width="126" height="18" fill="#3E8E34"/>'
    + logo(363, 80, 108) + ''.join(f'<g transform="translate({120+i*18} {170+i*38}) rotate(-8)">'
            f'<rect x="0" y="-10" width="200" height="20" rx="6" fill="url(#clear)" stroke="#B9CBD4"/>'
            f'<rect x="4" y="-7" width="120" height="14" rx="4" fill="#F4EBD6"/>'
            + ''.join(f'<rect x="{14+j*16}" y="-10" width="1.5" height="7" fill="#6F7E87"/>' for j in range(11)) +
            f'<rect x="200" y="-4" width="14" height="8" rx="3" fill="#3E8E34"/>'
            f'<rect x="-36" y="-4" width="40" height="8" rx="3" fill="#E6ECEF"/><rect x="-46" y="-13" width="12" height="26" rx="4" fill="#E6ECEF"/></g>' for i in range(3)), (250, 296, 170, 14))

# Chewable treats
tr = ('<path d="M318 86 H432 L428 252 Q375 264 322 252 Z" fill="url(#white)" stroke="#D5DEE3"/><rect x="318" y="80" width="114" height="14" rx="3" fill="#3E8E34"/>'
      + logo(375, 112, 96) + '<rect x="342" y="168" width="66" height="4" rx="2" fill="#C9D6DD"/><rect x="350" y="178" width="50" height="4" rx="2" fill="#C9D6DD"/>')
for (x, y, r) in [(170, 220, -12), (260, 240, 10), (330, 205, -25), (215, 270, 20), (300, 285, -6)]:
    tr += (f'<g transform="translate({x} {y}) rotate({r})"><rect x="-38" y="-24" width="76" height="48" rx="12" fill="url(#treat)"/>'
           f'<rect x="-30" y="-18" width="60" height="12" rx="6" fill="#fff" opacity=".18"/>'
           + ''.join(f'<circle cx="{dx}" cy="{dy}" r="2.2" fill="#7A4518" opacity=".6"/>' for dx, dy in [(-20, 4), (-6, 10), (10, 2), (22, 12), (0, -4)]) + '</g>')
forms['treat'] = wrap(tr, (250, 300, 170, 16))

# Suppositories in a mold strip
sp = '<g transform="translate(110 160) skewX(-12)"><rect x="0" y="40" width="270" height="106" rx="10" fill="url(#white)" stroke="#D5DEE3"/>' + logo(135, 106, 80)
for i in range(5):
    x = 26 + i * 50
    sp += f'<path d="M{x-14} 100 V40 Q{x-14} -4 {x} -10 Q{x+14} -4 {x+14} 40 V100 Z" fill="#F7F1E3" stroke="#E2DACB"/><rect x="{x-9}" y="0" width="6" height="90" rx="3" fill="#fff" opacity=".6"/>'
sp += '</g>'
forms['suppository'] = wrap(sp, (250, 296, 170, 16))

# Nasal spray bottle
forms['nasal'] = wrap(
    '<rect x="180" y="150" width="120" height="140" rx="22" fill="url(#white)"/>'
    '<rect x="196" y="120" width="88" height="34" rx="8" fill="url(#gray)"/>'
    '<path d="M222 120 V70 Q222 50 240 44 Q258 50 258 70 V120Z" fill="url(#white)" stroke="#D5DEE3"/>'
    '<rect x="200" y="96" width="80" height="12" rx="6" fill="url(#blue)"/>'
    + label(196, 186, 88, 70, 3) +
    '<rect x="186" y="160" width="14" height="120" rx="7" fill="url(#gloss)" opacity=".7"/>', (240, 296, 100, 14))

# Lollipop / sugar-free pops
forms['lollipop'] = wrap(
    '<g transform="rotate(-20 230 200)"><rect x="226" y="190" width="10" height="130" rx="5" fill="#F3F6F8" stroke="#D5DEE3"/>'
    '<circle cx="231" cy="160" r="62" fill="url(#pink)"/><path d="M231 160 m-40 0 a40 40 0 1 0 40 -40" fill="none" stroke="#fff" stroke-width="8" opacity=".55"/><ellipse cx="210" cy="132" rx="18" ry="10" fill="#fff" opacity=".5"/></g>'
    '<g transform="rotate(18 330 230)"><rect x="326" y="220" width="9" height="100" rx="4.5" fill="#F3F6F8" stroke="#D5DEE3"/>'
    '<circle cx="330" cy="200" r="42" fill="url(#green)"/><ellipse cx="316" cy="182" rx="12" ry="7" fill="#fff" opacity=".5"/></g>', (270, 300, 150, 16))

# Mouthwash / oral rinse bottle
forms['mouthwash'] = wrap(
    '<rect x="170" y="110" width="140" height="180" rx="20" fill="url(#clear)" stroke="#C7D7DF"/>'
    '<rect x="176" y="160" width="128" height="124" rx="14" fill="#8FD0C7" opacity=".55"/>'
    '<rect x="196" y="82" width="88" height="36" rx="8" fill="url(#white)"/>'
    + label(192, 170, 96, 72, 3) +
    '<rect x="178" y="118" width="14" height="160" rx="7" fill="url(#gloss)" opacity=".7"/>', (240, 296, 110, 14))

# Ear pack syringe (pet)
forms['earpack'] = forms['plo']

for k, v in forms.items():
    open(f'forms/{k}.svg', 'w').write(v)
print(len(forms))
