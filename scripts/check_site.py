"""Check generated pages, internal links, fragments, and local resources."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

root = Path(__file__).resolve().parents[1] / '_site'
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.ids, self.images = [], set(), []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])
        if tag == 'img':
            self.images.append(attrs)

required = ['index.html', 'research.html', 'publications.html', 'cv.html', 'contact.html', '404.html']
errors = []
for name in required:
    if not (root / name).is_file():
        errors.append(f'Missing page: {name}')
pages = {f: Page(f.read_text()) for f in root.glob('*.html')}
for path, page in pages.items():
    for img in page.images:
        if 'alt' not in img:
            errors.append(f'{path.name}: image without alt text')
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = (root / unquote(url.path).lstrip('/')) if url.path.startswith('/') else path.parent / unquote(url.path)
        if not url.path:
            target = path
        if target.is_dir():
            target /= 'index.html'
        target = target.resolve()
        if not target.is_file():
            errors.append(f'{path.name}: missing target {link}')
        elif url.fragment and target.suffix == '.html':
            target_page = pages.get(target) or Page(target.read_text())
            if unquote(url.fragment) not in target_page.ids:
                errors.append(f'{path.name}: missing fragment {link}')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'Passed: {len(pages)} pages; local links, fragments, resources, and image alt text.')
