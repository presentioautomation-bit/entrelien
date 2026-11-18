# Short teaser carnet 16 recréé : nouvelles prises de voix calées sur l'animation du film (plans 01, 03-06) + carte de fin.
import json,re,subprocess,os,sys
os.chdir('/home/claude/prod/c16')
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
TXT={'01':"Je lui avais dit : « Appelez-moi quand vous voulez. »… Il m'a pris au mot.",
 '03':"Un samedi, un homme m'appelle pour une petite difficulté. Je l'aide, tout fonctionne. Avant de raccrocher, il me demande : « Si je n'y arrive pas, je peux vous rappeler ? »",
 '04':"Puis il hésite : « Mais bon… je ne peux pas vous appeler n'importe quand. » Je lui réponds : « Si, si. Appelez-moi quand vous voulez. Si je peux vous aider, je décrocherai. »",
 '05':"J'étais sincère. Dans mon métier, il n'y a pas vraiment de jour ni d'heure. Et puis, c'était samedi.",
 '06':"Dimanche matin, je regarde mon téléphone. Un appel manqué."}
# plage de la voix d'origine dans le film (d'après les sous-titres du film)
ORIG={'01':(0.6,4.45),'03':(11.79,21.2),'04':(21.95,31.39),'05':(32.41,38.6),'06':(39.35,43.14)}
PRE={'01':0.25};POST={'06':0.75}
def segs_of(f,d):
    out=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',f,'-af','silencedetect=noise=-38dB:d=0.22','-f','null','-'],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',out)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',out)]
    sil=list(zip(st,en+[d]*(len(st)-len(en)))); s=[];cur=0
    for a,b in sil:
        if a-cur>0.15: s.append([cur,a])
        cur=b
    if d-cur>0.15: s.append([cur,d])
    return s
def phrases(t): return [x.strip() for x in re.findall(r'.+?(?:[.?!…](?:\s*»)?|$)(?=\s|$)',t) if x.strip()]
t=0;SEGS=[];SUBS=[];blocks={};os.makedirs('tmp',exist_ok=True)
for k in ['01','03','04','05','06']:
    f=f'tts/{k}.mp3';D=dur(f);pre=PRE.get(k,0.35);post=POST.get(k,0.4)
    vs,ve=ORIG[k];r=(ve-vs)/D
    SEGS.append({'k':k,'s':round(t,3),'len':round(pre+D+post,3),'pre':pre,'vs':vs,'r':r})
    blocks[k]=[round(t+pre,3),round(t+pre+D,3)]
    sp=segs_of(f,D);ph=phrases(TXT[k])
    if len(sp)!=len(ph):
        s0,s1=sp[0][0],sp[-1][1];tot=sum(map(len,ph));c=0;sp=[]
        for x in ph: a=s0+(s1-s0)*c/tot;c+=len(x);sp.append([a,s0+(s1-s0)*c/tot])
    for x,(a,b) in zip(ph,sp): SUBS.append([round(t+pre+a,2),round(t+pre+b,2),x])
    print(k,len(sp)==len(ph),round(D,2),round(r,3))
    t+=pre+D+post
CARD=t;CD=dur('tts/cta.mp3');END=round(t+0.3+CD+1.4,2)
blocks['cta']=[round(t+0.3,3),round(t+0.3+CD,3)]
# vo.wav
inp=[];flt=[]
for i,k in enumerate(blocks):
    inp+=['-i',f'tts/{k}.mp3'];ms=int(blocks[k][0]*1000);flt.append(f'[{i}]aresample=48000,aformat=channel_layouts=mono,adelay={ms}[a{i}]')
flt.append(''.join(f'[a{i}]' for i in range(len(blocks)))+f'amix=inputs={len(blocks)}:normalize=0,apad=whole_dur={END}[o]')
subprocess.run(['ffmpeg','-v','error','-y']+inp+['-filter_complex',';'.join(flt),'-map','[o]','-ar','48000','-t',str(END),'vo.wav'],check=True)
json.dump({'blocks':TXT|{'cta':"L'heure de son appel… est dans le Carnet numéro seize."},'mood':'warm','hush':[],'seed':16},open('script.json','w'),ensure_ascii=False)
open('timing.js','w').write('window.TIMING='+json.dumps({'blocks':blocks,'subs':SUBS,'end':END},ensure_ascii=False)+';')
json.dump({'SEGS':SEGS,'SUBS':SUBS,'CARD':CARD,'END':END},open('short_plan.json','w'),ensure_ascii=False)
print('END',END,'CARD',round(CARD,2));[print(s) for s in SUBS]
