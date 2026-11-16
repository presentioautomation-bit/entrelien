# Version verticale 1080x1920 (TikTok, Reels, Shorts) à partir de film.mp4 — gabarit validé le 14/11
# Usage : python3 vert.py <dossier> <numero> "ligne 1|ligne 2|ligne 3"
import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont
F='/home/claude/test/fonts/'
D,n,hook=sys.argv[1],sys.argv[2],sys.argv[3].split('|')
W,H=1080,1920
im=Image.new('RGB',(W,H),'#F3EEE4'); d=ImageDraw.Draw(im)
for y in range(0,H,48): d.line([(0,y),(W,y)],fill='#E6DFD1',width=2)
d.line([(70,0),(70,H)],fill='#E9C9A8',width=3)
d.text((110,250),f'Carnet de l’Entremetteur n°{n}',font=ImageFont.truetype(F+'caveat.ttf',58),fill='#C9922E')
size=70
while True:
    tit=ImageFont.truetype(F+'fraunces.ttf',size)
    if max(d.textlength(l,font=tit) for l in hook)<=900 or size<=50: break
    size-=2
y=330
for l in hook: d.text((110,y),l,font=tit,fill='#1E2A44'); y+=int(size*1.23)
d.rectangle([42,637,42+995,637+613],outline='#1E2A44',width=3)
d.text((110,1300),'Une histoire vraie, racontée par l’entremetteur.',font=ImageFont.truetype(F+'work.ttf',36),fill='#1E2A44')
d.text((110,1352),'entrelien.fr',font=ImageFont.truetype(F+'caveat.ttf',52),fill='#C9922E')
bg=os.path.join(D,'tmp','vbg.png'); im.save(bg)
dst=os.path.join(D,'vertical.mp4')
subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-i',bg,'-i',os.path.join(D,'film.mp4'),'-filter_complex',
  '[1:v]crop=1760:1080:80:0,scale=990:608[v];[0:v][v]overlay=45:640:shortest=1,format=yuv420p[o]',
  '-map','[o]','-map','1:a','-c:v','libx264','-preset','veryfast','-crf','20','-r','30','-c:a','aac','-b:a','160k','-movflags','+faststart','-shortest',dst],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-ss','3','-i',dst,'-frames:v','1','-vf','scale=360:-1',os.path.join(D,'stills','vert.jpg')],check=True)
print('vertical ok',os.path.getsize(dst))
