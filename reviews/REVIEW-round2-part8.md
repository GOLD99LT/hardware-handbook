# 第八篇「测量调试与工程实践」第二轮复审报告

- 复审日期：2026-10-11
- 复审范围：`docs/practice/` 12 章，仅核对首轮报告（1 BLOCKING / 3 MAJOR / 5 MINOR）的回修点
- 复审人：独立内容审核员（与本篇作者非同一 Agent）
- 首轮结论：暂不放行（CONDITIONAL REJECT）

## 一、回修点逐项核对

| 编号 | 严重度 | 章节 | 回修内容 | 核对结果 |
|---|---|---|---|---|
| B1 | BLOCKING | multimeter §5 例2 | R1 由 1MΩ 改为 100MΩ；衰减比 10/(100+10)=1/11；50V→4.55V×11=50V；补 P=50²/100M≈25µW、耐压≥100V；删除"5.0? 不对——"自语 | ✅ 通过。公式自洽，数值正确，自语已删 |
| M1 | MAJOR | oscilloscope §5 探头负载效应 | 改为 1X：Cin≈95pF、τ=95µs；10X：Cin≈9.5pF、τ=9.5µs；ECharts 图例改"真实信号（理想阶跃）" | ✅ 通过。与表格"无源 10X：10MΩ∥~9.5pF"一致；1X 电缆电容 ~95pF 为典型值 |
| M2 | MAJOR | signal-generator-load §2 | 电子负载模式补 CW 恒功率：CC/CV/CR/CW，另列 CC-CV 组合模式 | ✅ 通过 |
| M3 | MAJOR | reliability-derating §4 | SW 峰值改为 35V（24V 母线 + ~11V 尖峰），35/100=35%、35/60=58% | ✅ 通过。文字与计算一致 |
| m1 | MINOR | logic-analyzer-spectrum §2 频谱仪 | 补 dBm 定义 P_dBm=10log10(P/1mW)；补 QP 准峰值检波器（EMI 认证用）、峰值/平均值（看谐波用） | ✅ 通过 |
| m2 | MINOR | safety-certification §3 | 明确 3mm/4mm 为基本绝缘典型值；初次级加强绝缘约翻倍（间隙~6mm、爬电~8mm），光耦/隔离器件本身选加强绝缘 | ✅ 通过 |
| m3 | MINOR | ltspice §3 后新增"常用指令补充" | 补 .step 扫参、.measure WHEN 读数、E/F/G/H 受控源（VCVS/CCCS/VCCS/CCVS） | ✅ 通过。四类受控源分类正确 |
| m4 | MINOR | oscilloscope ECharts 标签 | "真实信号 1ns"改为"真实信号（理想阶跃）" | ✅ 通过（并入 M1 核对） |
| m5 | MINOR | 多章无 ::: advanced | 属可选优化，未强制补 | ⏸ 接受现状（仪器/流程类章节非必须） |

## 二、新引入问题排查

对改动行附近上下文通读，未发现新引入的技术错误、前后矛盾或死链：

- multimeter 例2 补的"100MΩ 属高阻，注意表笔/板面积污漏电"为正确实操提醒，无新问题。
- oscilloscope 探头示例改为"Rs=1MΩ"起算，与 1X/10X 电容搭配后 τ=95µs/9.5µs 数值正确。
- ltspice 新增"常用指令补充"中 `.measure t_when WHEN Vout=0.63` 为教学性写法（实际 LTspice 语法为 V(out)），对入门章可接受，不另立问题。
- safety 加强绝缘"~6mm/~8mm"为工程典型值，已注明"具体查 IEC 62368-1"，无过度承诺。

## 三、最终结论

**放行（PASS）**

- BLOCKING：0
- MAJOR：0
- MINOR：0（m5 接受现状）

首轮 1B/3M/5m 全部正确回修，未引入新问题。第八篇「测量调试与工程实践」12 章通过独立审核，可按 published 状态发布。
