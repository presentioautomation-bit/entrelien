# Construit timing.js (blocs + sous-titres) et vo.wav à partir de script.json et tts/XX.mp3
# Usage : python3 timing.py <dossier_episode>
import subprocess, re, json, sys, os
os.chdir(sys.argv[1])
S = json.load(open('script.json'))
T = S['blocks']; gaps = S.get('gaps', {}); order = list(T)
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
def segs_of(f,d):
    out=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',f,'-af','silencedetect=noise=-38dB:d=0.22','-f','null','-'],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',out)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',out)]
    sil=list(zip(st,en+[d]*(len(st)-len(en)))); segs=[];cur=0
    for a,b in sil:
        if a-cur>0.15: segs.append([cur,a])
        cur=b
    if d-cur>0.15: segs.append([cur,d])
    return segs
def phrases(t):
    t=t.replace('[pause]','')
    return [x.strip() for x in re.findall(r'.+?(?:[.?!…](?:\s*»)?|$)(?=\s|$)',t) if x.strip()]
t=0; blocks={}; subs=[]; os.makedirs('tmp',exist_ok=True); fl=open('tmp/vo_list.txt','w')
for k in order:
    g=gaps.get(k,0.6 if k==order[0] else 0.75); t+=g; f=f'tts/{k}.mp3'; d=dur(f); blocks[k]=[round(t,3),round(t+d,3)]
    sp=segs_of(f,d); ph=phrases(T[k])
    if len(sp)==len(ph):
        for x,(a,b) in zip(ph,sp): subs.append([round(t+a,2),round(t+b,2),x,k])
    else:
        s0=sp[0][0]; s1=sp[-1][1]; tot=sum(len(x) for x in ph); c=0
        for x in ph:
            a=s0+(s1-s0)*c/tot; c+=len(x); b=s0+(s1-s0)*c/tot; subs.append([round(t+a,2),round(t+b,2),x,k])
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i','anullsrc=r=48000:cl=mono','-t',str(g),f'tmp/sil_{k}.wav'],check=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',f,'-ar','48000','-ac','1',f'tmp/{k}.wav'],check=True)
    fl.write(f"file 'sil_{k}.wav'\nfile '{k}.wav'\n"); t+=d
fl.close(); END=round(t+S.get('tail',4.0),2)
# sous-titres trop longs : couper en deux à la virgule la plus centrale
out=[]
for a,b,x,k in subs:
    if len(x)>78 and ',' in x:
        cuts=[m.start() for m in re.finditer(',',x)]; c=min(cuts,key=lambda i:abs(i-len(x)/2))
        x1,x2=x[:c+1].strip(),x[c+1:].strip(); m=a+(b-a)*len(x1)/len(x)
        out+= [[a,round(m,2),x1,k],[round(m,2),b,x2,k]]
    else: out.append([a,b,x,k])
subs=out
open('timing.js','w').write('window.TIMING='+json.dumps({'blocks':blocks,'subs':subs,'end':END},ensure_ascii=False)+';')
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i','tmp/vo_list.txt','-af',f'apad=whole_dur={END}','-ar','48000','vo.wav'],check=True)
print(json.dumps(blocks)); print('END',END,'subs',len(subs))
