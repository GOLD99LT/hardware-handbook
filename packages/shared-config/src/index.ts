// @hw/shared-config —— P1 占位骨架。
// P2 起提供 defineHwConfig(options)：五类容器、KaTeX、CJK 加粗、details 折叠、
// ECharts 围栏、figure 化、frontmatter 修复、本地搜索中文、难度默认名等通用规则。
// 边界铁律：只封装通用规则，不读取任何 app 的私有路径。

export const PACKAGE_NAME = '@hw/shared-config' as const
export const VERSION = '0.1.0' as const

/** 预留：options 含 appId/title/description/base/sidebar/nav/partRegistry/socialLinks/logo? */
export interface HwConfigOptions {
  appId: string
  title: string
  description?: string
  base?: string
  [key: string]: unknown
}

/** P2 落地：返回 VitePress UserConfig。当前仅占位。 */
export function defineHwConfig(_options: HwConfigOptions): Record<string, unknown> {
  throw new Error('@hw/shared-config: defineHwConfig 将在 P2 落地，当前为 P1 骨架占位')
}
