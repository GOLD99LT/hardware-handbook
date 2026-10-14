# PLAYBOOK · hardware-handbook 操作手册（随代码更新）

> 本文是「当前怎么把这套东西跑起来、改对、验过」的手册，遇到坑就追加到第 11 节。
> 架构原则见 [`../ARCHITECTURE.md`](../ARCHITECTURE.md)，协作规则见 [`../CONTRIBUTING.md`](../CONTRIBUTING.md)、[`../AGENTS.md`](../AGENTS.md)，决策见 [`adr/`](adr/)。

## 1. 环境与工具链

| 工具 | 版本 | 说明 |
|---|---|---|
| Node | 22.x（本机 22.23.2） | 随产品内置，非系统安装 |
| pnpm | 12.11.2 | 用 corepack 启用；`packageManager` 已锁定 |
| Python | 3.11+（本机 3.13.13） | 核心脚本**仅标准库**；`merge_sources.py` 可选 PyYAML |
| Git | 2.x | 跨平台行尾由 `.gitattributes` 统一 |

启用 pnpm（corepack，首选）：

```bash
corepack enable
corepack prepare pnpm@latest --activate
pnpm -v        # 期望 12.x
```

> Windows 每个新 PowerShell 会话若 `git` 不在 PATH，先：`$env:Path += ';C:\Program Files\Git\cmd'`。
> 镜像源在 `.npmrc`（npmmirror）；**审计**镜像无 audit 端点，需 `npm audit --registry=https://registry.npmjs.org/`。

## 2. 仓库布局

```
apps/handbook/            # 手册 app（内容在 docs/）
  docs/                   # 140 章 md + assets/411 SVG + SUMMARY + index（唯一事实源）
  docs/.vitepress/config.mts     # 薄配置：defineHwConfig(...)
  docs/.vitepress/theme/index.ts # createHwTheme({catalog, repository})
  content.config.ts       # appId/标题/篇名 registry/nav/social + 学习仓储装配
packages/
  shared-config/          # @hw/shared-config：通用 markdown/搜索/插件工厂
  theme/                  # @hw/theme：布局/品牌/学习 UI/EChart/图片查看器（含 public 品牌资产）
  content-core/           # @hw/content-core：manifest 生成（TS），CLI 出 manifest + catalog 模块
  learning/               # @hw/learning：LearningRepository + 单测
  components/ svg-kit/    # 占位（P5）
  tooling/                # Python（非 npm 包）：src 脚本、vendor、templates
templates/site-template/  # 新专项脚手架（空 app 可构建）
tests/                    # routes.snapshot.json / manifest.snapshot.json（入库基准）
.generated/               # 生成物（manifest，不入库）
dist/                     # 离线单文件（不入库）
run_quality.py            # 统一质量门禁（仓库根）
.github/workflows/        # quality.yml（门禁）、deploy-docs.yml、deploy-cloudflare.yml
```

## 3. 日常开发

```bash
pnpm install                          # 首次或拉取后
pnpm --filter @hw/handbook docs:dev   # 开发（predev 自动 gen sidebar/catalog）
pnpm --filter @hw/handbook docs:build
pnpm --filter @hw/handbook docs:preview
```

`predev/prebuild` 会自动执行 `gen`：

- `gen:sidebar`：`python packages/tooling/src/build_vp_sidebar.py --src docs` → `docs/.vitepress/sidebar.generated.mjs`，并把品牌资产从 `packages/theme/public` 同步到 `docs/public`。
- `gen:catalog`：`node packages/content-core/src/cli.ts --src docs --out .generated/... --catalogOut docs/.vitepress/catalog.generated.mjs`。

> 这两个 `.generated.mjs` 与 `docs/public/` 都是生成物（已 gitignore），**不要手改、不要提交**。

## 4. 增改内容

1. 在 `apps/handbook/docs/<篇>/` 新建/改 md；图放 `docs/assets/schematics/`。
2. 在 `apps/handbook/docs/SUMMARY.md` 对应 `## 篇名` 下加一行 `* [标题](path.md)`。
3. frontmatter：`title/part/chapter/order/tags/difficulty`。`id` 即相对路径，**不写**。
4. 重新 `docs:dev` 或 build，sidebar/catalog 会自动重生。
5. 若新增/重命名/删除文件导致快照变化，见第 7 节（破坏性变更须 ADR）。

## 5. 双形态构建

在线：

```bash
pnpm --filter @hw/handbook docs:build   # 产物 apps/handbook/docs/.vitepress/dist
```

离线单文件（自包含、零网络）：

```bash
python packages/tooling/src/freeze_manifest.py
python packages/tooling/src/build_single_html.py --manifest .generated/content-manifest.json
# 产物 dist/hardware-handbook.html；末尾打印「对账一致：N 章 / M 处图片 / revision=…」
```

也可直接 `pnpm offline`（串联上面两步）。`--manifest` 会按章节数 / id / 标题 / 图片引用数 / revision 对账，不一致 `[MISMATCH]` 且非零退出。

## 6. 质量门禁

```bash
python run_quality.py        # 或 pnpm quality
```

聚合 5 步：① manifest 一致性 + 路由/指纹快照比对 ② validate ③ scan_grounds ④ scan_svg_order ⑤ scan_math。

基线冻结值：docCount **140**、imageTotal **418**、svg **411**、grounds **247**、routes **141**、revision `sha256-4c8521761e575941`、overallChecksum `4c852176…b9306`。

- `validate` 唯一已知告警是 `index.md` 孤儿（首页不进 SUMMARY，已豁免）。
- 一键全验：`pnpm verify`（在线构建 + 空 app 构建 + learning 单测 + quality + 离线）。
- learning 单测：`node packages/learning/test/learning.test.ts`（应 40 passed）。

## 7. 内容迁移 / 路由快照（强约束）

- 内容只允许 `git mv`；完成后必须 `routes.snapshot.json` 与 `manifest.snapshot.json` **零差异**。
- 重新生成快照只在「确有意变更」时做，且必须逐条列出差异；URL 变更属破坏性，须先写 ADR（见 [ADR-0002](adr/ADR-0002.md)）。
- 章节 id = 相对路径；学习数据按 id 存储，改文件名等于新章（旧记录进 tombstone）。

## 8. 学习数据（浏览器 localStorage）

- 键：`hb.v1.<appId>.learning`（handbook 为 `hb.v1.handbook.learning`）；旧键 `hh.v1.learning` 首次访问时迁移并**保留**。
- 笔记形态 `{text, updatedAt}`；导出含 `contentRevision/exportedAt`；导入支持 `merge/replace`，未知章进 `tombstones`（不落库不计分）。
- 每个 app 必须在 `content.config.ts` 启动时 `catalog.entries.forEach(e => repository.getChapter(e.id))` 注册全量已知章。
- 浏览器实测迁移可用 playwright 注入旧键后加载页面，断言「新键写入 / 旧键保留 / 字段迁移 / 0 console 错误」。

## 9. 新增一个专项 app

```bash
cp -r templates/site-template apps/<app>
# 改：
#   apps/<app>/content.config.ts  → APP_ID / TITLE / 篇名 PART_REGISTRY / NAV
#   apps/<app>/package.json       → gen:catalog 的 --appId、包名
#   apps/<app>/docs/.vitepress/config.mts → base（默认 '/', 子路径用 VP_BASE='/<app>/'）
#   docs/SUMMARY.md（用 ## 篇名分组）+ 写 md
pnpm install
pnpm --filter @hw/<app> docs:build
```

先做 3–5 章验证：schema、本地搜索、学习数据按 appId 隔离、离线包。**注意**：SUMMARY 必须有 `## 篇名` 分组（否则生成器收集到 0 章会退出）；正文里出现 `<app>` 这类裸尖括号要写进行内代码或转义，否则被 Vue 当成未闭合标签。

## 10. CI 与部署

- `quality.yml`：push/PR 跑 frozen 安装 → 在线构建 → 空 app 构建 → learning 单测 → run_quality → freeze → 离线对账。**不部署**。
- `deploy-docs.yml`：推 `main` 发 GitHub Pages，base `/hardware-handbook/`。
- `deploy-cloudflare.yml`：手动（或配置后随 main），构建时 `VP_BASE=/` 发根路径镜像。
- 本地必须能复现 CI 命令；**分支未 push 前 GitHub Actions 不会运行**，本地 `pnpm verify` 全绿即视为已就绪，待用户授权再 push 触发。

## 11. 截图自检（shot.py）

- 自检脚本 `python <skill>/scripts/shot.py <url|html>`（playwright；桌面 1440×900、移动 390×844 全页 + 控制台/资源/溢出/emoji 检查）。
- 对 VitePress 预览站：先 `pnpm --filter @hw/handbook docs:build`，再 `docs:preview`（默认 4173，base `/hardware-handbook/`），用 http 地址喂给 shot。
- **运行方式**：长任务用后台运行；命令后**不要接管道/重定向**；一次只跑一个，避免死锁。
- 重建 dist 后**重启 preview**（旧目录句柄会导致假 404 / 假未水合）。

### 已知豁免（不要为这些反复改/复测）

- `aside.VPSidebar` 在移动 390 视口报「离屏/横向溢出」：VitePress 抽屉式侧栏默认 `translateX` 藏在视口外，是正常行为，属对 fixed/transform 的误报。
- `faviconWarning` 引用外部 `/favicon.svg`：多页 VitePress 的正确写法，无需内联 data URI。
- emoji 检查命中 `U+2713 ✓`、`U+2192 →`、`U+2605 ★` 等 **dingbat**：是符号非 emoji，规则豁免；内容只 git mv，不为此改正文。
- `stretchedImages` 命中带 `padding` 的图：核对内容区宽高比（把边框盒里的 padding 扣掉），若比例与 SVG `viewBox` 一致则为 padding 计入盒模型的误报，图未变形。
- 宽块/行内 KaTeX 在窄屏：主题已让其在容器内横向滚动（`html,body overflow-x:clip`，页面级无横滚条）。

## 12. 故障与踩坑（持续追加）

1. **pnpm 安装报 `ERR_PNPM_IGNORED_BUILDS`（esbuild）**：pnpm 12 已移除 `onlyBuiltDependencies`，改在 `pnpm-workspace.yaml` 写 `allowBuilds: { esbuild: true }`。`pnpm approve-builds` 是交互式，非交互 shell 会挂起，别用。
2. **pnpm 不读 package.json 的 `pnpm` 字段**：只 auth/registry 读 `.npmrc`，其余设置读 `pnpm-workspace.yaml`。
3. **npmmirror audit 404 `NOT_IMPLEMENTED`**：审计走官方源（见第 1 节）。
4. **CI 锁文件失败**：本地改动 package.json 后先 `pnpm install` 更新 `pnpm-lock.yaml` 并提交；CI 用 `--frozen-lockfile`。
5. **模板/新 app 构建报 `Element is missing end tag` 且定位在某行**：多半是正文裸写了 `<xxx>` 尖括号，用行内代码包裹或转义。
6. **gen:sidebar 收集到 0 章**：SUMMARY 缺 `## 篇名` 分组标题。
7. **`pnpm/action-setup` 与 setup-node 顺序**：CI 里先 `pnpm/action-setup@v4`，再 `actions/setup-node` 配 `cache: pnpm`。
8. **依赖安全告警**：echarts<6 XSS（仅渲染作者自写 JSON，无外部输入）、esbuild（仅 dev server）、katex 原型污染（默认 trust:false 不可利用）当前发布形态均不可达；详见 `THIRD_PARTY_LICENSES.md`。
9. **CI 质量门禁 `manifest/fingerprint 比对` 在 Linux 失败、本地 Windows 却全绿（跨平台换行）**：`.gitattributes` 为 `* text=auto`，Windows 检出 CRLF、Linux 检出 LF；若内容指纹对文件**原始字节** sha256，同一份逻辑内容会在两平台算出不同 revision。修复统一在哈希前把 CRLF/CR 归一为 LF（与仓库 blob 一致）：TS `content-core` 的 `normalizeTextForHash`、Python `freeze_manifest.py` 的 `normalize_text_for_hash`。**切勿删除这两个归一化函数**，否则 Linux CI 必挂。自检要点：修复后本地（CRLF）生成的 revision 必须等于 CI（Linux）的 revision；改动指纹算法后须重新冻结快照（见第 6 节）。
