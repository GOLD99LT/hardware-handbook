# Hardware Handbook · 硬件工程师手册

> 一本从零开始、由浅入深的开源硬件知识手册：电路基础 → 元器件 → 模拟电路与运放 → 数字电路 → 单片机硬件 → 电源设计 → PCB/EMC → 测量调试与工程实践。
>
> 面向硬件初学者与希望系统梳理知识的工程师。每章包含原理图、静态/动态分析、环路分析、设计示例、常见坑与自测题。

- 在线阅读：_网站建设中（GitHub Pages / VitePress）_
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
| 附录 | 术语表 / 选型速查 / 实验清单等 | 8 |

## 快速开始

### 阅读

直接打开构建好的单文件 HTML（`dist/hardware-handbook.html`），无需联网、无需安装任何东西。

### 从源码构建（需要 Python 3.8+，无第三方依赖）

```bash
python tools/build_single_html.py
# 输出 dist/hardware-handbook.html
```

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
│   └── assets/      # 原理图 SVG / 波形图
├── tools/           # 构建脚本、模板、AI 协作规范
├── sources.list.yaml# 参考资料清单
├── web/             # 网站工程（阶段三）
└── dist/            # 构建产物（单文件 HTML）
```

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
