# -*- coding: utf-8 -*-
"""修复公式中的 Unicode 符号（只在 $...$ / $$...$$ 内部，不动正文）：
- Ω(U+03A9/U+2126) -> \\Omega；µ(U+00B5/U+03BC) -> \\mu；° -> ^{\\circ}
- \\text{...} 内的这些符号：先闭合 text、插入数学命令、再重开 text。
修改前备份到 _backup/math-fix/。参数化：--src 指定内容源（默认 <repo>/docs）。
"""
import os, re, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths_util import REPO_ROOT, add_common_args
_args, _ = add_common_args().parse_known_args()
DOCS = os.path.abspath(_args.src)
BACKUP = os.path.join(REPO_ROOT, '_backup', 'math-fix')

# text 内遇到这些字符的替换（数学命令）
TEXT_BAD = {'Ω': '\\Omega', '\u2126': '\\Omega', '\u00b5': '\\mu',
            '\u03bc': '\\mu', '°': '^{\\circ}', '≈': '\\approx'}
# text 外（数学区）的直接替换
MATH_BAD = {'Ω': '\\Omega', '\u2126': '\\Omega', '\u00b5': '\\mu',
            '\u03bc': '\\mu', '°': '^{\\circ}', '≈': '\\approx'}
CJK_RE = re.compile(r'[\u4e00-\u9fff]')

def fix_text(m):
    content = m.group(1)
    if not any(c in content for c in TEXT_BAD):
        return m.group(0)
    out, buf = [], ''
    for ch in content:
        if ch in TEXT_BAD:
            if buf:
                out.append('\\text{%s}' % buf); buf = ''
            out.append(TEXT_BAD[ch])
        else:
            buf += ch
    if buf:
        out.append('\\text{%s}' % buf)
    return ''.join(out)

def fix_tex(tex):
    # 1. text 内
    tex = re.sub(r'\\text\{([^}]*)\}', fix_text, tex)
    # 2. 下标/上标花括号内的裸中文：_{总} -> _{\text{总}}
    def sub_cjk(m):
        pre, content = m.group(1), m.group(2)
        if '\\text' in content or not CJK_RE.search(content):
            return m.group(0)
        return '%s{\\text{%s}}' % (pre, content)
    tex = re.sub(r'([_^])\{([^}]*)\}', sub_cjk, tex)
    # 3. 单字符下标/上标中文：_总 -> _\text{总}
    tex = re.sub(r'([_^])([\u4e00-\u9fff])',
                 lambda m: '%s\\text{%s}' % (m.group(1), m.group(2)), tex)
    # 4. text 外（数学区）符号
    for k, v in MATH_BAD.items():
        tex = tex.replace(k, v)
    return tex

def transform(text):
    # 块公式
    text = re.sub(r'\$\$(.+?)\$\$',
                  lambda m: '$$' + fix_tex(m.group(1)) + '$$', text, flags=re.S)
    # 行内公式（排除 $$）
    text = re.sub(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$',
                  lambda m: '$' + fix_tex(m.group(1)) + '$', text, flags=re.S)
    return text

changed = 0
for part in sorted(os.listdir(DOCS)):
    pd = os.path.join(DOCS, part)
    if not os.path.isdir(pd) or part == 'assets':
        continue
    for f in sorted(os.listdir(pd)):
        if not f.endswith('.md'):
            continue
        fp = os.path.join(pd, f)
        orig = open(fp, encoding='utf-8').read()
        new = transform(orig)
        if new != orig:
            bdir = os.path.join(BACKUP, part)
            os.makedirs(bdir, exist_ok=True)
            shutil.copyfile(fp, os.path.join(bdir, f))
            open(fp, 'w', encoding='utf-8').write(new)
            changed += 1
            print('fixed  %s/%s' % (part, f))

print('==== 共修正 %d 个文件（备份在 _backup/math-fix）====' % changed)
