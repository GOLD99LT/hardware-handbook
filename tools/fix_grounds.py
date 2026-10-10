# -*- coding: utf-8 -*-
"""把所有原理图的接地符号三线统一为标准比例：
长度 28/18/10（半长 14/9/5）、间距 7、stroke-width 2.4，竖线接入点不变。
备份到 _backup/grounds-fix/。"""
import os, re, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SDIR = os.path.join(ROOT, 'docs', 'assets', 'schematics')
BACKUP = os.path.join(ROOT, '_backup', 'grounds-fix')

LINE_RE = re.compile(r'<line\b[^>]*?/>')
ATTR = re.compile(r'(x1|y1|x2|y2)="([\d.]+)"')

def parse_line(tag):
    return {k: float(v) for k, v in ATTR.findall(tag)}

def newtag(cx, half, y):
    return ('<line x1="%g" y1="%g" x2="%g" y2="%g" '
            'stroke="#2b3a4a" stroke-width="2.4"/>' % (cx-half, y, cx+half, y))

def fix_svg(svg):
    h = []
    for m in LINE_RE.finditer(svg):
        d = parse_line(m.group(0))
        if abs(d['y1'] - d['y2']) < 0.1:
            cx = (d['x1'] + d['x2']) / 2
            h.append((m.group(0), cx, d['y1'], abs(d['x2'] - d['x1'])))
    h.sort(key=lambda t: (round(t[1]/4), t[2]))
    repl, n = {}, len(h)
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                t1, t2, t3 = h[i], h[j], h[k]
                if abs(t1[1]-t2[1]) <= 3 and abs(t2[1]-t3[1]) <= 3:
                    d12, d23 = t2[2]-t1[2], t3[2]-t2[2]
                    if (3 <= d12 <= 14 and 3 <= d23 <= 14 and abs(d12-d23) <= 5
                            and t1[3] > t2[3] > t3[3] and 12 <= t1[3] <= 50):
                        if t1[0] in repl or t2[0] in repl or t3[0] in repl:
                            continue
                        cx, topY = t1[1], t1[2]
                        repl[t1[0]] = newtag(cx, 14, topY)
                        repl[t2[0]] = newtag(cx, 9, topY+7)
                        repl[t3[0]] = newtag(cx, 5, topY+14)
    for old, new in repl.items():
        svg = svg.replace(old, new, 1)
    return svg, len(repl) // 3

total_files, total_g = 0, 0
os.makedirs(BACKUP, exist_ok=True)
for f in sorted(os.listdir(SDIR)):
    if not f.endswith('.svg'):
        continue
    fp = os.path.join(SDIR, f)
    orig = open(fp, encoding='utf-8').read()
    new, cnt = fix_svg(orig)
    if cnt:
        shutil.copyfile(fp, os.path.join(BACKUP, f))
        open(fp, 'w', encoding='utf-8').write(new)
        total_files += 1
        total_g += cnt
        print('fixed %-40s %d 个接地' % (f, cnt))
print('==== 修正 %d 个文件、%d 个接地符号 ====' % (total_files, total_g))
