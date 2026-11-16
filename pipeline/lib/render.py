# Rendu image par image du film (Chrome headless) + assemblage avec mix.wav
# Usage : python3 render.py <dossier> [stills t1,t2,...]   -> film.mp4 (ou stills/*.jpg)
import asyncio, subprocess, os, sys
from playwright.async_api import async_playwright
FPS=30
D=os.path.abspath(sys.argv[1]); os.chdir(D)
async def part(a,bb,k):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':1920,'height':1080})
        await pg.goto('file://'+D+'/film.html'); await pg.evaluate('window.ready')
        ff=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',f'tmp/part{k}.mp4'],stdin=subprocess.PIPE)
        for i in range(a,bb):
            await pg.evaluate(f'window.renderAt({i/FPS})')
            ff.stdin.write(await pg.screenshot(type='jpeg',quality=90))
            if (i-a)%600==0: print(k,f'{i-a}/{bb-a}',flush=True)
        ff.stdin.close(); ff.wait(); await b.close()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':1920,'height':1080})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+D+'/film.html'); await pg.evaluate('window.ready')
        if errs: print('ERREURS JS',errs); sys.exit(1)
        total=await pg.evaluate('window.TOTAL')
        if len(sys.argv)>2:
            os.makedirs('stills',exist_ok=True)
            ts=[float(x) for x in sys.argv[2].split(',')] if sys.argv[2]!='auto' else None
            if ts is None:
                info=await pg.evaluate('window.SCENES_INFO()'); ts=[]
                for _,a,bb in info: ts+= [round(a+(bb-a)*0.35,2),round(a+(bb-a)*0.85,2)]
            for t in ts:
                await pg.evaluate(f'window.renderAt({t})'); await pg.screenshot(path=f'stills/s_{t:06.2f}.jpg',type='jpeg',quality=80)
            print(await pg.evaluate('window.SCENES_INFO()')); await b.close(); return
        n=int(total*FPS); await b.close()
    K=2; parts=[(k*n//K,(k+1)*n//K) for k in range(K)]
    await asyncio.gather(*[part(a,bb,k) for k,(a,bb) in enumerate(parts)])
    open('tmp/parts.txt','w').write(''.join(f"file 'part{k}.mp4'\n" for k in range(K)))
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i','tmp/parts.txt','-c','copy','tmp/video.mp4'],check=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i','tmp/video.mp4','-i','mix.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart','film.mp4'],check=True)
    print('done',flush=True)
asyncio.run(main())
