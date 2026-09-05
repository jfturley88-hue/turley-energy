import re, subprocess, os, builtins
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'ber_build_planner.html')).read()
blocks = re.findall(r'<script(?![^>]*type=["\']module)[^>]*>(.*?)</script>', src, re.S)
sp = os.path.dirname(os.path.abspath(__file__))
bad = 0
for i, b in enumerate(blocks):
    if not b.strip(): continue
    f = f'{sp}/_chk{i}.js'; open(f, 'w').write(b)
    r = subprocess.run(['/opt/node22/bin/node', '--check', f], capture_output=True, text=True)
    if r.returncode: bad += 1; print('SYNTAX FAIL block', i, r.stderr.strip().splitlines()[-1][:160])
    os.remove(f)
print(f'syntax: {len([b for b in blocks if b.strip()])} blocks, {bad} failed')
js = '\n'.join(blocks)
# strip comments and strings crudely so names inside them do not count
code = re.sub(r'/\*.*?\*/', ' ', js, flags=re.S)
code = re.sub(r'(^|[^:])//[^\n]*', r'\1', code)
code_nostr = re.sub(r"'(?:\\.|[^'\\\n])*'|\"(?:\\.|[^\"\\\n])*\"|`(?:\\.|[^`\\])*`", '""', code, flags=re.S)
defined = set(re.findall(r'\bfunction\s+([A-Za-z_$][\w$]*)\s*\(', code))
defined |= set(re.findall(r'\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=', code))
defined |= set(re.findall(r'\bwindow\.([A-Za-z_$][\w$]*)\s*=', code))
defined |= set(re.findall(r'^\s*([A-Za-z_$][\w$]*)\s*[:(]', code, re.M))   # object methods / labels
defined |= set(re.findall(r'\bfunction\s*\(([^)]*)\)', code))
# parameters of all functions (so calls to callback params are not flagged)
for params in re.findall(r'\(([^()]*)\)\s*(?:=>|\{)', code):
    for p in re.split(r'[,\s]+', params):
        p = p.strip('.= ').split('=')[0].strip()
        if re.match(r'^[A-Za-z_$][\w$]*$', p): defined.add(p)
called = set(re.findall(r'(?<![\w$.])([A-Za-z_$][\w$]*)\s*\(', code_nostr))
kw = set('if for while switch catch function return typeof new delete void throw in of instanceof await async yield class super this else do try with'.split())
globs = set(dir(builtins)) | set('''parseFloat parseInt isNaN isFinite Number String Boolean Array Object Math JSON Date RegExp Error Map Set Promise Symbol encodeURIComponent decodeURIComponent encodeURI decodeURI escape unescape alert confirm prompt setTimeout setInterval clearTimeout clearInterval requestAnimationFrame cancelAnimationFrame fetch Blob File FileReader URL Event CustomEvent MouseEvent KeyboardEvent Intl structuredClone queueMicrotask atob btoa Image Option XMLHttpRequest FormData Headers Request Response TextEncoder TextDecoder Uint8Array Int32Array Float64Array ArrayBuffer DataView WeakMap WeakSet Proxy Reflect BigInt Infinity NaN undefined require module exports console document window navigator location history localStorage sessionStorage getComputedStyle print open close focus blur scrollTo scrollBy'''.split())
missing = sorted(n for n in called - defined - kw - globs if not n[0].isupper() or n in called)
missing = [n for n in missing if not n[0].isupper()]
print('called but never defined (candidates):', len(missing))
for n in missing:
    m = re.search(r'\b' + re.escape(n) + r'\s*\(', code)
    line = code[:m.start()].count('\n') + 1 if m else '?'
    print(f'  {n:40s} first call near block-line {line}')
