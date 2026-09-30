import os
from playwright.sync_api import sync_playwright
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W,H=480,360
with sync_playwright() as p:
  b=p.chromium.launch(); pg=b.new_page()
  for f in sorted(os.listdir('forms')):
    svg=open('forms/'+f).read()
    pg.set_content(svg); x,y,w,h=pg.evaluate("(()=>{const r=document.querySelector('#c').getBBox();return [r.x,r.y,r.width,r.height]})()")
    sc=min(440/w,320/h,2.2); tx=W/2-(x+w/2)*sc; ty=H/2-(y+h/2)*sc+4
    open('forms/'+f,'w').write(svg.replace('<g id="c">',f'<g id="c" transform="translate({tx:.1f} {ty:.1f}) scale({sc:.3f})">',1))
  fs=sorted(os.listdir('forms'))
  open('fsheet.html','w').write('<html><body style="margin:0;background:#fff;font:13px sans-serif">'+''.join(f'<div style="display:inline-block;margin:6px;text-align:center"><img src="forms/{f}" width="300"><br>{f}</div>' for f in fs)+'</body></html>')
  pg=b.new_page(viewport={'width':1300,'height':800}); pg.goto('file://'+os.path.abspath('fsheet.html')); pg.wait_for_timeout(700); pg.screenshot(path='fsheet.png',full_page=True)
  b.close()
