#!/usr/bin/env python3
"""
Gera as ilustrações das 3 etapas da proposta via Gemini (Nano Banana Pro).

Existe para substituir as imagens atuais de `img/etapa-*.jpg`, que são material
de terceiros — uma delas traz legendas em russo creditando o estúdio original.
Além do problema de licença, ilustrar "o que a Júnia entrega" com prancha de
outro escritório é uma promessa que a proposta faz por ela.

    python3 gerar_ilustracoes.py            # gera as 3 em img/novas/
    python3 gerar_ilustracoes.py planta     # só uma
    MODEL=gemini-2.5-flash-image python3 gerar_ilustracoes.py   # fallback barato

Custo aprox.: Pro ~US$0,13/imagem. Não sobrescreve as atuais — sai em img/novas/
para comparar antes de trocar.
"""
import base64
import json
import os
import sys
import time
import urllib.request

DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(DIR, "img", "novas")
MODEL = os.environ.get("MODEL", "gemini-3-pro-image")

# As colunas do slide são ~85x48mm com background-size:cover -> 16:9
ASPECTO = "16:9"

# Paleta tirada do próprio gerador.html, para a imagem já nascer no tom certo
PALETA = (
    "Strictly limited warm neutral palette: bone white #E9E3DA, sand beige #D9CCBF, "
    "warm taupe #C9AE8E, muted ochre-brown #9C8055, deep walnut brown #8A6A45, "
    "soft grey-green sage as the only accent. No saturated colors, no blue, no black. "
)

# A regra que mais importa: a imagem antiga foi flagrada justamente pelas legendas
# em russo. Qualquer texto na arte a denuncia como material de terceiros.
SEM_TEXTO = (
    "ABSOLUTELY CRITICAL — the image must contain NO text whatsoever: no words, no "
    "letters in any alphabet (no Latin, no Cyrillic, no Asian characters), no numbers, "
    "no room labels, no dimension lines with figures, no legends, no annotation "
    "callouts, no logo, no watermark, no signature, no scale bar. Absolutely zero "
    "typography anywhere in the frame. "
)

COMUM = (
    "Professional architectural presentation graphic for a Brazilian interior design "
    "studio's client proposal. Flat, elegant, editorial quality. Light bone-white "
    "background with generous negative space. Soft, even lighting, no harsh shadows. "
    "Composition centered and balanced, designed to be cropped to a wide banner. "
    + PALETA + SEM_TEXTO
)

CENAS = {
    "planta": (
        "A top-down COLORED ARCHITECTURAL FLOOR PLAN of a contemporary apartment, drawn "
        "in the style of a polished presentation render. Walls as clean solid poché in "
        "warm dark brown. Rooms furnished from above: a living room with sofa and rug, "
        "a dining table with chairs, two bedrooms with beds, a kitchen counter, "
        "bathrooms with fixtures. Light oak wood flooring pattern in the social areas, "
        "subtle stone texture in the wet areas, a few potted plants and a small balcony "
        "with outdoor seating. Delicate, refined linework. The plan floats on the bone "
        "background with soft margins. " + COMUM
    ),
    "moodboard": (
        "An overhead FLAT-LAY MATERIAL BOARD of interior finish samples, arranged in a "
        "loose, elegant composition on a bone-white surface — the kind an interior "
        "architect assembles to present a concept. Include: a light oak wood veneer "
        "chip, a slab of warm beige travertine or marble with soft veining, folded "
        "linen and bouclé fabric swatches in oatmeal and sand, a coil of woven rattan "
        "or cane, two round paint chips in off-white and ochre, a small brushed brass "
        "metal plate, and a sprig of dried eucalyptus. Realistic textures, gentle "
        "top-down daylight, subtle contact shadows. " + COMUM
    ),
    "executivo": (
        "An AXONOMETRIC CUTAWAY ILLUSTRATION of a single contemporary living room, "
        "viewed from above at a 45-degree isometric angle, with two walls cut away to "
        "reveal the interior — the classic technical-yet-beautiful drawing used to "
        "present detailing. Show: herringbone light oak flooring, a built-in joinery "
        "wall with open shelving and a recessed niche, a low sofa, a round coffee "
        "table, an armchair, a floor lamp, a large window with sheer floor-length "
        "curtains, and a rug. Rendered in soft flat tones with fine precise linework, "
        "like a refined vector drawing. Clean bone background around the room volume. "
        + COMUM
    ),
}


def api_key():
    """A chave já existe nos outros projetos do Leo — reaproveita em vez de pedir."""
    locais = [
        os.path.join(DIR, ".env"),
        os.path.expanduser("~/decoracao/.env"),
        os.path.expanduser("~/livro-colorir/.env"),
    ]
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"]
    for caminho in locais:
        if os.path.exists(caminho):
            with open(caminho) as f:
                for linha in f:
                    if linha.startswith("GEMINI_API_KEY="):
                        return linha.split("=", 1)[1].strip()
    sys.exit("GEMINI_API_KEY não encontrada (.env local, ~/decoracao/.env ou ambiente)")


def gerar(slug, prompt, key, tentativas=3):
    cfg = {"responseModalities": ["IMAGE"]}
    if "pro-image" in MODEL:
        cfg["imageConfig"] = {"aspectRatio": ASPECTO,
                              "imageSize": os.environ.get("IMGSIZE", "2K")}
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": cfg}
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{MODEL}:generateContent?key={key}")
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}, method="POST")

    for i in range(tentativas):
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.load(resp)
            for part in data["candidates"][0]["content"]["parts"]:
                if "inlineData" in part:
                    os.makedirs(OUT, exist_ok=True)
                    caminho = os.path.join(OUT, f"etapa-{slug}.png")
                    with open(caminho, "wb") as f:
                        f.write(base64.b64decode(part["inlineData"]["data"]))
                    return caminho
            raise RuntimeError(f"sem imagem na resposta: {json.dumps(data)[:300]}")
        except Exception as e:
            print(f"  tentativa {i + 1} falhou: {e}", flush=True)
            if i < tentativas - 1:
                time.sleep(8)
    return None


if __name__ == "__main__":
    key = api_key()
    alvos = [a for a in sys.argv[1:] if not a.startswith("-")]
    n = int(os.environ.get("VARIACOES", "1"))
    print(f"Modelo: {MODEL} | {ASPECTO} | {n} variação(ões) | saída: img/novas/\n", flush=True)
    for slug, prompt in CENAS.items():
        if alvos and slug not in alvos:
            continue
        for v in range(1, n + 1):
            nome = slug if n == 1 else f"{slug}-{v}"
            print(f"Gerando {nome}...", flush=True)
            caminho = gerar(nome, prompt, key)
            print(f"  -> {caminho}" if caminho else "  -> FALHOU", flush=True)
