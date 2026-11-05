# 產生 PWA 圖示：撕日曆＋紅印章
from PIL import Image, ImageDraw
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'icons')
GREEN, RED, WHITE = (0, 98, 58, 255), (184, 18, 27, 255), (255, 255, 255, 255)
def draw(size, pad=0.0, rounded=True):
    S = size * 4
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if rounded: d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * .22), fill=GREEN)
    else: d.rectangle([0, 0, S, S], fill=GREEN)
    k = 1 - pad * 2
    P = lambda x, y: (S * (pad + x * k), S * (pad + y * k))
    a, b = P(.2, .18), P(.8, .84)
    d.rounded_rectangle([a[0], a[1], b[0], b[1]], radius=int(S * .03), fill=WHITE)
    a2, b2 = P(.2, .18), P(.8, .34)
    d.rounded_rectangle([a2[0], a2[1], b2[0], b2[1]], radius=int(S * .03), fill=RED)
    d.rectangle([a2[0], P(0, .29)[1], b2[0], b2[1]], fill=RED)
    for x in (.34, .5, .66):
        c = P(x, .25); r = S * .018 * k
        d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=WHITE)
    c = P(.5, .6); r = S * .16 * k
    d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], outline=RED, width=int(S * .028 * k))
    d.line([P(.42, .6), P(.485, .67), P(.595, .535)], fill=RED, width=int(S * .04 * k), joint='curve')
    return im.resize((size, size), Image.LANCZOS)
os.makedirs(OUT, exist_ok=True)
draw(180, rounded=False).convert('RGB').save(os.path.join(OUT, 'icon-180.png'))
draw(192).save(os.path.join(OUT, 'icon-192.png'))
draw(512).save(os.path.join(OUT, 'icon-512.png'))
draw(512, pad=.1, rounded=False).save(os.path.join(OUT, 'icon-maskable-512.png'))
