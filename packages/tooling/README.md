# packages/tooling（Python，非 npm 包）

离线构建、Python 质检、`vendor` 等纯标准库工具的归属包。

## 当前状态（P1 已平移并参数化）

- tools/ 下脚本已 `git mv` 到 `packages/tooling/src/`，`tools/vendor`→`packages/tooling/vendor`，`tools/templates`→`packages/tooling/templates`。
- 脚本统一参数化 `--app/--src/--out/--vendor`，默认对 handbook 等价（`src=<repo>/docs`、`vendor=packages/tooling/vendor`、`app=handbook`）；仓库根 `python run_quality.py` 无需额外参数即可跑通。
- `build_single_html.py` 支持 `--manifest <content-manifest.json>`：文件存在则按其对账（章节数/id 序列/标题/图片引用数），缺失则维持自解析；不重写 Markdown（ARCHITECTURE §6）。

## 内容

- `src/build_single_html.py`：离线单文件构建（纯标准库、内联 vendor、零依赖）。
- `src/validate.py / scan_math.py / scan_grounds.py / scan_svg_order.py`（+ `fix_*`）：内容质检。
- `src/freeze_manifest.py`：P0 基线 manifest/快照生成（P1 后由 `@hw/content-core` 接管）。
- `src/build_vp_sidebar.py / fetch_vendor.py / merge_sources.py / _stats.py / test_net.py`：侧边栏/vendor 拉取/资料合并/统计/网络探测。
- `src/paths_util.py`：共享路径默认值（repo root 发现 + `add_common_args`）。
- `vendor/`：离线内联资源。

## 边界

- 这是 Python 包，**不是 npm 包**：不放 `package.json`，不参与 `pnpm install`。
- 运行方式：仓库根 `python run_quality.py`（门禁）；离线构建 `python packages/tooling/src/build_single_html.py`。
- 跨 app 最终集成（apps/handbook 落地后默认 src 切换）由 P2 主控统一，本包不做。
