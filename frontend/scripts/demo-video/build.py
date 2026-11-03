"""Monte la vidéo de démo à partir des images capturées.

usage (depuis frontend/) : python scripts/demo-video/build.py desktop|mobile [dossier_sortie]
Réglages utilisés : desktop par défaut ; mobile avec X264_CRF=26 VP9_CRF=38.
Dépendances : pip install imageio-ffmpeg pillow
Produit <nom>.mp4 (H.264), <nom>.webm (VP9) et <nom>-poster.jpg.
La fin se fond dans la première image : la boucle est invisible.
"""
import json
import os
import subprocess
import sys

import imageio_ffmpeg
from PIL import Image

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
HERE = os.path.dirname(os.path.abspath(__file__))
MODE = sys.argv[1]
OUT_DIR = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', '..', 'public', 'video')
NAME = {'desktop': 'optitab-demo-ordinateur', 'mobile': 'optitab-demo-telephone'}[MODE]
REC = os.path.join(HERE, '.work', f'rec-{MODE}')
FADE = 0.6
FPS = 30

data = json.load(open(os.path.join(REC, 'timeline.json'), encoding='utf-8'))
timeline = data['timeline']
total = data['total']

# Liste ffconcat : chaque image avec sa durée réelle.
lines = ['ffconcat version 1.0']
for frame in timeline:
    lines.append(f"file 'frames/{frame['file']}'")
    lines.append(f"duration {frame['d']:.4f}")
lines.append(f"file 'frames/{timeline[-1]['file']}'")
concat_path = os.path.join(REC, 'list.ffconcat')
with open(concat_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

first = os.path.join(REC, 'frames', timeline[0]['file'])
width, height = Image.open(first).size
# H.264 exige des dimensions paires.
width -= width % 2
height -= height % 2

os.makedirs(OUT_DIR, exist_ok=True)
offset = max(0.0, total - FADE)
# OUT_W (facultatif) : largeur finale, réduite proprement (lanczos) depuis la capture.
out_w = int(os.environ.get('OUT_W', '0') or 0)
scale = f',scale={out_w}:-2:flags=lanczos' if out_w and out_w < width else ''
graph = (
    f'[0:v]fps={FPS},crop={width}:{height}:0:0{scale},setsar=1,format=yuv420p[a];'
    f'[1:v]fps={FPS},crop={width}:{height}:0:0{scale},setsar=1,format=yuv420p[b];'
    f'[a][b]xfade=transition=fade:duration={FADE}:offset={offset:.3f}[v]'
)
inputs = [
    '-f', 'concat', '-safe', '0', '-i', concat_path,
    '-loop', '1', '-t', f'{FADE + 0.5:.2f}', '-i', first,
]


def run(args):
    result = subprocess.run([FFMPEG, '-y', '-hide_banner', '-loglevel', 'error'] + args,
                            capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr[-2000:])
        sys.exit(1)


mp4 = os.path.join(OUT_DIR, f'{NAME}.mp4')
run(inputs + ['-filter_complex', graph, '-map', '[v]', '-an',
              '-c:v', 'libx264', '-preset', 'veryslow', '-crf', os.environ.get('X264_CRF', '22'), '-tune', 'animation',
              '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', mp4])

webm = os.path.join(OUT_DIR, f'{NAME}.webm')
run(inputs + ['-filter_complex', graph, '-map', '[v]', '-an',
              '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', os.environ.get('VP9_CRF', '34'), '-row-mt', '1',
              '-deadline', 'good', '-cpu-used', '2', webm])

poster = os.path.join(OUT_DIR, f'{NAME}-poster.jpg')
poster_im = Image.open(first).convert('RGB').crop((0, 0, width, height))
if scale:
    poster_im = poster_im.resize((out_w, round(height * out_w / width / 2) * 2), Image.LANCZOS)
poster_im.save(poster, quality=82, optimize=True, progressive=True)

for path in (mp4, webm, poster):
    print(f'{os.path.basename(path)} : {os.path.getsize(path) / 1024:.0f} Ko')
print(f'{width}x{height}, {total + 0.5:.1f} s')
