# -*- coding: utf-8 -*-
"""
paths_util.py — packages/tooling 共享路径默认值（纯 Python 标准库，零第三方依赖）。

按 ARCHITECTURE §4：脚本参数化 --app/--src/--out/--vendor，默认对 handbook 等价：
  - app    = 'handbook'
  - src    = <repo_root>/docs
  - vendor = <repo_root>/packages/tooling/vendor
未传参时默认值与重构前 tools/ 布局等价，保证 run_quality.py 无需额外参数即可跑通。
"""
import os
import argparse

# packages/tooling/src
HERE = os.path.dirname(os.path.abspath(__file__))
# packages/tooling
TOOLING_DIR = os.path.dirname(HERE)


def find_repo_root(start=None):
    """向上查找含 ARCHITECTURE.md 的目录作为仓库根（重构前 = 仓库根）。"""
    d = os.path.abspath(start or HERE)
    while True:
        if os.path.exists(os.path.join(d, 'ARCHITECTURE.md')):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return d
        d = parent


REPO_ROOT = find_repo_root()
DEFAULT_SRC = os.path.join(REPO_ROOT, 'docs')
DEFAULT_VENDOR = os.path.join(TOOLING_DIR, 'vendor')
DEFAULT_OUT_DIST = os.path.join(REPO_ROOT, 'dist')


def add_common_args(parser=None, out_default=None):
    """给 ArgumentParser 追加 --app/--src/--out/--vendor 四个通用参数。"""
    p = parser or argparse.ArgumentParser()
    p.add_argument('--app', default='handbook',
                   help='应用 id（默认 handbook）')
    p.add_argument('--src', default=DEFAULT_SRC,
                   help='内容源目录（默认 <repo>/docs）')
    p.add_argument('--out', default=out_default,
                   help='输出目录/文件（默认见各脚本）')
    p.add_argument('--vendor', default=DEFAULT_VENDOR,
                   help='vendor 资源目录（默认 packages/tooling/vendor）')
    return p
