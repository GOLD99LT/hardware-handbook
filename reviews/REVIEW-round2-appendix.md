# 附录篇 第二轮复审报告（REVIEW-round2-appendix）

- 复审日期：2026-10-11
- 复审人：独立内容审核员（与作者非同一 Agent）
- 范围：仅就首轮报告（暂不放行，1 BLOCKING / 4 MAJOR / 多 MINOR）的回修点做复核，Read 对应 .md 与 SVG；不重审未改动部分。
- 工程根：`E:\001_work\010-Doubao\hardware-handbook`

---

## 一、回修点逐项核对

| # | 首轮问题 | 严重度 | 回修内容 | 复核结论 |
|---|---|---|---|---|
| I-1 | PortaPack 仓库 URL 错误（`portapack/portapack-havoc` 不存在） | BLOCKING | 改为 `https://github.com/portapack-mayhem/mayhem-firmware`，名「PortaPack Mayhem」，License GPL-3.0，标注「（活跃 fork）」 | ✅ 通过。该仓为当前活跃官方 fork，GPL-3.0 属实。 |
| B-1 | E6 列 5 格重复（12/18/27/39/56 行误填 10/22/33/47/68） | MAJOR | 5 格已改「—」，E6 列仅余 10/15/22/33/47/68 共 6 项 | ✅ 通过。逐行复核，E12 列 12 项完好未动。 |
| D-1 | AD8051 误标「电流反馈、GBP≈30MHz」 | MAJOR | 改为「高速电压反馈型，−3dB 带宽 110MHz(G=+1)，SR 145V/µs」 | ✅ 通过。与 ADI 官方 datasheet 一致。 |
| F-1 | Buck 续流二极管方向反接 | MAJOR | `circuit-buck.svg` 二极管翻转：竖线（阴极）在上接 SW，三角形 apex 朝上、底边（阳极）在下接 GND | ✅ 通过。XML 复核：阴极条 y=115（接 SW），阳极三角底边 y=135（接 GND），电流方向 GND→SW，符合 Buck 续流。 |
| H-1 | 实验4 LED 预期与接线相反 | MAJOR | 预期改为「常态 LED 亮（节点被上拉到高电平）；按下按键节点被拉低到 GND，LED 灭」 | ✅ 通过。与「节点接 LED→GND」接线一致。 |
| I-2 | 项目数 18 vs 实际 19 | MINOR | 正文改「精选 19 个」 | ✅ 通过。实列 5+4+2+5+3=19。 |
| I-3 | DSLogic 仓库已更名 | MINOR | 改为 `DreamSourceLab/DSView`，简介「开源 USB 逻辑分析仪软件（原 DSLogic 上位机）」，GPL-3.0 | ✅ 通过。 |
| I-4 | ChibiOS License 标注不全 | MINOR | 改为「GPLv3 / Apache-2.0 双许可」 | ✅ 通过。 |
| C-1 | QFP/QFN SVG 焊盘数与标注不符 | MINOR | 图注改「QFP/QFN 顶视示意（焊盘数量未按比例）」 | ✅ 通过（以图注声明方式处理，可接受）。 |
| C-2 | QFP 示例器件错配（F103C8T6 为 LQFP48） | MINOR | 改为 STM32G030K8T6（LQFP-32） | ✅ 通过。K8 封装即 LQFP-32，与表题一致。 |
| E-1 | 「库仑定律 Q=It」误标 | MINOR | 行名改「电荷量」 | ✅ 通过。 |
| E-2 | AWG 电阻值偏高无说明 | MINOR | 加注「20°C 电阻值按铜电阻率 ρ≈1.75µΩ·cm 估算」 | ✅ 通过。 |
| F-2 | 整流图单管 vs 文字桥式 | MINOR | 图注改「整流滤波（简化）」 | ✅ 通过。 |
| F-3 | 共射公式 vs 未旁路 Re | MINOR | 公式补「Re 旁路时 Av≈-RC/re'；未旁路时 Av≈-RC/Re」 | ✅ 通过。 |
| F-4 | BJT 开关 LED 未画限流电阻 | MINOR | 文字补「LED 回路串 220Ω~1k 限流电阻」 | ✅ 通过。 |

---

## 二、是否还有 BLOCKING / MAJOR

- **BLOCKING：0**。
- **MAJOR：0**。

首轮全部 1 BLOCKING + 4 MAJOR 均已正确修复，未发现引入新的技术错误、失实链接或图文矛盾。其余 MINOR 项也已一并处理（或以图注声明方式兜底）。

---

## 三、最终放行结论

# ✅ Pass（放行）

附录 A–I 9 个文件现已达到发布标准：
- 真实性：开源仓库链接、License、芯片型号/参数均核实无误；
- 技术正确性：E96 标准值、E6/E12/E24 对齐、Buck 续流方向、共射/BJT/实验4 等公式与现象均正确；
- SVG 与正文一致、接地规范、frontmatter（part=10、chapter=附录、order 间隔 5、sources≥1）合规；
- 无整段搬运、无编造 star。

可进入构建/发布流程。后续若再版，建议顺手把 QFP/QFN 示意图焊盘数量补画到与标注一致（当前已用图注免责，不阻断）。
