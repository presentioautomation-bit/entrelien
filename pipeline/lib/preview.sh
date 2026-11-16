#!/bin/bash
# Aperçu d'un épisode : voix factice si absente, timing, images clés, planche-contact tmp/sheet.jpg
# Usage : preview.sh <dossier>
set -e
cd "$1"; mkdir -p tts tmp stills
python3 - <<'E'
import json,subprocess,os
S=json.load(open('script.json'))
for k,v in S['blocks'].items():
    f=f'tts/{k}.mp3'
    if not os.path.exists(f):
        subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i',f'sine=f=180:d={len(v)/14.5}','-af','volume=0.3',f],check=True)
        open('tmp/FAKE','w').write('1')
E
python3 /home/claude/prod/lib/timing.py . | tail -1
rm -f stills/s_*.jpg
python3 /home/claude/prod/lib/render.py . auto | tail -1
ffmpeg -v error -y -pattern_type glob -i 'stills/s_*.jpg' -vf "scale=640:-1,tile=3x8" -frames:v 1 tmp/sheet.jpg
