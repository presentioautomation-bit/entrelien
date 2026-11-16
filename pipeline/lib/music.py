# Musique originale douce (nappe + piano), une couleur d'accord par bloc, presque silence sur la bascule.
# Puis mixage voix + musique (atténuation automatique sous la voix) à -14 LUFS -> mix.wav
# Usage : python3 music.py <dossier_episode>
import numpy as np, json, sys, os, re, subprocess, soundfile as sf
os.chdir(sys.argv[1])
S=json.load(open('script.json')); TM=json.loads(open('timing.js').read().split('=',1)[1].rstrip(';'))
SR=48000; END=TM['end']; N=int(END*SR); t=np.arange(N)/SR
rng=np.random.default_rng(S.get('seed',7))
def hz(m): return 440*2**((m-69)/12)
# progressions (accords en notes MIDI), choisies par épisode
PROG={'warm':[[50,57,62,66],[47,54,59,62],[43,50,55,59],[45,52,57,61]],     # D  Bm G  A
      'tender':[[48,55,60,64],[45,52,57,60],[41,48,53,57],[43,50,55,59]],   # C  Am F  G
      'dusk':[[45,52,57,60],[41,48,53,57],[48,55,60,64],[43,50,55,59]],     # Am F  C  G
      'blue':[[50,57,62,65],[46,53,58,62],[43,50,55,58],[45,52,57,61]]}     # Dm Bb Gm A
prog=PROG[S.get('mood','warm')]
keys=list(TM['blocks']); hush=set(S.get('hush',[]))
# bornes : chaque accord commence au début du silence qui précède le bloc
starts=[0.0]+[TM['blocks'][k][0]-0.6 for k in keys[1:]]
pad=np.zeros((N,2)); pia=np.zeros((N,2))
for i,k in enumerate(keys):
    a=starts[i]; b=starts[i+1] if i+1<len(keys) else END
    ch=prog[i%len(prog)]; lvl=0.12 if k in hush else 1.0
    ia,ib=int(a*SR),min(N,int((b+1.6)*SR)); tt=np.arange(ib-ia)/SR; L=len(tt)
    env=np.minimum(1,tt/1.8)*np.clip((b+1.6-a-tt)/1.6,0,1)
    for j,m in enumerate(ch):
        for det,pan in ((-0.12,0.3),(0.12,0.7)):
            f=hz(m)*2**(det/1200*10)
            w=np.sin(2*np.pi*f*tt+rng.uniform(0,6))+0.18*np.sin(4*np.pi*f*tt)+0.05*np.sin(6*np.pi*f*tt)
            w*=env*lvl*(0.05 if j else 0.07)*(1+0.15*np.sin(2*np.pi*0.13*tt+j))
            pad[ia:ib,0]+=w*(1-pan); pad[ia:ib,1]+=w*pan
    if k in hush: continue
    # piano : arpège lent sur l'accord, une octave au-dessus
    x=a+0.4
    notes=[m+12 for m in ch[1:]]+[ch[1]+24]
    n=0
    while x<b-0.8:
        m=notes[n%len(notes)] if rng.random()>0.25 else notes[rng.integers(len(notes))]
        f=hz(m); i0=int(x*SR); L=min(int(3.2*SR),N-i0); tt=np.arange(L)/SR
        e=np.exp(-tt/0.9)*np.minimum(1,tt/0.006)
        w=(np.sin(2*np.pi*f*tt)+0.35*np.sin(4*np.pi*f*tt)*np.exp(-tt/0.3)+0.12*np.sin(6*np.pi*f*tt)*np.exp(-tt/0.2))*e*0.085*rng.uniform(0.75,1.0)
        p=rng.uniform(0.3,0.7); pia[i0:i0+L,0]+=w*(1-p); pia[i0:i0+L,1]+=w*p
        x+=rng.choice([1.2,1.5,1.8,2.4]); n+=1
mus=pad+pia
# filtre passe-bas doux (une pôle) pour arrondir
from scipy.signal import lfilter
alpha=np.exp(-2*np.pi*3500/SR)
for c in range(2):
    mus[:,c]=lfilter([1-alpha],[1,-alpha],mus[:,c])
fadeo=np.clip((END-t)/3.0,0,1); mus*=fadeo[:,None]
mus/=max(1e-9,np.abs(mus).max()); mus*=0.5
sf.write('tmp/music_raw.wav',mus,SR)
# réverbération légère + mix avec atténuation sous la voix
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i','tmp/music_raw.wav','-af','aecho=0.8:0.6:60|130:0.25|0.15','tmp/music.wav'],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i','vo.wav','-i','tmp/music.wav','-filter_complex',
  '[0]aformat=channel_layouts=stereo,asplit=2[v][sc];[1]volume=0.30[m];[m][sc]sidechaincompress=threshold=0.02:ratio=6:attack=20:release=450[md];[v][md]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]',
  '-map','[a]','-ar','48000','mix.wav'],check=True)
print('mix ok',END)
