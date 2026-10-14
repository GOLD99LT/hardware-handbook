---
# ===== frontmatter（每章必填）=====
id: chapter-id-in-english        # 稳定语义ID，与文件名一致，永不随插入顺序改变
title: 章节中文标题 English Term  # 显示标题
part: 3                          # 篇号 1-8
chapter: 运放应用电路             # 章分组名（可空）
order: 45                        # 篇内排序数字（越小越靠前，建议留间隔 5,10,15）
tags: [运放, 反相放大, 核心电路]   # 标签，用于聚合与搜索
difficulty: 2                    # 1入门 2进阶 3深入
status: draft                    # draft(草稿,不发布) / published(正式) / deprecated
sources:                         # 参考来源，至少1条；禁止无来源的内容
  - https://github.com/owner/repo
  - TI Precision Labs - Op Amps
---

# 章节中文标题

<!--
  写作顺序按下面 11 个模块。基础层（小白必学）与进阶层（::: advanced 折叠）分开。
  每节聚焦讲清楚一件事；多用图、表、例子，少用大段文字。
-->

## 1. 设计动机

<!-- 什么场景需要它；不用它直接接线会怎样 -->

::: motivation 为什么需要这个电路
用一两段话说清痛点与应用场景。
:::

## 2. 原理图

<!-- 统一风格 SVG，放入 docs/assets/schematics/，用相对路径引用；构建时自动内联 -->

![反相比例放大器](../assets/schematics/inverting-amplifier.svg)

## 3. 静态分析（DC）

<!-- 电容开路、电感短路，求各节点直流电位、偏置电流、静态工作点 -->

## 4. 动态分析（AC / 瞬态）

<!-- 传递函数（只给结论）、频率响应、瞬态波形；推导过程放进 advanced 折叠 -->

$$V_{out}=-\frac{R_f}{R_1}V_{in}$$

<!-- 波形图：用 echarts 代码块，内容为 ECharts option 的 JSON -->

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["Vin", "Vout"], "bottom": 0},
  "xAxis": {"type": "category", "data": [0, 1, 2, 3]},
  "yAxis": {"type": "value"},
  "series": [
    {"name": "Vin", "type": "line", "smooth": true, "data": [0, 0.2, 0, -0.2]},
    {"name": "Vout", "type": "line", "smooth": true, "data": [0, -2, 0, 2]}
  ]
}
```

## 5. 环路分析

<!-- 反馈拓扑、环路增益 T(s)、伯德图、相位裕度/增益裕度、自激条件 -->

::: advanced 进阶：环路稳定性推导
小白可先跳过。给出去断环方法、T(s) 表达式、伯德图、相位裕度判据（>45° 通常稳定）。
:::

## 6. 元件取值与工程权衡

<!-- 输入阻抗、功耗、噪声、偏置电流之间的权衡；为什么取这个数量级 -->

## 7. 完整设计示例

::: example 从需求到选值
1. 需求：把 0~0.25V 放大到 0~2.5V
2. 计算增益 G = 10
3. 取 R1 = 10kΩ，则 Rf = 100kΩ
4. 验算 Vout = -10 × 0.25 = -2.5V
:::

## 8. 仿真与实验

<!-- LTspice 网表/仿真设置，或面包板接线步骤与预期现象 -->

## 9. 常见坑与故障现象

::: pitfall 常见坑
- **坑一标题**：现象、原因、解决办法
- **坑二标题**：……
:::

## 10. 自测题

<!-- 用 details 折叠，点击展开答案 -->

<details><summary>R1=1kΩ、Rf=10kΩ、Vin=0.3V，Vout 等于多少？</summary>

Vout = -(Rf/R1) × Vin = -10 × 0.3 = **-3V**。

</details>

## 11. 参考资料

- [来源名称](https://example.com)
- 数据手册 / 应用笔记编号

<!--
  ===== Markdown 扩展语法速查（构建脚本支持）=====
  行内公式 $V=IR$；块公式 $$...$$（KaTeX 语法）
  自定义容器：
    ::: motivation 标题   设计动机（橙）
    ::: analogy 标题      直觉类比（蓝）
    ::: example 标题      设计示例（绿）
    ::: pitfall 标题      常见坑（红）
    ::: advanced 标题     进阶内容（默认折叠）
  波形图：```echarts 代码块，内容为 option JSON
  原理图：![](../assets/schematics/xxx.svg)，或 ```svg 代码块
  表格：标准 GFM 表格
  自测题：<details><summary>问题</summary>答案</details>
-->
