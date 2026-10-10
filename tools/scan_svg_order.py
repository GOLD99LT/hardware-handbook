# -*- coding: utf-8 -*-
"""扫描原理图 SVG，检查是否有绘图元素被错误地写在根 <svg> 标签之前。
根标签外的图元浏览器不渲染，会出现"只有文字、没有电路"的空白图。
合法的 <?xml ...?> 声明不计为异常。"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SD = os.path.join(ROOT, 'docs', 'assets', 'schematics')

broken, ok = [], []
for fn in sorted(os.listdir(SD)):
    if not fn.endswith('.svg'):
        continue
    s = open(os.path.join(SD, fn), encoding='utf-8').read()
    m = re.search(r'<svg\b', s)
    if not m:
        broken.append((fn, 'NO <svg> root'))
        continue
    head = re.sub(r'<\?xml[^>]*\?>', '', s[:m.start()]).strip()
    if head:
        n = len(re.findall(r'<(?:line|rect|circle|text|path|g|polyline|polygon)\b', head))
        broken.append((fn, 'content-before-root, head_tags=%d, svg_at=%d/%d' % (n, m.start(), len(s))))
    else:
        ok.append(fn)

print('==== BROKEN (root <svg> not first): %d ====' % len(broken))
for fn, why in broken:
    print(' ', fn, '|', why)
print('==== OK (root first): %d ====' % len(ok))
