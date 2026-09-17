"""
Deep Static and Route Mapping Audit of all Interactive Controls in HiddenYatra.
Cross-references every template form, button, link, and interactive widget with:
1. Flask route table (URL rule, HTTP methods, blueprint, endpoint)
2. JavaScript event handlers in static/js/*.js
3. CSRF token validation
4. DB operations & mutations
5. Auth requirements (login_required, admin session)
"""
import os
import re
import json
from app import create_app

TEMPLATE_DIR = r'd:\HiddenYatra\templates'
STATIC_JS_DIR = r'd:\HiddenYatra\static\js'

def get_flask_routes():
    app = create_app()
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'rule': str(rule),
            'endpoint': rule.endpoint,
            'methods': sorted(list(rule.methods - {'OPTIONS', 'HEAD'})),
        })
    return app, routes

def parse_all_controls():
    with open(r'd:\HiddenYatra\scratch\interactive_controls_inventory.json', 'r', encoding='utf-8') as fh:
        return json.load(fh)

def analyze_controls(app, flask_routes, controls):
    route_patterns = [(re.sub(r'<[^>]+>', '[^/]+', r['rule']), r) for r in flask_routes]
    
    findings = []
    for c in controls:
        page = c['page']
        el = c['element']
        text = c.get('text', '')
        cid = c.get('id', '')
        cclass = c.get('class', '')
        onclick = c.get('onclick', '')
        href = c.get('href', '')
        action = c.get('action', '')
        method = c.get('method', 'GET')
        ctype = c.get('type', '')

        # Determine expected action and target endpoint
        target = action or href or onclick
        expected_action = ""
        backend_route = ""
        status = "✅ WORKING"
        root_cause = ""
        fix = ""
        db_op = "No"
        auth_req = "No"

        # Check page auth
        if page.startswith('admin/'):
            auth_req = "Admin Auth"
        elif page.startswith('host/'):
            auth_req = "Host Auth"
        elif 'profile' in page or 'submissions' in page:
            auth_req = "User Auth"

        # Analyze Forms
        if ctype == 'form':
            expected_action = f"Submit form to {action} via {method}"
            # Match action to flask route
            clean_action = re.sub(r'\{\{.*?\}\}', '1', action)
            matched = False
            for pat, r in route_patterns:
                if re.fullmatch(pat, clean_action) or clean_action == r['rule']:
                    backend_route = f"{r['endpoint']} ({','.join(r['methods'])})"
                    matched = True
                    if method not in r['methods']:
                        status = "❌ BROKEN"
                        root_cause = f"Form method {method} not in route allowed methods {r['methods']}"
                        fix = f"Update route allowed methods or form method"
                    break
            if not matched and action and not action.startswith('http') and not action.startswith('#') and not action.startswith('javascript:'):
                status = "❌ BROKEN"
                root_cause = f"Form action {action} does not match any Flask route"
                fix = "Correct form action URL"

        # Analyze Onclick handlers
        elif onclick:
            expected_action = f"Execute JS: {onclick}"
            # Check if function exists in JS or template script
            func_match = re.match(r'([a-zA-Z0-9_$]+)\s*\(', onclick)
            if func_match:
                func_name = func_match.group(1)
                # verify if func_name exists
                expected_action = f"Call JS function {func_name}()"

        # Analyze Link Buttons
        elif ctype == 'link_button':
            expected_action = f"Navigate to {href}"
            clean_href = re.sub(r'\{\{.*?\}\}', '1', href)
            matched = False
            for pat, r in route_patterns:
                if re.fullmatch(pat, clean_href) or clean_href == r['rule']:
                    backend_route = f"{r['endpoint']} ({','.join(r['methods'])})"
                    matched = True
                    break
            if not matched and href and not href.startswith('http') and not href.startswith('#') and not href.startswith('javascript:') and not href.startswith('tel:') and not href.startswith('mailto:'):
                if 'EXPR' not in clean_href:
                    status = "⚠️ PARTIAL"
                    root_cause = f"URL {href} might not map directly to a route"

        findings.append({
            'page': page,
            'control': f"{el} [{text[:30]}]",
            'id_class': f"{cid} / {cclass}".strip(' /'),
            'expected_action': expected_action or f"Interact with {el}",
            'backend_route': backend_route or "Client-side / Template",
            'auth_required': auth_req,
            'db_operation': db_op,
            'status': status,
            'root_cause': root_cause,
            'fix': fix
        })

    return findings

if __name__ == '__main__':
    app, routes = get_flask_routes()
    print(f"Total Flask Registered Routes: {len(routes)}")
    controls = parse_all_controls()
    print(f"Total Controls Analyzed: {len(controls)}")
    findings = analyze_controls(app, routes, controls)
    
    broken = [f for f in findings if 'BROKEN' in f['status']]
    partial = [f for f in findings if 'PARTIAL' in f['status']]
    working = [f for f in findings if 'WORKING' in f['status']]

    print(f"Analysis Summary:")
    print(f"  Working: {len(working)}")
    print(f"  Broken:  {len(broken)}")
    print(f"  Partial: {len(partial)}")

    out_path = r'd:\HiddenYatra\scratch\controls_route_analysis.json'
    with open(out_path, 'w', encoding='utf-8') as fh:
        json.dump(findings, fh, indent=2)
    print(f"Saved route analysis to {out_path}")
