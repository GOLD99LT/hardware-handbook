# Hardware Handbook · 硬件工程师手册

> 一本从零开始、由浅入深的开源硬件知识手册：电路基础 → 元器件 → 模拟电路与运放 → 数字电路 → 单片机硬件 → 电源设计 → PCB/EMC → 测量调试与工程实践。
>
> 面向硬件初学者与希望系统梳理知识的工程师。每章包含原理图、静态/动态分析、环路分析、设计示例、常见坑与自测题。

- 在线阅读：<https://gold99lt.github.io/hardware-handbook/>
- 离线单文件版：见 [`dist/`](dist/)（运行构建脚本生成）
- 总目录：[`docs/SUMMARY.md`](docs/SUMMARY.md)

## 内容总览

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

## 快速开始

### 阅读

直接打开构建好的单文件 HTML（`dist/hardware-handbook.html`），无需联网、无需安装任何东西。

### 从源码构建（需要 Python 3.8+，无第三方依赖）

```bash
python tools/build_single_html.py
# 输出 dist/hardware-handbook.html
```

### 文档站（VitePress）

文档站与离线单文件版共用同一批 Markdown（`docs/` 是唯一事实来源），只是渲染与打包方式不同。

```bash
npm install
npm run docs:dev      # 本地预览，热更新
npm run docs:build    # 构建（先 python tools/build_vp_sidebar.py 自动生成侧边栏，再 vitepress build）
npm run docs:preview  # 预览构建产物（默认输出到 docs/.vitepress/dist）
```

> 上线步骤见下方「## 部署」：首次需在仓库 Settings → Pages 将 Source 切为 **GitHub Actions**。

## 部署

三种产物共用同一批 Markdown（`docs/` 是唯一事实源）：GitHub 源码、离线单文件 HTML、在线文档站。
在线构建（`npm run docs:build`）与离线构建（`python tools/build_single_html.py`）读的是同一批 `.md` 与 `SUMMARY.md`，保证内容永远一致。

### GitHub Pages（主部署）

- 地址：<https://gold99lt.github.io/hardware-handbook/>，base 路径 `/hardware-handbook/` 已在 `docs/.vitepress/config.mts` 配置。
- 流水线：[`.github/workflows/deploy-docs.yml`](.github/workflows/deploy-docs.yml)，推送 `main`（或手动 Actions → Run workflow）即自动 `npm ci → npm run docs:build → 发布`。
- **首次上线一次性开关**：仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**（选完即可，之后无需再动）。

### Cloudflare Pages 镜像（可选，国内访问增强）

> 状态：**待办**。真正启用需要你自己的 Cloudflare 账号，未配置前不影响主站。

方式一（推荐，控制台绑定，零 Secrets）：

1. 登录 Cloudflare Dashboard → **Workers & Pages → Create → Pages → Connect to Git**，授权并选中 `gold99lt/hardware-handbook`。
2. 构建配置：
   - **Framework preset**：无 / None
   - **Build command**：`npm run docs:build`
   - **Build output directory**：`docs/.vitepress/dist`
   - **环境变量**：`NODE_VERSION=22`；**`VP_BASE=/`**——Pages 部署在根路径，需以此环境变量让站点按根 base 构建（config.mts：`process.env.VP_BASE || '/hardware-handbook/'`；GitHub Pages 流水线不设该变量，保持 `/hardware-handbook/`）
3. 推送 `main` 即自动构建发布，得到 `https://hardware-handbook.pages.dev`。

方式二（Actions 自动部署）：[`.github/workflows/deploy-cloudflare.yml`](.github/workflows/deploy-cloudflare.yml)。
启用前在仓库 **Settings → Secrets and variables → Actions** 配置 `CLOUDFLARE_API_TOKEN` 与 `CLOUDFLARE_ACCOUNT_ID`，并在 Cloudflare 侧创建 Pages 项目 `hardware-handbook`。

💡 **base 路径说明**：GitHub Pages 项目站用 `base: '/hardware-handbook/'`；Cloudflare Pages 跑在根路径，因此镜像构建需设 `VP_BASE=/`（控制台方式在环境变量里加，Actions 方式已在 workflow 内置好）。

### 校验内容

```bash
python tools/validate.py
```

## 仓库结构

```
hardware-handbook/
├── docs/            # 知识内容（Markdown，唯一事实来源）
│   ├── SUMMARY.md   # 装配清单（决定篇章顺序）
│   ├── basics/ ... practice/   # 各篇文件夹
│   ├── assets/      # 原理图 SVG / 波形图
│   └── .vitepress/  # VitePress 站点工程（配置、主题、组件；产物 dist/ 不入库）
├── tools/           # 构建脚本、模板、AI 协作规范
├── sources.list.yaml# 参考资料清单
└── dist/            # 离线单文件构建产物
```

> 注：早期规划中的 `web/` 目录已废弃，站点工程位于 `docs/.vitepress/`。

## 如何扩展（新增/修改章节）

1. 在对应篇文件夹中新建/修改 Markdown 文件（模板见 `tools/templates/chapter.md`）；
2. 在 `docs/SUMMARY.md` 中加入一行；
3. 重新运行构建脚本。

详见 [`tools/AGENTS.md`](tools/AGENTS.md)。

## 贡献

欢迎提 Issue 纠错、补充内容、提交 Pull Request。内容请遵循章节模板，并在 front matter 的 `sources` 中注明参考来源。

## License

- 代码与构建工具：[MIT License](LICENSE)
- 文档内容（`docs/`）：[CC BY-SA 4.0](docs/LICENSE-docs.md)
