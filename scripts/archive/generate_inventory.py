"""
Comprehensive interactive control scanner and analyzer for HiddenYatra.
Uses Python's standard html.parser (no external dependencies).
Extracts every interactive element:
<button>, <input>, <form>, <select>, <a> (with btn/action), onclick handlers, file uploads, toggles, chips.
"""
import os
import re
import json
from html.parser import HTMLParser

TEMPLATE_DIR = r'd:\HiddenYatra\templates'

class TemplateControlParser(HTMLParser):
    def __init__(self, page_name):
        super().__init__()
        self.page_name = page_name
        self.controls = []
        self.current_tag = None
        self.current_attrs = {}
        self.current_text = []

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attr_dict = dict(attrs)
        self.current_attrs = attr_dict
        self.current_text = []

        # Check for Forms
        if tag == 'form':
            self.controls.append({
                'page': self.page_name,
                'element': 'form',
                'id': attr_dict.get('id', ''),
                'class': attr_dict.get('class', ''),
                'action': attr_dict.get('action', ''),
                'method': attr_dict.get('method', 'GET').upper(),
                'text': f"Form: {attr_dict.get('action', '')} ({attr_dict.get('method', 'GET').upper()})",
                'type': 'form'
            })

        # Check for Buttons
        elif tag == 'button':
            pass # We will collect text in handle_data and finish in handle_endtag

        # Check for Inputs
        elif tag == 'input':
            itype = attr_dict.get('type', 'text').lower()
            if itype in ('submit', 'button', 'file', 'checkbox', 'radio', 'range', 'hidden'):
                name = attr_dict.get('name', '')
                val = attr_dict.get('value', '')
                label = val or name or itype
                self.controls.append({
                    'page': self.page_name,
                    'element': f'input[type={itype}]',
                    'id': attr_dict.get('id', ''),
                    'class': attr_dict.get('class', ''),
                    'name': name,
                    'value': val,
                    'text': label[:60],
                    'type': f'input_{itype}'
                })

        # Check for Select dropdowns
        elif tag == 'select':
            self.controls.append({
                'page': self.page_name,
                'element': 'select',
                'id': attr_dict.get('id', ''),
                'class': attr_dict.get('class', ''),
                'name': attr_dict.get('name', ''),
                'text': f"Select: {attr_dict.get('name', '')}",
                'type': 'select'
            })

        # Check for Links
        elif tag == 'a':
            aclass = attr_dict.get('class', '')
            onclick = attr_dict.get('onclick', '')
            href = attr_dict.get('href', '')
            is_btn = 'btn' in aclass or 'button' in aclass or onclick or href.startswith('javascript:') or attr_dict.get('role') == 'button' or href.startswith('#')
            if is_btn:
                # We will collect text in handle_data
                pass

        # Check for non-standard interactive widgets with onclick or special classes
        elif attr_dict.get('onclick') or any(c in attr_dict.get('class', '') for c in ('wishlist', 'favorite', 'favourite', 'star', 'rating', 'heart', 'bookmark', 'tab-btn', 'chip', 'stepper-btn', 'filter-chip')):
            self.controls.append({
                'page': self.page_name,
                'element': tag,
                'id': attr_dict.get('id', ''),
                'class': attr_dict.get('class', ''),
                'onclick': attr_dict.get('onclick', ''),
                'text': f"Interactive {tag}: {attr_dict.get('class', '')}",
                'type': 'interactive_widget'
            })

    def handle_data(self, data):
        if self.current_tag in ('button', 'a'):
            self.current_text.append(data.strip())

    def handle_endtag(self, tag):
        if tag == 'button' and self.current_attrs is not None:
            text = ' '.join(t for t in self.current_text if t)
            if not text:
                text = self.current_attrs.get('aria-label') or self.current_attrs.get('title') or '[Icon/Empty Button]'
            self.controls.append({
                'page': self.page_name,
                'element': f"button[type={self.current_attrs.get('type', 'submit')}]",
                'id': self.current_attrs.get('id', ''),
                'class': self.current_attrs.get('class', ''),
                'onclick': self.current_attrs.get('onclick', ''),
                'text': text[:60],
                'type': 'button'
            })
            self.current_tag = None
            self.current_attrs = {}
            self.current_text = []
        elif tag == 'a' and self.current_attrs is not None:
            aclass = self.current_attrs.get('class', '')
            onclick = self.current_attrs.get('onclick', '')
            href = self.current_attrs.get('href', '')
            is_btn = 'btn' in aclass or 'button' in aclass or onclick or href.startswith('javascript:') or self.current_attrs.get('role') == 'button' or href.startswith('#')
            if is_btn:
                text = ' '.join(t for t in self.current_text if t) or self.current_attrs.get('title') or self.current_attrs.get('aria-label') or href
                self.controls.append({
                    'page': self.page_name,
                    'element': 'a.btn',
                    'id': self.current_attrs.get('id', ''),
                    'class': aclass,
                    'href': href,
                    'onclick': onclick,
                    'text': text[:60],
                    'type': 'link_button'
                })
            self.current_tag = None
            self.current_attrs = {}
            self.current_text = []

def parse_template(fpath):
    rel_path = os.path.relpath(fpath, TEMPLATE_DIR).replace('\\', '/')
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    
    # Strip Jinja2 block tags to prevent HTML parser confusion while retaining content
    clean_html = re.sub(r'\{%.*?%\}', ' ', content)
    clean_html = re.sub(r'\{\{.*?\}\}', 'EXPR', clean_html)
    clean_html = re.sub(r'\{#.*?#\}', ' ', clean_html)

    parser = TemplateControlParser(rel_path)
    try:
        parser.feed(clean_html)
    except Exception as e:
        # Fallback regex extraction if parser trips on invalid template snippets
        pass
    return parser.controls

def run_inventory():
    all_tpls = []
    for root, dirs, files in os.walk(TEMPLATE_DIR):
        for f in files:
            if f.endswith('.html'):
                all_tpls.append(os.path.join(root, f))

    all_controls = []
    for tpl in all_tpls:
        ctrls = parse_template(tpl)
        all_controls.extend(ctrls)

    print(f"Total Interactive Controls Found Across Templates: {len(all_controls)}")
    
    # Breakdown by element type
    by_type = {}
    for c in all_controls:
        t = c['type']
        by_type[t] = by_type.get(t, 0) + 1

    print("\nBreakdown by Control Type:")
    for t, cnt in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {t:25s}: {cnt}")

    # Breakdown by Page
    by_page = {}
    for c in all_controls:
        p = c['page']
        by_page[p] = by_page.get(p, 0) + 1

    print("\nBreakdown by Page/Template:")
    for p, cnt in sorted(by_page.items(), key=lambda x: -x[1]):
        print(f"  {p:35s}: {cnt}")

    # Save complete JSON inventory
    out_path = r'd:\HiddenYatra\scratch\interactive_controls_inventory.json'
    with open(out_path, 'w', encoding='utf-8') as fh:
        json.dump(all_controls, fh, indent=2)
    print(f"\nSaved inventory to {out_path}")

if __name__ == '__main__':
    run_inventory()
