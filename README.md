# Hardware Handbook · 硬件工程师手册

> 从零开始、由浅入深的开源硬件知识手册：电路基础 → 元器件 → 模拟电路与运放 → 数字电路 → 单片机硬件 → 电源设计 → PCB/EMC → 测量调试与工程实践。
>
> 每章包含原理图、静态/动态分析、环路分析、设计示例、常见坑与自测题。本仓库是 **pnpm Monorepo**：在线 VitePress 与离线单文件 HTML 双形态，共用同一份 Markdown（唯一事实源）。

- 在线阅读：<https://gold99lt.github.io/hardware-handbook/>
- 国内镜像：<https://hardware-handbook.pages.dev/>
- 架构蓝图：[`ARCHITECTURE.md`](ARCHITECTURE.md) ｜ 操作手册：[`docs/PLAYBOOK.md`](docs/PLAYBOOK.md) ｜ 贡献指南：[`CONTRIBUTING.md`](CONTRIBUTING.md) ｜ 决策记录：[`docs/adr/`](docs/adr/)

## 内容总览（140 章 + 411 张原理图）

| 篇 | 内容 | 章节数 |
|---|---|---|
| 第一篇 | 电路基础 | 14 |
| 第二篇 | 元器件详解 | 13 |
| 第三篇 | 模拟电路与运放（核心） | 33 |
| 第四篇 | 数字电路与逻辑 | 12 |
| 第五篇 | 单片机与嵌入式硬件 | 13 |
| 第六篇 | 电源设计 | 12 |
| 第七篇 | PCB 设计与 EMC | 13 |
| 第八篇 | 测量、调试与工程实践 | 12 |
| 第九篇 | 硬件测试与面试题库 | 9 |
| 附录 | 术语表 / 选型速查 / 实验清单等 | 9 |

## 环境要求

- Node 22 + **pnpm 12**（用 corepack 启用，见 [PLAYBOOK](docs/PLAYBOOK.md)）
- Python 3.11+（离线构建与质检，核心脚本仅用标准库）

## 快速开始

```bash
pnpm install
pnpm --filter @hw/handbook docs:dev       # 本地开发（自动生成 sidebar/catalog）
pnpm --filter @hw/handbook docs:build     # 在线构建
pnpm --filter @hw/handbook docs:preview   # 预览构建产物
```

## 离线单文件版（无需联网）

```bash
pnpm offline
# = python packages/tooling/src/freeze_manifest.py
#   + python packages/tooling/src/build_single_html.py --manifest .generated/content-manifest.json
# 产物：dist/hardware-handbook.html（约 6 MB，自包含 140 章），并用 manifest 对账
```

## 质量门禁

```bash
pnpm verify      # 在线构建 + 空脚手架构建 + learning 单测 + run_quality + 离线对账
pnpm quality     # 仅 run_quality：路由/内容快照 + validate/scan_math/scan_grounds/scan_svg_order
```

## 新增一个专项

`templates/site-template` 是与正式 app 同形态的脚手架：复制到 `apps/<app>`，改 appId/标题/篇名，写内容即可。详见 [PLAYBOOK 第 9 节](docs/PLAYBOOK.md#9-新增一个专项-app)。

## 仓库结构

```
hardware-handbook/
├── apps/handbook/docs/   # 140 章 Markdown + assets SVG（唯一事实源）+ SUMMARY.md
├── packages/
│   ├── shared-config/    # defineHwConfig：通用 markdown/搜索/插件
│   ├── theme/            # 布局、品牌、学习 UI、EChart、图片查看器
│   ├── content-core/     # 内容 manifest 生成（TS）
│   ├── learning/         # 学习数据仓储（按 appId 隔离、迁移、导入导出）
│   └── tooling/          # Python 离线构建/质检/vendor（零第三方依赖）
├── templates/site-template/  # 新专项脚手架
├── tests/                # 路由/内容指纹快照（CI 基准）
├── docs/                 # 活文档：PLAYBOOK + ADR
└── .github/workflows/    # quality.yml（门禁）、deploy-docs/cloudflare
```

## 部署

- GitHub Pages（主）：`.github/workflows/deploy-docs.yml`，推 `main` 即构建发布，base `/hardware-handbook/`；首次需在 Settings → Pages 将 Source 设为 **GitHub Actions**。
- Cloudflare Pages（镜像，根路径）：`deploy-cloudflare.yml` 构建时设 `VP_BASE=/`；控制台绑定方式见 PLAYBOOK。
- 已发布 URL 受 `tests/routes.snapshot.json` 保护，任何路径变更须先写 ADR。

## 扩展章节

在对应篇目录写 md、在 `apps/handbook/docs/SUMMARY.md` 加一行、重新构建。写作规范见 [`packages/tooling/AGENTS.md`](packages/tooling/AGENTS.md)，破坏性变更/ADR 规则见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## License

- 代码与构建工具：[MIT License](LICENSE)
- 文档内容（`apps/handbook/docs/`）：[CC BY-SA 4.0](apps/handbook/docs/LICENSE-docs.md)
