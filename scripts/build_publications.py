# Regenerate the single publications page and BibTeX from publications.json.
from pathlib import Path
import json, html
root=Path(__file__).resolve().parents[1]
rows=json.loads((root/'publications.json').read_text())
out=['---\ntitle: Publications\n---\n',
     '[Google Scholar](https://scholar.google.com/citations?user=n778aCsAAAAJ&hl=en)\n',
     '<p class="publication-key"><sup>&#42;</sup> Indicates a primary author, in addition to the first-listed author.</p>\n',
     '<nav class="publication-years" aria-label="Publication years">'+''.join(f'<a href="#year-{y}">{y}</a>' for y in sorted({r['year'] for r in rows},reverse=True))+'</nav>\n']
bib=[]
current=None
for r in rows:
 if r['year']!=current:
  current=r['year'];out.append(f'## {current} {{#year-{current}}}\n')
 ext='svg' if r.get('schematic') else 'webp'
 image=f"assets/publications/{r['id']}.{ext}"
 authors=[]
 for i,name in enumerate(r['authors']):
  name=html.escape(name)
  if 'Nerem' in name:name=f'<strong>{name}</strong>'
  if i in r.get('equal',[]):name+='<sup>&#42;</sup>'
  authors.append(name)
 links=[f'<a href="{html.escape(r["url"],quote=True)}">'+('Record' if r['id']=='thesis' else 'Paper')+'</a>']
 if r.get('pdf'):links.append(f'<a href="{html.escape(r["pdf"],quote=True)}">PDF</a>')
 if r.get('arxiv'):links.append(f'<a href="{r["arxiv"]}">arXiv</a>')
 badges=' '.join('<span class="publication-badge">'+html.escape(label)+'</span>' for label in r.get('recognition',[]))
 figure_url=r.get('pdf',r['url'])+(f'#page={r["page"]}' if r.get('page') else '')
 out.append(f'''<article class="publication" id="{r['id']}">
<figure class="publication-figure">
<a href="{html.escape(figure_url,quote=True)}" aria-label="View {html.escape(r['title'],quote=True)}"><img src="{image}" alt="{html.escape(r['alt'],quote=True)}" width="600" height="360" loading="lazy"></a>
<figcaption>{html.escape(r['figure'])}</figcaption>
</figure>
<div class="publication-body">
<h3><a href="{html.escape(r['url'],quote=True)}">{html.escape(r['title'])}</a></h3>
<p class="publication-authors">{', '.join(authors)}.</p>
<p class="publication-venue">{html.escape(r['venue'])} {badges}</p>
<div class="publication-links">{' '.join(links)}</div>
</div></article>\n''')
 def esc(s):return s.replace('&',r'\&').replace('%',r'\%').replace('–','--')
 authors_bib=[]
 for a in r['authors']:
  first,last=a.rsplit(' ',1);authors_bib.append(last+', '+first)
 fields={'title':'{'+esc(r['title'])+'}','author':' and '.join(authors_bib),'year':str(r['year']),'url':r['url']}
 if r['bibtype']=='mastersthesis':fields['school']='University of Calgary'
 else:fields['journal' if r['bibtype']=='article' else 'booktitle' if r['bibtype']=='inproceedings' else 'note']=esc(r['venue'])
 if r.get('doi'):fields['doi']=r['doi']
 if r.get('equal'):fields['note']='Additional primary-author designation: '+', '.join(r['authors'][i] for i in r['equal'])
 bib.append('@'+r['bibtype']+'{nerem'+str(r['year'])+r['id']+',\n'+',\n'.join('  '+k+' = {'+v+'}' for k,v in fields.items())+'\n}\n')
(root/'publications.qmd').write_text('\n'.join(out))
(root/'papers.bib').write_text('\n'.join(bib))
print(f'Generated {len(rows)} publication entries and citations.')
