# -*- coding: utf-8 -*-
"""
merge_sources.py — 合并 sources/index-a.yaml / index-b.yaml / index-c.yaml，
去重后回填 sources.list.yaml（official / github / books / other 四桶），
并打印 122 章 A/B 级覆盖矩阵与缺口。

只做索引合并，不写正文、不 git commit。
"""
import os, sys
import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from paths_util import REPO_ROOT

ROOT = REPO_ROOT
SRC = os.path.join(ROOT, "sources")


def load(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


# 全书 122 章 id（按 SUMMARY 顺序）
ORDER = [
    # 第一篇 电路基础
    "voltage-current-power", "ohms-law", "series-parallel", "kcl-kvl",
    "nodal-mesh-analysis", "capacitor-rc", "inductor-rl", "dc-ac", "impedance",
    "rlc-resonance", "transformer", "mains-three-phase", "electrical-safety",
    "math-basics",
    # 第二篇 元器件
    "resistors", "smd-packages-e-series", "special-resistors", "capacitors",
    "capacitor-parameters", "inductors-ferrite-beads", "diodes",
    "zener-led-tvs", "bjt", "mosfet", "igbt-scr-relay-optocoupler",
    "crystal-oscillator", "switches-connectors-fuses",
    # 第三篇 模电/运放
    "analog-signal-chain", "diode-circuits", "linear-regulator-reference",
    "bjt-amplifiers", "small-signal-model", "power-amplifiers",
    "opamp-overview", "ideal-opamp", "open-loop-feedback", "feedback-topologies",
    "stability-bode", "supply-rails", "cmrr-psrr", "offset-bias",
    "gbp-slew-rate", "noise", "voltage-follower", "inverting-amplifier",
    "non-inverting-amplifier", "differential-amplifier",
    "instrumentation-amplifier", "summing-amplifier",
    "integrator-differentiator", "first-order-filters", "sallen-key-filters",
    "bandpass-bandstop", "comparator-hysteresis", "oscillators", "555-timer",
    "precision-rectifier-peak-samplehold", "vi-iv-converter",
    "analog-switch-mux", "single-supply-biasing",
    # 第四篇 数电
    "number-systems", "logic-gates-boole", "combinational-logic", "flip-flops",
    "registers-counters", "timing-analysis-metastability",
    "tri-state-bus-pull", "logic-levels", "memory", "level-shifter",
    "fpga-verilog", "clock-reset-design",
    # 第五篇 单片机
    "mcu-overview", "minimum-system", "gpio", "interrupts", "adc", "dac",
    "timer-pwm", "uart-rs232", "rs485-can", "i2c-spi", "usb-ethernet",
    "watchdog-rtc-lowpower", "peripheral-design",
    # 第六篇 电源
    "power-specs", "linear-supply", "ldo", "buck", "boost-buckboost",
    "power-component-selection", "smps-control-loop", "flyback",
    "battery-charger", "power-monitoring-loadswitch", "grounding",
    "power-integrity-decoupling",
    # 第七篇 PCB/EMC
    "pcb-stackup", "eda-tools", "schematic-library", "placement", "routing",
    "analog-digital-power-routing", "signal-integrity",
    "crosstalk-differential", "emi-emc", "shielding-filtering-grounding",
    "esd-protection", "thermal-design", "dfm-process",
    # 第八篇 实践
    "multimeter", "oscilloscope", "signal-generator-load",
    "logic-analyzer-spectrum", "soldering", "debug-methodology",
    "troubleshooting-cases", "reliability-derating", "safety-certification",
    "development-flow", "bom-version-cost", "ltspice",
]

RANK = {"A": 0, "B": 1, "C": 2}


def union_chapters(a, b):
    out = list(a or [])
    for c in (b or []):
        if c not in out:
            out.append(c)
    return out


def best_rating(a, b):
    if not a:
        return b
    if not b:
        return a
    return a if RANK.get(a, 9) <= RANK.get(b, 9) else b


# awesome-electronics 在三个索引中重复：显式合并为一条（章节并集 + 最新核实元数据）
AWESOME_URL = "https://github.com/kitspace/awesome-electronics"
AWESOME = {
    "name": "awesome-electronics (kitspace)",
    "url": AWESOME_URL,
    "type": "repo",
    "stars": 8198,
    "last_active": "2026-09",
    "license": "CC0-1.0",
    "rating": "A",
    "chapters": [
        # A：基础/器件/运放入口
        "voltage-current-power", "ohms-law", "series-parallel", "kcl-kvl",
        "capacitor-rc", "inductor-rl", "rlc-resonance", "diodes", "bjt",
        "mosfet", "opamp-overview", "analog-signal-chain",
        # B：PCB/EDA
        "eda-tools", "schematic-library", "placement", "routing",
        "dfm-process", "pcb-stackup",
        # C：实践/流程
        "soldering", "development-flow", "bom-version-cost", "multimeter",
        "oscilloscope", "ltspice", "peripheral-design",
    ],
    "summary": "Kitspace 维护的电子工程师资源大清单（教程/课程/仿真器/EDA/元件库/PCB 制造/分销/社区），既是选型与流程入口，也是发现其余资料的索引枢纽",
    "cloned": True,
    "clone_path": "sources/repos/awesome-electronics",
}


def dedup(entries, key):
    merged = {}
    order = []
    for e in entries:
        k = key(e)
        if k not in merged:
            merged[k] = dict(e)
            order.append(k)
        else:
            base = merged[k]
            base["chapters"] = union_chapters(base.get("chapters"), e.get("chapters"))
            base["rating"] = best_rating(base.get("rating"), e.get("rating"))
            for fld in ("license", "vendor", "note_path", "clone_path",
                        "last_active", "author", "isbn", "year", "summary"):
                if not base.get(fld) and e.get(fld):
                    base[fld] = e[fld]
            if e.get("cloned"):
                base["cloned"] = True
            s1, s2 = base.get("stars"), e.get("stars")
            if isinstance(s2, (int, float)) and (not isinstance(s1, (int, float)) or s2 > s1):
                base["stars"] = s2
    return [merged[k] for k in order]


def main():
    with open(os.path.join(ROOT, "sources.list.yaml"), encoding="utf-8") as f:
        existing = yaml.safe_load(f) or {}

    a, b, c = load("index-a.yaml"), load("index-b.yaml"), load("index-c.yaml")

    # ---- github：剔除三条 awesome-electronics，用显式合并条目，其余按 url 去重 ----
    gh = [e for e in (a.get("github", []) + b.get("github", []) + c.get("github", []))
          if e.get("url") != AWESOME_URL]
    gh = dedup(gh, lambda e: e.get("url"))
    gh.insert(0, AWESOME)

    # ---- official：保留既有 6 条，追加三片新条目，按 name 去重 ----
    off = list(existing.get("official", []))
    new_off = a.get("official", []) + b.get("official", []) + c.get("official", [])
    off = dedup(off + new_off, lambda e: e.get("name"))

    # ---- books：按 ISBN（去连字符）去重 ----
    books = a.get("books", []) + b.get("books", []) + c.get("books", [])
    books = dedup(books, lambda e: str(e.get("isbn", "")).replace("-", "").strip())

    # ---- other：按 url 去重 ----
    other = a.get("other", []) + b.get("other", []) + c.get("other", [])
    other = dedup(other, lambda e: e.get("url"))

    data = {"official": off, "github": gh, "books": books, "other": other}

    # 自定义 Dumper：纯标量序列（chapters）内联为 flow 风格
    class FlowDumper(yaml.SafeDumper):
        pass

    def list_rep(d, value):
        flow = all(isinstance(x, (str, int, float, bool)) for x in value) and len(value) > 0
        return d.represent_sequence("tag:yaml.org,2002:seq", value, flow_style=flow)

    FlowDumper.add_representer(list, list_rep)

    header = (
        "# 参考资料清单\n"
        "# 由 tools/merge_sources.py 合并 sources/index-a.yaml|index-b.yaml|index-c.yaml 生成。\n"
        "# 调研阶段只做索引、一句话摘要与本地参考缓存，不整段搬运；书籍只列书目。\n"
        "# 字段：name / url / type(repo|app-note|course|book|video|tool) /\n"        "#   vendor 或 license / stars / last_active / rating(A|B|C) / chapters[] / summary\n"
        "# 本地缓存：cloned+clone_path（浅克隆于 sources/repos）、note_path（要点于 sources/notes）。\n\n"
    )
    body = yaml.dump(data, Dumper=FlowDumper, allow_unicode=True,
                     sort_keys=False, default_flow_style=False, width=4096,
                     indent=2)
    with open(os.path.join(ROOT, "sources.list.yaml"), "w", encoding="utf-8",
              newline="\n") as f:
        f.write(header + body)

    # ---- 覆盖矩阵（只统计 A/B；C 不计入达标）----
    ab = {}
    allc = {}
    for bucket in data.values():
        for e in bucket:
            for ch in e.get("chapters", []):
                allc[ch] = allc.get(ch, 0) + 1
                if e.get("rating") in ("A", "B"):
                    ab[ch] = ab.get(ch, 0) + 1

    missing = [ch for ch in ORDER if ch not in ab]
    thin = [ch for ch in ORDER if ab.get(ch, 0) == 1]
    illegal = [ch for ch in allc if ch not in ORDER]

    print("== 桶计数 ==", {k: len(v) for k, v in data.items()})
    print("总条目:", sum(len(v) for v in data.values()))
    print("A/B 未覆盖章节(%d):" % len(missing), missing)
    print("仅 1 条 A/B 的偏薄章节(%d):" % len(thin), thin)
    print("非法 chapter id:", illegal)
    print("已浅克隆仓库:", [e["clone_path"] for e in gh if e.get("cloned")])


if __name__ == "__main__":
    main()
