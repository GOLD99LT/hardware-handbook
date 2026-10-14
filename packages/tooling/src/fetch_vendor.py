# -*- coding: utf-8 -*-
"""下载前端依赖（KaTeX / ECharts）到 packages/tooling/vendor，构建时内联，保证离线自包含。
当前网络环境 unpkg 可达；每个文件带重试。vendor 目录提交进 git，clone 后无需联网即可构建。
参数化：--vendor 可覆盖 vendor 目录（默认 packages/tooling/vendor）。
"""
import urllib.request, os, time, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths_util import add_common_args
_args, _ = add_common_args().parse_known_args()

BASE = 'https://unpkg.com/'
VENDOR = os.path.abspath(_args.vendor)
FONT_DIR = os.path.join(VENDOR, 'fonts')
os.makedirs(FONT_DIR, exist_ok=True)

KATEX = 'katex@0.16.11/dist/'
ECHARTS = 'echarts@5.5.1/dist/'

FILES = [
    (ECHARTS + 'echarts.min.js', 'echarts.min.js'),
    (KATEX + 'katex.min.js', 'katex.min.js'),
    (KATEX + 'katex.min.css', 'katex.min.css'),
]
FONTS = [
    'KaTeX_AMS-Regular', 'KaTeX_Caligraphic-Bold', 'KaTeX_Caligraphic-Regular',
    'KaTeX_Fraktur-Bold', 'KaTeX_Fraktur-Regular', 'KaTeX_Main-Bold',
    'KaTeX_Main-BoldItalic', 'KaTeX_Main-Italic', 'KaTeX_Main-Regular',
    'KaTeX_Math-BoldItalic', 'KaTeX_Math-Italic', 'KaTeX_SansSerif-Bold',
    'KaTeX_SansSerif-Italic', 'KaTeX_SansSerif-Regular', 'KaTeX_Script-Regular',
    'KaTeX_Size1-Regular', 'KaTeX_Size2-Regular', 'KaTeX_Size3-Regular',
    'KaTeX_Size4-Regular', 'KaTeX_Typewriter-Regular',
]

def fetch(url, dest, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req, timeout=30).read()
            open(dest, 'wb').write(data)
            print('OK  %s  (%d KB)' % (os.path.basename(dest), len(data)//1024))
            return True
        except Exception as e:
            print('  retry %d/%d %s (%s)' % (i+1, tries, os.path.basename(dest), type(e).__name__))
            time.sleep(2)
    print('FAIL  %s' % url)
    return False

ok = True
for src, name in FILES:
    ok = fetch(BASE + src, os.path.join(VENDOR, name)) and ok
for f in FONTS:
    ok = fetch(BASE + KATEX + 'fonts/' + f + '.woff2',
               os.path.join(FONT_DIR, f + '.woff2')) and ok

print('全部完成' if ok else '存在失败项，请重跑本脚本')
sys.exit(0 if ok else 1)
