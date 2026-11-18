import asyncio,subprocess,os,sys,json
from playwright.async_api import async_playwright
os.chdir('/home/claude/prod/c16');FPS=30
P=json.load(open('short_plan.json'));END=P['END']
CSS="""html,body{background:#F3EEE4!important;width:1080px;height:1920px}
#short{position:absolute;inset:0;background:#F3EEE4}
#short.night{background:radial-gradient(90% 70% at 50% 45%,#3B4762,#1E2A44)}
#clip{position:absolute;left:81px;top:560px;width:918px;height:880px;overflow:hidden;border-radius:6px;box-shadow:0 6px 30px rgba(30,42,68,.12)}
#stage{position:absolute!important;left:0;top:0;transform-origin:0 0}
#kick{position:absolute;left:90px;top:250px;margin:0;font-family:Caveat,cursive;font-weight:600;font-size:52px;color:#C9922E}
#ttl{position:absolute;left:90px;top:318px;width:900px;margin:0;font-family:Fraunces,Georgia,serif;font-weight:500;font-size:58px;line-height:1.12;color:#1E2A44}
#cap{position:absolute;left:90px;width:900px;top:1480px;margin:0;text-align:center;font-family:"Work Sans",sans-serif;font-weight:500;font-size:46px;line-height:1.28;color:#1E2A44}
#short.night #ttl,#short.night #cap{color:#F3EEE4}
#fade{position:absolute;inset:0;opacity:0}
#endc{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:26px;opacity:0;background:#F3EEE4;text-align:center}
#endc .a{font-family:Fraunces,Georgia,serif;font-weight:500;font-size:64px;line-height:1.15;color:#1E2A44;margin:0;max-width:880px}
#endc .b{font-family:Caveat,cursive;font-weight:600;font-size:110px;color:#C9922E;margin:0}
#endc .c{font-family:"Work Sans",sans-serif;font-weight:500;font-size:44px;color:#4A4D55;margin:0;max-width:860px;line-height:1.3}"""
JS="""c=>{const st=document.getElementById('stage');const $=i=>document.getElementById(i);const sh=document.createElement('div');sh.id='short';document.body.appendChild(sh);
sh.innerHTML='<p id="kick">Carnet de l’Entremetteur n°16</p><p id="ttl">« Appelez-moi quand vous voulez. » Il m’a pris au mot.</p><div id="clip"></div><p id="cap"></p><div id="fade"></div><div id="endc"><p class="a">L’heure de son appel…</p><p class="b">Carnet n°16</p><p class="c">L’histoire complète, sur la chaîne YouTube Entrelien</p></div>';
$('clip').appendChild(st);const s=c.scale;
window.shortAt=function(t){const CAP=$('cap'),FADE=$('fade'),ENDC=$('endc');
 for(const g of c.SEGS){if(t<g.s+g.len){const u=t-g.s;const T=Math.max(0,g.vs+(u-g.pre)*g.r);
   st.style.transform='translate('+(-c.cropx*s)+'px,'+(-c.cropy*s)+'px) scale('+s+')';const id=window.renderAt(T);
   sh.classList.toggle('night',id==='accroche'||id==='question');
   const sub=c.SUBS.find(x=>t>=x[0]-.05&&t<x[1]+.25);CAP.textContent=sub?sub[2]:'';CAP.style.opacity=sub?Math.min(1,(t-sub[0]+.05)/.15,(sub[1]+.25-t)/.15):0;
   const e=Math.min(u,g.len-u);FADE.style.background=sh.classList.contains('night')?'#1E2A44':'#F3EEE4';FADE.style.opacity=(g.s===0&&u<g.len/2)?0:Math.max(0,1-e/.22);ENDC.style.opacity=0;return}}
 const u=t-c.CARD;ENDC.style.opacity=Math.min(1,u/.4);CAP.style.opacity=0}}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto('file://'+os.path.abspath('film.html'));await pg.evaluate('window.ready');await pg.add_style_tag(content=CSS)
        await pg.evaluate(JS,{'scale':0.85,'cropx':840,'cropy':0,'SEGS':P['SEGS'],'SUBS':P['SUBS'],'CARD':P['CARD']})
        if len(sys.argv)>1:
            for t in [float(x) for x in sys.argv[1].split(',')]:
                await pg.evaluate(f'window.shortAt({t})');await pg.screenshot(path=f'stills/s_{t:05.1f}.jpg',type='jpeg',quality=80)
            await b.close();return
        n=int(END*FPS)
        ff=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','tmp/short_video.mp4'],stdin=subprocess.PIPE)
        for i in range(n):
            await pg.evaluate(f'window.shortAt({i/FPS})');ff.stdin.write(await pg.screenshot(type='jpeg',quality=92))
            if i%300==0: print(i,'/',n,flush=True)
        ff.stdin.close();ff.wait();await b.close()
    subprocess.run(['ffmpeg','-v','error','-y','-i','tmp/short_video.mp4','-i','mix.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest','vertical.mp4'],check=True)
    print('done')
asyncio.run(main())
