# Pharmacy on the Park website build.
# Usage: python build.py   -> writes the finished website to _site/ (and a one-file preview to _preview/)
# Requires: pip install pillow playwright && playwright install chromium
import re, json, os, base64, glob, shutil
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
s=open('src/site.tpl.html').read()
for k,f in [('CSS_BASE','css_base.txt'),('ICONS','icons.txt'),('MAP','map.txt'),('LIB','library.json')]:
  s=s.replace('{{'+k+'}}',open('src/'+f).read())
LOGO_B64=base64.b64encode(open('src/logo.svg','rb').read()).decode()
s=s.replace('{{LOGO}}',LOGO_B64)
LOGO_DARK_B64=base64.b64encode(open('src/logo-dark.svg','rb').read()).decode()   # white-lettering version for the dark footer
s=s.replace('{{LOGODARK}}',LOGO_DARK_B64)
LIBJSON=open('src/library.json').read()
FORMS=sorted(f[:-4] for f in os.listdir('src/forms') if f.endswith('.svg'))
FDATA={k:'data:image/svg+xml;base64,'+base64.b64encode(open('src/forms/'+k+'.svg','rb').read()).decode() for k in FORMS}
ART=s.replace('{{MEDPAGES}}','false').replace('{{FORMIMG}}',json.dumps(FDATA))
ART=re.sub(r'\{\{FORM:([a-z-]+)\}\}',lambda m:FDATA[m.group(1)],ART)
s=s.replace('{{MEDPAGES}}','true').replace('{{FORMIMG}}',json.dumps({k:'/forms/'+k+'.svg' for k in FORMS}))
s=re.sub(r'\{\{FORM:([a-z-]+)\}\}',lambda m:'/forms/'+m.group(1)+'.svg',s)
assert not [x for x in re.findall(r'\{\{([A-Z_]+)', s) if x not in ('LG','FORM')], re.findall(r'\{\{([A-Z_]+)', s)
LOGOF={f.rsplit('.',1)[0]:f for f in os.listdir('src/logos')}
MIME={'svg':'image/svg+xml','png':'image/png','jpg':'image/jpeg'}
def lg_data(m):
  f=LOGOF[m.group(1)]; return 'data:'+MIME[f.rsplit('.',1)[1]]+';base64,'+base64.b64encode(open('src/logos/'+f,'rb').read()).decode()
os.makedirs('_preview',exist_ok=True); open('_preview/pharmacy-on-the-park.html','w').write(re.sub(r'\{\{LG:([a-z0-9-]+)\}\}',lg_data,ART))   # artifact version
s=re.sub(r'\{\{LG:([a-z0-9-]+)\}\}',lambda m:'/logos/'+LOGOF[m.group(1)],s)
DOMAIN='https://pharmacyonthepark.com'
shutil.rmtree('_site',ignore_errors=True); os.makedirs('_site')
shutil.copy('src/logo.svg','_site/logo.svg'); shutil.copy('src/logo-dark.svg','_site/logo-dark.svg')
s=s.replace('data:image/svg+xml;base64,'+LOGO_B64,'/logo.svg').replace('data:image/svg+xml;base64,'+LOGO_DARK_B64,'/logo-dark.svg')
lg=Image.open('src/logo.png').convert('RGB'); og=Image.new('RGB',(1200,630),'white')
lg.thumbnail((980,420)); og.paste(lg,((1200-lg.width)//2,(630-lg.height)//2)); og.save('_site/og-image.png',optimize=True)
open('_site/favicon.svg','w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect x="4" y="18" width="30" height="28" rx="14" fill="#5FBA51"/><rect x="18" y="18" width="16" height="28" fill="#5FBA51"/><rect x="30" y="18" width="30" height="28" rx="14" fill="#005687"/><rect x="30" y="18" width="16" height="28" fill="#005687"/></svg>')
start=s.index('<!-- ================= HOME ================= -->'); end=s.index('<section class="cta-band">')
prefix=s[:start]; suffix=s[end:]; body=s[start:end]
pages={}
for b in re.split(r'(?=<!-- ================= [A-Z ]+ ================= -->)',body):
  m=re.search(r'<div class="page" id="p-([a-z-]+)">',b)
  if m: pages[m.group(1)]=b.replace(m.group(0),'<div class="page on" id="p-'+m.group(1)+'">')
URL={'home':'/','retail':'/retail-pharmacy/','supplements':'/retail-pharmacy/supplements/','discount':'/retail-pharmacy/discount-program/','insurance':'/retail-pharmacy/insurance/','service':'/retail-pharmacy/fast-service/','otc':'/retail-pharmacy/otc-products/','compounding':'/compounding/','hormone-therapy':'/compounding/hormone-therapy/','mcas':'/compounding/mast-cell-activation-syndrome/','veterinary':'/veterinary/','fip':'/veterinary/fip-medication/','vet-lunch':'/veterinary/lunch-and-learn/','prescribers':'/prescribers/','about':'/about/','quality':'/about/quality/','choose':'/how-to-choose-a-compounding-pharmacy/','contact':'/contact/','medications':'/medications/','ldn':'/low-dose-naltrexone/'}
EXTRA={'send':'/contact/#send-sec','about-quality':'/about/#about-quality-sec'}
TOP={'ldn':'compounding','supplements':'retail','discount':'retail','insurance':'retail','service':'retail','otc':'retail','mcas':'compounding','vet-lunch':'veterinary','hormone-therapy':'compounding','fip':'veterinary','quality':'about','choose':'about'}
META={
'ldn':("Low-Dose Naltrexone (LDN) Tablets $60 for 90 | Florida Pharmacy","Low-dose naltrexone (LDN) 1.5 mg, 3 mg and 4.5 mg tablets: $60 for 90 tablets. Compounded in Oviedo near Orlando. Transfers welcome; shipping across Florida. Call 407-977-9779."),
'medications':("Compounded Medication Library | Pharmacy on the Park","Search 230+ medications we compound for people and pets in Oviedo, FL: dosage forms, flavors, common uses, side effects and research links."),
'home':("Pharmacy on the Park | Compounding Pharmacy in Oviedo, FL","Family-owned compounding pharmacy in Oviedo, FL. LDN 1.5, 3 and 4.5 mg tablets $60 for 90. Hormone therapy, pet medications and FIP treatment. Accredited. Call 407-977-9779."),
'retail':("Retail Pharmacy in Oviedo, FL | Transfers & Refills","Switch to Pharmacy on the Park in Oviedo, FL. We handle prescription transfers and refills, accept most insurance plans, and a real person answers the phone."),
'supplements':("Professional Supplements in Oviedo, FL | Pharmacy on the Park","Shop Pure Encapsulations, Ortho Molecular Products, Genestra, MaryRuth's and more in Oviedo, FL. We special order supplements and keep them stocked for you."),
'discount':("$9 for 90 Days: Low-Cost Medications in Oviedo, FL","Hundreds of medications for $9 for a 90-day supply at Pharmacy on the Park in Oviedo, FL. No insurance, no discount card and no sign-up. Competitive cash prices and price matching."),
'insurance':("Insurance Accepted | Pharmacy on the Park, Oviedo FL","Pharmacy on the Park in Oviedo, FL accepts most prescription insurance plans. Call 407-977-9779 to check your plan, transfer your prescriptions or ask about cash prices."),
'service':("Fast, Reliable Pharmacy Service in Oviedo, FL","Same-day prescription fills, short wait times and a text when your prescription is ready. Refill by phone, text, online or with our MobileScripts app."),
'otc':("Over-the-Counter Products in Oviedo, FL | Pharmacy on the Park","Cold and flu, pain relief, allergy, first aid and baby care products in Oviedo, FL, with a pharmacist to help you choose. 784 S. Central Ave. 407-977-9779."),
'mcas':("Compounding for MCAS (Mast Cell Activation Syndrome) | Oviedo, FL","Dye-free and allergen-free compounded medications for mast cell activation syndrome: ketotifen, antihistamines, famotidine, montelukast and LDN, in custom strengths. Oviedo, FL. 407-977-9779."),
'vet-lunch':("Lunch and Learn for Veterinary Teams | Pharmacy on the Park","Veterinary practices: book a lunch and learn and we'll come to your clinic to share compounded pet medications, flavors, pricing and same-day to 24-hour turnaround. Oviedo, FL."),
'compounding':("Compounding Pharmacy in Oviedo, FL | Pharmacy on the Park","Custom compounded medications in Oviedo, FL: capsules, creams, troches, rapid-dissolve tablets and more. Accredited, USP <800> compliant, nonsterile and select sterile."),
'hormone-therapy':("Compounded Hormone Therapy in Oviedo, FL","Compounded bioidentical hormone therapy in Oviedo, FL: estradiol, estriol, Biest, progesterone, testosterone and DHEA, prepared as your clinician prescribes."),
'veterinary':("Veterinary Compounding Pharmacy in Oviedo, FL","Compounded pet medications for dogs, cats and exotics: flavored liquids, treats, transdermals and more. Pickup in Oviedo or shipping across Florida."),
'fip':("GS-441524 for Cats with FIP | Florida Pharmacy","Pharmacy on the Park fills veterinary prescriptions for GS-441524 to treat FIP in cats. Pickup in Oviedo or shipping within Florida. Call 407-977-9779."),
'prescribers':("For Prescribers | Compounding Partner in Central Florida","Human and veterinary prescribers: talk formulations with a pharmacist. Fax 407-977-0079, phone 407-977-9779. Accredited, USP <800> compliant compounding pharmacy."),
'about':("About Pharmacy on the Park | Family-Owned in Oviedo, FL","Family-owned pharmacy in Oviedo, FL, opened in 2022 and led by Ian Tasman, PharmD. Accredited and USP <800> compliant, and active with Orlando Science Center, Girl Scouts and local teams."),
'quality':("Quality & Sourcing | USP <795>, <797> & <800> | Pharmacy on the Park","Pharmacy on the Park exceeds Florida compounding standards: USP <800> compliant, meets USP <795> and <797>, every sterile batch tested by Pharmetric Labs and a certified clean room."),
'choose':("How to Choose a Compounding Pharmacy | Pharmacy on the Park","What to look for in a compounding pharmacy: accreditation, USP <795>, <797> and <800>, lab standards, ingredient sourcing, independent testing and written procedures, plus questions to ask."),
'contact':("Contact & Directions | Pharmacy on the Park, Oviedo FL","784 S. Central Ave, Oviedo, FL 32765. Phone 407-977-9779, fax 407-977-0079. Hours, directions, reviews and how to send a prescription."),
}
NAMES={'ldn':'Low-Dose Naltrexone (LDN)','medications':'Medication Library','supplements':'Supplements','discount':'$9 for 90 Days','insurance':'Insurance','service':'Fast, Reliable Service','otc':'Over-the-Counter Products','mcas':'Mast Cell Activation Syndrome (MCAS)','vet-lunch':'Lunch and Learn for Veterinary Teams','retail':'Retail Pharmacy','compounding':'Human Compounding','hormone-therapy':'Hormone Therapy','veterinary':'Veterinary Pharmacy','fip':'FIP Medication','prescribers':'For Prescribers','about':'About Us','quality':'Quality and Sourcing','choose':'How to Choose a Compounding Pharmacy','contact':'Contact'}
business={"@context":"https://schema.org","@type":"Pharmacy","@id":DOMAIN+"/#pharmacy","name":"Pharmacy on the Park","url":DOMAIN+"/","logo":DOMAIN+"/logo.svg","image":DOMAIN+"/og-image.png",
 "description":"Family-owned retail and compounding pharmacy in Oviedo, Florida serving patients, pet owners and prescriber offices.",
 "telephone":"+1-407-977-9779","faxNumber":"+1-407-977-0079","email":"info@pharmacyonthepark.com",
 "address":{"@type":"PostalAddress","streetAddress":"784 S Central Ave","addressLocality":"Oviedo","addressRegion":"FL","postalCode":"32765","addressCountry":"US"},
 "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"18:00"},{"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"09:00","closes":"12:00"}],
 "areaServed":[{"@type":"City","name":"Oviedo"},{"@type":"State","name":"Florida"}],
 "sameAs":["https://www.facebook.com/oviedopharmacyonthepark/","https://www.instagram.com/pharmacyonthepark/"],
 "founder":{"@type":"Person","name":"Ian Tasman","jobTitle":"Owner and Pharmacist"},"foundingDate":"2022"}
def fix_links(h):
  def r(m):
    k=m.group(1)
    return 'href="'+URL[k]+'"' if k in URL else ('href="'+EXTRA[k]+'"' if k in EXTRA else m.group(0))
  return re.sub(r'href="#([a-z-]+)"',r,h)
def unhtml(x): return re.sub('<.*?>','',x).replace('&lt;','<').replace('&gt;','>').replace('&amp;','&')
faq=[{"@type":"Question","name":unhtml(q),"acceptedAnswer":{"@type":"Answer","text":unhtml(a)}} for q,a in re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>',pages['home'])]
esc=lambda x:x.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')
for key,html in pages.items():
  title,desc=META[key]; url=DOMAIN+URL[key]; ld=[business]
  if key=='ldn':
    for st in ('1.5 mg','3 mg','4.5 mg'):
      ld.append({"@context":"https://schema.org","@type":"Product","name":"Low-Dose Naltrexone (LDN) "+st+" Tablets, 90 count","description":"Compounded low-dose naltrexone "+st+" tablets prepared from a prescription at Pharmacy on the Park in Oviedo, Florida.","image":DOMAIN+"/forms/tablet.svg","brand":{"@type":"Organization","name":"Pharmacy on the Park"},"offers":{"@type":"Offer","price":"60.00","priceCurrency":"USD","availability":"https://schema.org/InStock","url":DOMAIN+"/low-dose-naltrexone/","seller":{"@id":DOMAIN+"/#pharmacy"},"eligibleRegion":{"@type":"State","name":"Florida"}}})
    ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":unhtml(q),"acceptedAnswer":{"@type":"Answer","text":unhtml(a)}} for q,a in re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>',html)]})
  if key=='home':
    ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":faq})
  else:
    c=[{"@type":"ListItem","position":1,"name":"Home","item":DOMAIN+"/"}]
    if key in TOP: c.append({"@type":"ListItem","position":2,"name":NAMES[TOP[key]],"item":DOMAIN+URL[TOP[key]]})
    c.append({"@type":"ListItem","position":len(c)+1,"name":NAMES[key],"item":url})
    ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":c})
  head=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#005687">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pharmacy on the Park">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="US-FL"><meta name="geo.placename" content="Oviedo">
'''+''.join('<script type="application/ld+json">'+json.dumps(x,ensure_ascii=False)+'</script>\n' for x in ld)
  p=prefix.replace('<title>Pharmacy on the Park</title>\n',''); i=p.index('</style>')+8
  page=fix_links(head+p[:i]+'\n</head>\n<body>\n'+p[i:]+html+suffix+'\n</body>\n</html>\n')
  top=TOP.get(key,key)
  page=page.replace(f'<a class="nl" href="{URL[top]}">',f'<a class="nl" href="{URL[top]}" aria-current="page">',1)
  if key in TOP: page=page.replace(f'<a href="{URL[key]}">',f'<a href="{URL[key]}" aria-current="page">',1)
  for a,b in [("window.addEventListener('hashchange', show); show();",""),("  form.addEventListener('submit', function(e){","  if(form) form.addEventListener('submit', function(e){"),('alt="Pharmacy on the Park"','alt="Pharmacy on the Park logo" width="254" height="104"')]:
    assert a in page, a; page=page.replace(a,b)
  if key!='medications': page=page.replace(LIBJSON,'null')
  d='_site'+URL[key]; os.makedirs(d,exist_ok=True); open(d+'index.html','w').write(page)
# ---- one page per medication ----
LIB=json.loads(LIBJSON)
tmpl=open('_site/medications/index.html').read()
hs=tmpl.index('<div class="page on" id="p-medications">'); he=tmpl.index('<section class="cta-band">')
MEDURLS=[]
from urllib.parse import quote
from playwright.sync_api import sync_playwright
with sync_playwright() as _p:
  _b=_p.chromium.launch(); _pg=_b.new_page()
  _pg.goto('file://'+os.path.abspath('_site/medications/index.html')); _pg.wait_for_timeout(300)
  BODIES=_pg.evaluate("(()=>{const o={}; (window.__LIB||[]).forEach(x=>{o[x.id]=window.renderDrug(x)}); return o;})()")
  _b.close()
assert len(BODIES)==len(LIB), (len(BODIES),len(LIB))
for x in LIB:
  nm=x['name']; base=re.sub(r'\s*\(.*?\)','',nm)
  pets_only=x['aud']==['pets']
  FM={'Cream':'cream','Ointment':'cream','Gel':'cream','Serum':'cream','Lotion':'cream','Foam':'cream','Paste':'cream','Capsule':'capsule','Slow-release capsule':'capsule','Powder':'capsule','Tablet':'tablet','Rapid-dissolve tablet':'rdt','Troche':'troche','Oral liquid':'suspension','Solution':'suspension','Transdermal gel (PLO)':'plo','Ear pack':'earpack','Chewable treat':'treat','Suppository':'suppository','Vaginal preparation':'pearl','Nasal spray':'nasal','Lollipop':'lollipop','Mouthwash':'mouthwash'}
  f0=(x['forms'] or ['Capsule'])[0]
  FIMG='/forms/'+(('suspension-pet' if pets_only else 'suspension') if f0=='Flavored oral suspension' else FM.get(f0,'capsule'))+'.svg'
  who=' and '.join('pets' if a=='pets' else 'people' for a in x['aud'])
  title=f"{base} Compounding in Oviedo, FL | Pharmacy on the Park"
  forms=', '.join(x['forms']) or 'custom forms'
  desc=f"{base}: {x['uses']} Compounded for {who} as {forms.lower()}. Pharmacy on the Park, Oviedo, FL. Call 407-977-9779."
  if len(desc)>300: desc=desc[:297].rsplit(' ',1)[0]+'...'
  pq=quote(base+(' AND (dogs OR cats)' if pets_only else '')); dq=quote(base)
  chips=lambda L:''.join(f'<span>{esc(v)}</span>' for v in L)
  body='<div class="page on" id="p-med">'+BODIES[x['id']]+'</div>\n\n'
  page=tmpl[:hs]+body+tmpl[he:]
  page=page.replace(LIBJSON,'null')
  u='/medications/'+x['id']+'/'; url=DOMAIN+u
  page=re.sub(r'<title>.*?</title>','<title>'+esc(title)+'</title>',page,1)
  page=re.sub(r'<meta name="description" content=".*?">','<meta name="description" content="'+esc(desc)+'">',page,1)
  page=re.sub(r'<meta property="og:title" content=".*?">','<meta property="og:title" content="'+esc(title)+'">',page,1)
  page=re.sub(r'<meta property="og:description" content=".*?">','<meta property="og:description" content="'+esc(desc)+'">',page,1)
  page=page.replace('<link rel="canonical" href="'+DOMAIN+'/medications/">','<link rel="canonical" href="'+url+'">').replace('<meta property="og:url" content="'+DOMAIN+'/medications/">','<meta property="og:url" content="'+url+'">')
  crumbs={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":DOMAIN+"/"},{"@type":"ListItem","position":2,"name":"Medication Library","item":DOMAIN+"/medications/"},{"@type":"ListItem","position":3,"name":nm,"item":url}]}
  page=re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "BreadcrumbList".*?</script>','<script type="application/ld+json">'+json.dumps(crumbs,ensure_ascii=False)+'</script>',page,1,flags=re.S)
  who2='veterinarian' if pets_only else 'prescriber'
  faq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in [(f"What is {base}?",x['how']),("What is it used for?",x['uses']),("What are the common side effects?",x['side']),("Who should use caution?",x['avoid']),("Are compounded medications FDA-approved?","No. Compounded medications are prepared for an individual patient from a prescription and are not FDA-approved."),("Do I need a prescription?",f"Yes. Your {who2} sends the prescription to Pharmacy on the Park.")]]}
  page=page.replace('</head>','<script type="application/ld+json">'+json.dumps(faq,ensure_ascii=False)+'</script>\n</head>',1)
  os.makedirs('_site'+u,exist_ok=True); open('_site'+u+'index.html','w').write(page); MEDURLS.append(u)
shutil.copytree('src/logos','_site/logos'); shutil.copytree('src/forms','_site/forms'); shutil.copytree('src/photos','_site/photos')
os.makedirs('_site/media',exist_ok=True); open('_site/media/README.txt','w').write('Retail page background video: save a short, silent, looping clip of your nonsterile compounding lab here as compounding-nonsterile.mp4 (MP4/H.264, 10-30 seconds, under 10 MB, 1920x1080). It plays softly behind the Retail Pharmacy banner. Until the file is here, the banner shows without video.\n')
os.makedirs('_site/downloads',exist_ok=True); shutil.copy('src/downloads/hrt-order-form.pdf','_site/downloads/hrt-order-form.pdf')
open('_site/robots.txt','w').write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
open('_site/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{DOMAIN}{u}</loc><lastmod>2026-10-01</lastmod><priority>{"1.0" if u in ("/","/low-dose-naltrexone/") else ("0.6" if u.count("/")>2 and u.startswith("/medications/") else "0.8")}</priority></url>\n' for u in list(URL.values())+MEDURLS)+'</urlset>\n')
print('built')
# Pharmacy on the Park website build.
# Usage: python build.py   -> writes the finished website to _site/ (and a one-file preview to _preview/)
# Requires: pip install pillow playwright && playwright install chromium
import re, json, os, base64, glob, shutil
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
s=open('src/site.tpl.html').read()
for k,f in [('CSS_BASE','css_base.txt'),('ICONS','icons.txt'),('MAP','map.txt'),('LIB','library.json')]:
  s=s.replace('{{'+k+'}}',open('src/'+f).read())
LOGO_B64=base64.b64encode(open('src/logo.svg','rb').read()).decode()
s=s.replace('{{LOGO}}',LOGO_B64)
LIBJSON=open('src/library.json').read()
FORMS=sorted(f[:-4] for f in os.listdir('src/forms') if f.endswith('.svg'))
FDATA={k:'data:image/svg+xml;base64,'+base64.b64encode(open('src/forms/'+k+'.svg','rb').read()).decode() for k in FORMS}
ART=s.replace('{{MEDPAGES}}','false').replace('{{FORMIMG}}',json.dumps(FDATA))
ART=re.sub(r'\{\{FORM:([a-z-]+)\}\}',lambda m:FDATA[m.group(1)],ART)
s=s.replace('{{MEDPAGES}}','true').replace('{{FORMIMG}}',json.dumps({k:'/forms/'+k+'.svg' for k in FORMS}))
s=re.sub(r'\{\{FORM:([a-z-]+)\}\}',lambda m:'/forms/'+m.group(1)+'.svg',s)
assert not [x for x in re.findall(r'\{\{([A-Z_]+)', s) if x not in ('LG','FORM')], re.findall(r'\{\{([A-Z_]+)', s)
LOGOF={f.rsplit('.',1)[0]:f for f in os.listdir('src/logos')}
MIME={'svg':'image/svg+xml','png':'image/png','jpg':'image/jpeg'}
def lg_data(m):
  f=LOGOF[m.group(1)]; return 'data:'+MIME[f.rsplit('.',1)[1]]+';base64,'+base64.b64encode(open('src/logos/'+f,'rb').read()).decode()
os.makedirs('_preview',exist_ok=True); open('_preview/pharmacy-on-the-park.html','w').write(re.sub(r'\{\{LG:([a-z0-9-]+)\}\}',lg_data,ART))   # artifact version
s=re.sub(r'\{\{LG:([a-z0-9-]+)\}\}',lambda m:'/logos/'+LOGOF[m.group(1)],s)
DOMAIN='https://pharmacyonthepark.com'
shutil.rmtree('_site',ignore_errors=True); os.makedirs('_site')
shutil.copy('src/logo.svg','_site/logo.svg')
s=s.replace('data:image/svg+xml;base64,'+LOGO_B64,'/logo.svg')
lg=Image.open('src/logo.png').convert('RGB'); og=Image.new('RGB',(1200,630),'white')
lg.thumbnail((980,420)); og.paste(lg,((1200-lg.width)//2,(630-lg.height)//2)); og.save('_site/og-image.png',optimize=True)
open('_site/favicon.svg','w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect x="4" y="18" width="30" height="28" rx="14" fill="#5FBA51"/><rect x="18" y="18" width="16" height="28" fill="#5FBA51"/><rect x="30" y="18" width="30" height="28" rx="14" fill="#005687"/><rect x="30" y="18" width="16" height="28" fill="#005687"/></svg>')
start=s.index('<!-- ================= HOME ================= -->'); end=s.index('<section class="cta-band">')
prefix=s[:start]; suffix=s[end:]; body=s[start:end]
pages={}
for b in re.split(r'(?=<!-- ================= [A-Z ]+ ================= -->)',body):
  m=re.search(r'<div class="page" id="p-([a-z-]+)">',b)
  if m: pages[m.group(1)]=b.replace(m.group(0),'<div class="page on" id="p-'+m.group(1)+'">')
URL={'home':'/','retail':'/retail-pharmacy/','supplements':'/retail-pharmacy/supplements/','discount':'/retail-pharmacy/discount-program/','insurance':'/retail-pharmacy/insurance/','service':'/retail-pharmacy/fast-service/','otc':'/retail-pharmacy/otc-products/','compounding':'/compounding/','hormone-therapy':'/compounding/hormone-therapy/','mcas':'/compounding/mast-cell-activation-syndrome/','veterinary':'/veterinary/','fip':'/veterinary/fip-medication/','vet-lunch':'/veterinary/lunch-and-learn/','prescribers':'/prescribers/','about':'/about/','quality':'/about/quality/','choose':'/how-to-choose-a-compounding-pharmacy/','contact':'/contact/','medications':'/medications/','ldn':'/low-dose-naltrexone/'}
EXTRA={'send':'/contact/#send-sec','about-quality':'/about/#about-quality-sec'}
TOP={'ldn':'compounding','supplements':'retail','discount':'retail','insurance':'retail','service':'retail','otc':'retail','mcas':'compounding','vet-lunch':'veterinary','hormone-therapy':'compounding','fip':'veterinary','quality':'about','choose':'about'}
META={
'ldn':("Low-Dose Naltrexone (LDN) Tablets $60 for 90 | Florida Pharmacy","Low-dose naltrexone (LDN) 1.5 mg, 3 mg and 4.5 mg tablets: $60 for 90 tablets. Compounded in Oviedo near Orlando. Transfers welcome; shipping across Florida. Call 407-977-9779."),
'medications':("Compounded Medication Library | Pharmacy on the Park","Search 230+ medications we compound for people and pets in Oviedo, FL: dosage forms, flavors, common uses, side effects and research links."),
'home':("Pharmacy on the Park | Compounding Pharmacy in Oviedo, FL","Family-owned compounding pharmacy in Oviedo, FL. LDN 1.5, 3 and 4.5 mg tablets $60 for 90. Hormone therapy, pet medications and FIP treatment. Accredited. Call 407-977-9779."),
'retail':("Retail Pharmacy in Oviedo, FL | Transfers & Refills","Switch to Pharmacy on the Park in Oviedo, FL. We handle prescription transfers and refills, accept most insurance plans, and a real person answers the phone."),
'supplements':("Professional Supplements in Oviedo, FL | Pharmacy on the Park","Shop Pure Encapsulations, Ortho Molecular Products, Genestra, MaryRuth's and more in Oviedo, FL. We special order supplements and keep them stocked for you."),
'discount':("$9 for 90 Days: Low-Cost Medications in Oviedo, FL","Hundreds of medications for $9 for a 90-day supply at Pharmacy on the Park in Oviedo, FL. No insurance, no discount card and no sign-up. Competitive cash prices and price matching."),
'insurance':("Insurance Accepted | Pharmacy on the Park, Oviedo FL","Pharmacy on the Park in Oviedo, FL accepts most prescription insurance plans. Call 407-977-9779 to check your plan, transfer your prescriptions or ask about cash prices."),
'service':("Fast, Reliable Pharmacy Service in Oviedo, FL","Same-day prescription fills, short wait times and a text when your prescription is ready. Refill by phone, text, online or with our MobileScripts app."),
'otc':("Over-the-Counter Products in Oviedo, FL | Pharmacy on the Park","Cold and flu, pain relief, allergy, first aid and baby care products in Oviedo, FL, with a pharmacist to help you choose. 784 S. Central Ave. 407-977-9779."),
'mcas':("Compounding for MCAS (Mast Cell Activation Syndrome) | Oviedo, FL","Dye-free and allergen-free compounded medications for mast cell activation syndrome: ketotifen, antihistamines, famotidine, montelukast and LDN, in custom strengths. Oviedo, FL. 407-977-9779."),
'vet-lunch':("Lunch and Learn for Veterinary Teams | Pharmacy on the Park","Veterinary practices: book a lunch and learn and we'll come to your clinic to share compounded pet medications, flavors, pricing and same-day to 24-hour turnaround. Oviedo, FL."),
'compounding':("Compounding Pharmacy in Oviedo, FL | Pharmacy on the Park","Custom compounded medications in Oviedo, FL: capsules, creams, troches, rapid-dissolve tablets and more. Accredited, USP <800> compliant, nonsterile and select sterile."),
'hormone-therapy':("Compounded Hormone Therapy in Oviedo, FL","Compounded bioidentical hormone therapy in Oviedo, FL: estradiol, estriol, Biest, progesterone, testosterone and DHEA, prepared as your clinician prescribes."),
'veterinary':("Veterinary Compounding Pharmacy in Oviedo, FL","Compounded pet medications for dogs, cats and exotics: flavored liquids, treats, transdermals and more. Pickup in Oviedo or shipping across Florida."),
'fip':("GS-441524 for Cats with FIP | Florida Pharmacy","Pharmacy on the Park fills veterinary prescriptions for GS-441524 to treat FIP in cats. Pickup in Oviedo or shipping within Florida. Call 407-977-9779."),
'prescribers':("For Prescribers | Compounding Partner in Central Florida","Human and veterinary prescribers: talk formulations with a pharmacist. Fax 407-977-0079, phone 407-977-9779. Accredited, USP <800> compliant compounding pharmacy."),
'about':("About Pharmacy on the Park | Family-Owned in Oviedo, FL","Family-owned pharmacy in Oviedo, FL, opened in 2022 and led by Ian Tasman, PharmD. Accredited and USP <800> compliant, and active with Orlando Science Center, Girl Scouts and local teams."),
'quality':("Quality & Sourcing | USP <795>, <797> & <800> | Pharmacy on the Park","Pharmacy on the Park exceeds Florida compounding standards: USP <800> compliant, meets USP <795> and <797>, every sterile batch tested by Pharmetric Labs and a certified clean room."),
'choose':("How to Choose a Compounding Pharmacy | Pharmacy on the Park","What to look for in a compounding pharmacy: accreditation, USP <795>, <797> and <800>, lab standards, ingredient sourcing, independent testing and written procedures, plus questions to ask."),
'contact':("Contact & Directions | Pharmacy on the Park, Oviedo FL","784 S. Central Ave, Oviedo, FL 32765. Phone 407-977-9779, fax 407-977-0079. Hours, directions, reviews and how to send a prescription."),
}
NAMES={'ldn':'Low-Dose Naltrexone (LDN)','medications':'Medication Library','supplements':'Supplements','discount':'$9 for 90 Days','insurance':'Insurance','service':'Fast, Reliable Service','otc':'Over-the-Counter Products','mcas':'Mast Cell Activation Syndrome (MCAS)','vet-lunch':'Lunch and Learn for Veterinary Teams','retail':'Retail Pharmacy','compounding':'Human Compounding','hormone-therapy':'Hormone Therapy','veterinary':'Veterinary Pharmacy','fip':'FIP Medication','prescribers':'For Prescribers','about':'About Us','quality':'Quality and Sourcing','choose':'How to Choose a Compounding Pharmacy','contact':'Contact'}
business={"@context":"https://schema.org","@type":"Pharmacy","@id":DOMAIN+"/#pharmacy","name":"Pharmacy on the Park","url":DOMAIN+"/","logo":DOMAIN+"/logo.svg","image":DOMAIN+"/og-image.png",
 "description":"Family-owned retail and compounding pharmacy in Oviedo, Florida serving patients, pet owners and prescriber offices.",
 "telephone":"+1-407-977-9779","faxNumber":"+1-407-977-0079","email":"info@pharmacyonthepark.com",
 "address":{"@type":"PostalAddress","streetAddress":"784 S Central Ave","addressLocality":"Oviedo","addressRegion":"FL","postalCode":"32765","addressCountry":"US"},
 "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"18:00"},{"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"09:00","closes":"12:00"}],
 "areaServed":[{"@type":"City","name":"Oviedo"},{"@type":"State","name":"Florida"}],
 "sameAs":["https://www.facebook.com/oviedopharmacyonthepark/","https://www.instagram.com/pharmacyonthepark/"],
 "founder":{"@type":"Person","name":"Ian Tasman","jobTitle":"Owner and Pharmacist"},"foundingDate":"2022"}
def fix_links(h):
  def r(m):
    k=m.group(1)
    return 'href="'+URL[k]+'"' if k in URL else ('href="'+EXTRA[k]+'"' if k in EXTRA else m.group(0))
  return re.sub(r'href="#([a-z-]+)"',r,h)
def unhtml(x): return re.sub('<.*?>','',x).replace('&lt;','<').replace('&gt;','>').replace('&amp;','&')
faq=[{"@type":"Question","name":unhtml(q),"acceptedAnswer":{"@type":"Answer","text":unhtml(a)}} for q,a in re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>',pages['home'])]
esc=lambda x:x.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')
for key,html in pages.items():
  title,desc=META[key]; url=DOMAIN+URL[key]; ld=[business]
  if key=='ldn':
    for st in ('1.5 mg','3 mg','4.5 mg'):
      ld.append({"@context":"https://schema.org","@type":"Product","name":"Low-Dose Naltrexone (LDN) "+st+" Tablets, 90 count","description":"Compounded low-dose naltrexone "+st+" tablets prepared from a prescription at Pharmacy on the Park in Oviedo, Florida.","image":DOMAIN+"/forms/tablet.svg","brand":{"@type":"Organization","name":"Pharmacy on the Park"},"offers":{"@type":"Offer","price":"60.00","priceCurrency":"USD","availability":"https://schema.org/InStock","url":DOMAIN+"/low-dose-naltrexone/","seller":{"@id":DOMAIN+"/#pharmacy"},"eligibleRegion":{"@type":"State","name":"Florida"}}})
    ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":unhtml(q),"acceptedAnswer":{"@type":"Answer","text":unhtml(a)}} for q,a in re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>',html)]})
  if key=='home':
    ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":faq})
  else:
    c=[{"@type":"ListItem","position":1,"name":"Home","item":DOMAIN+"/"}]
    if key in TOP: c.append({"@type":"ListItem","position":2,"name":NAMES[TOP[key]],"item":DOMAIN+URL[TOP[key]]})
    c.append({"@type":"ListItem","position":len(c)+1,"name":NAMES[key],"item":url})
    ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":c})
  head=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#005687">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pharmacy on the Park">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="US-FL"><meta name="geo.placename" content="Oviedo">
'''+''.join('<script type="application/ld+json">'+json.dumps(x,ensure_ascii=False)+'</script>\n' for x in ld)
  p=prefix.replace('<title>Pharmacy on the Park</title>\n',''); i=p.index('</style>')+8
  page=fix_links(head+p[:i]+'\n</head>\n<body>\n'+p[i:]+html+suffix+'\n</body>\n</html>\n')
  top=TOP.get(key,key)
  page=page.replace(f'<a class="nl" href="{URL[top]}">',f'<a class="nl" href="{URL[top]}" aria-current="page">',1)
  if key in TOP: page=page.replace(f'<a href="{URL[key]}">',f'<a href="{URL[key]}" aria-current="page">',1)
  for a,b in [("window.addEventListener('hashchange', show); show();",""),("  form.addEventListener('submit', function(e){","  if(form) form.addEventListener('submit', function(e){"),('alt="Pharmacy on the Park"','alt="Pharmacy on the Park logo" width="254" height="104"')]:
    assert a in page, a; page=page.replace(a,b)
  if key!='medications': page=page.replace(LIBJSON,'null')
  d='_site'+URL[key]; os.makedirs(d,exist_ok=True); open(d+'index.html','w').write(page)
# ---- one page per medication ----
LIB=json.loads(LIBJSON)
tmpl=open('_site/medications/index.html').read()
hs=tmpl.index('<div class="page on" id="p-medications">'); he=tmpl.index('<section class="cta-band">')
MEDURLS=[]
from urllib.parse import quote
from playwright.sync_api import sync_playwright
with sync_playwright() as _p:
  _b=_p.chromium.launch(); _pg=_b.new_page()
  _pg.goto('file://'+os.path.abspath('_site/medications/index.html')); _pg.wait_for_timeout(300)
  BODIES=_pg.evaluate("(()=>{const o={}; (window.__LIB||[]).forEach(x=>{o[x.id]=window.renderDrug(x)}); return o;})()")
  _b.close()
assert len(BODIES)==len(LIB), (len(BODIES),len(LIB))
for x in LIB:
  nm=x['name']; base=re.sub(r'\s*\(.*?\)','',nm)
  pets_only=x['aud']==['pets']
  FM={'Cream':'cream','Ointment':'cream','Gel':'cream','Serum':'cream','Lotion':'cream','Foam':'cream','Paste':'cream','Capsule':'capsule','Slow-release capsule':'capsule','Powder':'capsule','Tablet':'tablet','Rapid-dissolve tablet':'rdt','Troche':'troche','Oral liquid':'suspension','Solution':'suspension','Transdermal gel (PLO)':'plo','Ear pack':'earpack','Chewable treat':'treat','Suppository':'suppository','Vaginal preparation':'pearl','Nasal spray':'nasal','Lollipop':'lollipop','Mouthwash':'mouthwash'}
  f0=(x['forms'] or ['Capsule'])[0]
  FIMG='/forms/'+(('suspension-pet' if pets_only else 'suspension') if f0=='Flavored oral suspension' else FM.get(f0,'capsule'))+'.svg'
  who=' and '.join('pets' if a=='pets' else 'people' for a in x['aud'])
  title=f"{base} Compounding in Oviedo, FL | Pharmacy on the Park"
  forms=', '.join(x['forms']) or 'custom forms'
  desc=f"{base}: {x['uses']} Compounded for {who} as {forms.lower()}. Pharmacy on the Park, Oviedo, FL. Call 407-977-9779."
  if len(desc)>300: desc=desc[:297].rsplit(' ',1)[0]+'...'
  pq=quote(base+(' AND (dogs OR cats)' if pets_only else '')); dq=quote(base)
  chips=lambda L:''.join(f'<span>{esc(v)}</span>' for v in L)
  body='<div class="page on" id="p-med">'+BODIES[x['id']]+'</div>\n\n'
  page=tmpl[:hs]+body+tmpl[he:]
  page=page.replace(LIBJSON,'null')
  u='/medications/'+x['id']+'/'; url=DOMAIN+u
  page=re.sub(r'<title>.*?</title>','<title>'+esc(title)+'</title>',page,1)
  page=re.sub(r'<meta name="description" content=".*?">','<meta name="description" content="'+esc(desc)+'">',page,1)
  page=re.sub(r'<meta property="og:title" content=".*?">','<meta property="og:title" content="'+esc(title)+'">',page,1)
  page=re.sub(r'<meta property="og:description" content=".*?">','<meta property="og:description" content="'+esc(desc)+'">',page,1)
  page=page.replace('<link rel="canonical" href="'+DOMAIN+'/medications/">','<link rel="canonical" href="'+url+'">').replace('<meta property="og:url" content="'+DOMAIN+'/medications/">','<meta property="og:url" content="'+url+'">')
  crumbs={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":DOMAIN+"/"},{"@type":"ListItem","position":2,"name":"Medication Library","item":DOMAIN+"/medications/"},{"@type":"ListItem","position":3,"name":nm,"item":url}]}
  page=re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "BreadcrumbList".*?</script>','<script type="application/ld+json">'+json.dumps(crumbs,ensure_ascii=False)+'</script>',page,1,flags=re.S)
  who2='veterinarian' if pets_only else 'prescriber'
  faq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in [(f"What is {base}?",x['how']),("What is it used for?",x['uses']),("What are the common side effects?",x['side']),("Who should use caution?",x['avoid']),("Are compounded medications FDA-approved?","No. Compounded medications are prepared for an individual patient from a prescription and are not FDA-approved."),("Do I need a prescription?",f"Yes. Your {who2} sends the prescription to Pharmacy on the Park.")]]}
  page=page.replace('</head>','<script type="application/ld+json">'+json.dumps(faq,ensure_ascii=False)+'</script>\n</head>',1)
  os.makedirs('_site'+u,exist_ok=True); open('_site'+u+'index.html','w').write(page); MEDURLS.append(u)
shutil.copytree('src/logos','_site/logos'); shutil.copytree('src/forms','_site/forms'); shutil.copytree('src/photos','_site/photos')
os.makedirs('_site/media',exist_ok=True); open('_site/media/README.txt','w').write('Retail page background video: save a short, silent, looping clip of your nonsterile compounding lab here as compounding-nonsterile.mp4 (MP4/H.264, 10-30 seconds, under 10 MB, 1920x1080). It plays softly behind the Retail Pharmacy banner. Until the file is here, the banner shows without video.\n')
os.makedirs('_site/downloads',exist_ok=True); shutil.copy('src/downloads/hrt-order-form.pdf','_site/downloads/hrt-order-form.pdf')
open('_site/robots.txt','w').write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
open('_site/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{DOMAIN}{u}</loc><lastmod>2026-10-01</lastmod><priority>{"1.0" if u in ("/","/low-dose-naltrexone/") else ("0.6" if u.count("/")>2 and u.startswith("/medications/") else "0.8")}</priority></url>\n' for u in list(URL.values())+MEDURLS)+'</urlset>\n')
print('built')
