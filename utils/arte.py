
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[1]

def _font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()

def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i+2],16) for i in (0,2,4))

def gerar_card(cliente, titulo, subtitulo="", logos=None, foto=None, tamanho=(1080,1350)):
    bg = _hex(cliente["cores"][1])
    roxo = _hex(cliente["cores"][0])
    escuro = _hex(cliente["cores"][2])
    img = Image.new("RGB", tamanho, bg)
    d = ImageDraw.Draw(img)

    # barra superior
    d.rectangle((0,0,tamanho[0],42), fill=escuro)

    # foto opcional
    text_left = 90
    text_right = tamanho[0]-90
    if foto:
        p = ROOT / foto
        if p.exists():
            ph = Image.open(p).convert("RGBA")
            max_h = 760
            ratio = min(500/ph.width, max_h/ph.height)
            ph = ph.resize((int(ph.width*ratio), int(ph.height*ratio)))
            x = tamanho[0]-ph.width
            y = tamanho[1]-ph.height-120
            img.paste(ph, (x,y), ph)
            text_right = max(520, x-30)

    title_font = _font(64, True)
    sub_font = _font(34, False)

    # wrapping
    max_chars = 23 if foto else 30
    y = 150
    for line in textwrap.wrap(titulo, width=max_chars):
        d.text((text_left,y), line, font=title_font, fill=escuro)
        y += 78

    if subtitulo:
        y += 30
        for line in textwrap.wrap(subtitulo, width=40 if foto else 52):
            d.text((text_left,y), line, font=sub_font, fill=roxo)
            y += 48

    # logos
    logos = logos or []
    if logos:
        logo_imgs = []
        for rel in logos:
            p = ROOT / rel
            if not p.exists():
                continue
            lg = Image.open(p).convert("RGBA")
            max_h = 95
            ratio = min(200/lg.width, max_h/lg.height)
            lg = lg.resize((int(lg.width*ratio), int(lg.height*ratio)))
            logo_imgs.append(lg)
        total_w = sum(x.width for x in logo_imgs) + max(0,len(logo_imgs)-1)*22
        x = 70
        y = tamanho[1]-125
        for lg in logo_imgs:
            img.paste(lg, (x,y), lg)
            x += lg.width + 22

    return img
