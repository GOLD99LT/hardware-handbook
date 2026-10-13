# 第三方资源与许可证清单（THIRD-PARTY LICENSES）

> 本文件记录《硬件工程师手册》（hardware-handbook）使用的第三方库、运行时 vendor、字体及其许可证。
> 生成时间：2026-10-14（P0 基线）。仓库本体：代码 **MIT**、文档 **CC BY-SA 4.0**（见 `LICENSE`、`docs/LICENSE-docs.md`）。
> 各依赖完整许可证文本以其包内 `LICENSE` 文件为准；本文件负责署名、归类与审计记录。

## 1. 直接依赖（构建与运行时）

| 包 | 版本 | 许可证 | 用途 | 上游 |
| --- | --- | --- | --- | --- |
| vitepress | 1.6.4 | MIT | 静态文档站框架（Vue3 + Vite） | https://github.com/vuejs/vitepress |
| vue | 3.5.43 | MIT | 前端框架（vitepress 传递） | https://github.com/vuejs/core |
| vite | 5.4.21 | MIT | 构建/开发服务器（vitepress 传递） | https://github.com/vitejs/vite |
| echarts | 5.6.0 | Apache-2.0 | 交互图表渲染（在线版） | https://github.com/apache/echarts |
| zrender | 5.6.1 | BSD-3-Clause | echarts 底层渲染（传递） | https://github.com/ecomfe/zrender |
| katex | 0.16.47 | MIT | 数学公式渲染（在线版） | https://github.com/KaTeX/KaTeX |
| @vscode/markdown-it-katex | 1.1.2 | MIT | markdown-it 的 KaTeX 插件 | https://github.com/microsoft/vscode-markdown-it-katex |
| markdown-it-container | 4.0.0 | MIT | 自定义容器（motivation/analogy/…） | https://github.com/markdown-it/markdown-it-container |
| minisearch | 7.2.0 | MIT | 本地全文搜索（vitepress 传递） | https://github.com/lucaong/minisearch |
| shiki | 2.5.0 | MIT | 代码高亮（vitepress 传递） | https://github.com/shikijs/shiki |

## 2. 离线形态 vendor（`tools/vendor/`，随离线单文件分发）

| 资源 | 许可证 | 说明 |
| --- | --- | --- |
| `echarts.min.js` | Apache-2.0 | Apache ECharts 离线运行时，与在线版同系（5.6.x） |
| `katex.min.js` / `katex.min.css` | MIT | KaTeX 离线运行时与样式 |
| `fonts/KaTeX_*.woff2` | 各字体对应开放字体许可证 | 见下节 |

### KaTeX 字体许可证
KaTeX 自托管 Web 字体沿用其上游字体许可证，**并非全部为 MIT**：
- 由 **Latin Modern / Computer Modern 派生**的字体（`KaTeX_Main`、`KaTeX_Math`、`KaTeX_SansSerif`、`KaTeX_Size1…4`、`KaTeX_Typewriter`、`KaTeX_Script`）遵循 **GUST Font License（GFL）**。
- `KaTeX_AMS` 遵循 **AMS Fonts License**（American Mathematical Society）。
- `KaTeX_Caligraphic`、`KaTeX_Fraktur` 遵循其各自的开放字体许可证（见 KaTeX 上游）。
- 准确口径以 KaTeX 上游 `LICENSE` 与字体目录说明为准：https://github.com/KaTeX/fonts 及 https://katex.org/docs/license。

## 3. 全部传递依赖（按许可证归类）

### MIT（绝大多数）
@algolia/abtesting, @algolia/autocomplete-core, @algolia/autocomplete-plugin-algolia-insights, @algolia/autocomplete-preset-algolia, @algolia/autocomplete-shared, @algolia/client-abtesting, @algolia/client-analytics, @algolia/client-common, @algolia/client-insights, @algolia/client-personalization, @algolia/client-query-suggestions, @algolia/client-search, @algolia/ingestion, @algolia/monitoring, @algolia/recommend, @algolia/requester-browser-xhr, @algolia/requester-fetch, @algolia/requester-node-http, @babel/helper-string-parser, @babel/helper-validator-identifier, @babel/parser, @babel/types, @docsearch/css, @docsearch/js, @docsearch/react, @esbuild/win32-x64, @iconify/types, @jridgewell/sourcemap-codec, @rollup/rollup-win32-x64-gnu, @rollup/rollup-win32-x64-msvc, @shikijs/core, @shikijs/engine-javascript, @shikijs/engine-oniguruma, @shikijs/langs, @shikijs/themes, @shikijs/transformers, @shikijs/types, @shikijs/vscode-textmate, @types/estree, @types/hast, @types/linkify-it, @types/markdown-it, @types/mdast, @types/mdurl, @types/unist, @types/web-bluetooth, @vitejs/plugin-vue, @vscode/markdown-it-katex, @vue/compiler-core, @vue/compiler-dom, @vue/compiler-sfc, @vue/compiler-ssr, @vue/devtools-api, @vue/devtools-kit, @vue/devtools-shared, @vue/reactivity, @vue/runtime-core, @vue/runtime-dom, @vue/server-renderer, @vue/shared, @vueuse/core, @vueuse/integrations, @vueuse/metadata, @vueuse/shared, birpc, ccount, character-entities-html4, character-entities-legacy, comma-separated-tokens, commander, copy-anything, csstype, dequal, devlop, emoji-regex-xs, esbuild, estree-walker, focus-trap, hast-util-to-html, hast-util-whitespace, hookable, html-void-elements, katex, magic-string, mark.js, markdown-it-container, mdast-util-to-hast, micromark-util-character, micromark-util-encode, micromark-util-sanitize-uri, micromark-util-symbol, micromark-util-types, minisearch, mitt, nanoid, oniguruma-to-es, perfect-debounce, postcss, preact, property-information, regex-recursion, regex-utilities, regex, rfdc, rollup, search-insights, shiki, space-separated-tokens, stringify-entities, superjson, tabbable, trim-lines, unist-util-is, unist-util-position, unist-util-stringify-position, unist-util-visit-parents, unist-util-visit, vfile-message, vfile, vite, vitepress, vue。

### 其他许可证
| 包 | 版本 | 许可证 |
| --- | --- | --- |
| echarts | 5.6.0 | Apache-2.0 |
| zrender | 5.6.1 | BSD-3-Clause |
| entities | 7.0.1 | BSD-2-Clause |
| source-map-js | 1.2.2 | BSD-3-Clause |
| speakingurl | 14.0.1 | BSD-3-Clause |
| @ungap/structured-clone | 1.4.0 | ISC |
| picocolors | 1.1.1 | ISC |
| tslib | 2.3.0 | 0BSD |
| @iconify-json/simple-icons | 1.2.99 | CC0-1.0 |

> 注：`@iconify-json/simple-icons`、`@algolia/*`、`@docsearch/*`、`preact` 等为工具链/图标数据，仅出现在开发依赖闭包中；最终发布页面不含其运行时（按实际 bundle 为准）。

## 4. 依赖安全审计（2026-10-14）

审计方式：`npm audit --registry=https://registry.npmjs.org/`（默认安装走镜像 npmmirror，镜像未实现 audit 端点，故审计直连官方）。共 6 条（2 low / 3 moderate / 1 high）：

| 受影响 | 严重度 | 公告 | 在本项目的可达性 | 处置 |
| --- | --- | --- | --- | --- |
| echarts <6.1.0 | moderate | GHSA-fgmj-fm8m-jvvx（option XSS） | **不可达**：echarts 仅渲染作者自写的 JSON option，无外部/用户输入来源 | 记录；echarts 6 为破坏变更，升级列入 Backlog，不在重构零变化范围内 |
| esbuild ≤0.24.2 | moderate | GHSA-67mh-4wv8-2f99（dev server 可被任意网站发请求） | **不影响产物**：仅本地开发服务器 | 随 vite/vitepress 上游更新；记录 |
| vite / vitepress | low（链） | 依赖上述 esbuild | 同上，仅 dev | 记录 |
| katex 0.11–0.18.1 | high | GHSA-238p-pmpm-9mq7（原型污染可绕过 trust） | **不可利用**：本站使用 KaTeX 默认 `trust:false`，未启用任何受 trust 保护的命令 | 记录；待上游修复版本跟进 |
| @vscode/markdown-it-katex | low（链） | 依赖上述 katex | 同上 | 记录 |

**结论**：无一项在当前发布形态（作者自写内容、资源全本地化、无外部输入）中可被实际利用；无需在本次重构中升级（升级会破坏“零行为变化”）。后续建立 high/critical 阻断与自动更新（Backlog B11）。

## 5. 资源本地化
所有运行时资源（KaTeX、ECharts、字体、SVG）均随仓库/离线包自托管，不依赖 Google CDN 或第三方在线服务；满足离线零依赖。
