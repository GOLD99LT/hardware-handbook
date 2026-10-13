# packages/tooling（Python，非 npm 包）

离线构建、Python 质检、`tools/vendor` 等纯标准库工具的归属包。

## 当前状态（P1 骨架）

- **本阶段不搬迁任何文件**。现有脚本仍在仓库根的 `tools/` 目录（P0 位置），由 P2 起逐步 `git mv` 到这里并参数化（`--app/--src/--out/--vendor`，默认对 handbook 等价）。
- 本目录仅作为 Monorepo 蓝图中的包占位，说明归属。

## 规划中的内容（P2 及以后）

- `build_single_html.py`：离线单文件构建（纯标准库、内联 vendor、零依赖）。
- `validate.py / scan_math.py / scan_grounds.py / scan_svg_order.py`（+ `fix_*`）：内容质检。
- `vendor/`：离线内联资源。
- 迁移后这些脚本改为**只读** `.generated/content-manifest.json` 对账，不重写 Markdown（ARCHITECTURE §4/§6）。

## 边界

- 这是 Python 包，**不是 npm 包**：不放 `package.json`，不参与 `pnpm install`。
- 参数化完成前，运行方式与现状一致（仓库根 `run_quality.py`）。
