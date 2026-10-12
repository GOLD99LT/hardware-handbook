// 章节目录：从自动生成的侧边栏抽取「relativePath -> 标题 / 链接」。
// 侧边链接形如 /basics/voltage-current-power，对应 page.relativePath = basics/voltage-current-power.md。
import sidebar from '../../../sidebar.generated.mjs'

export interface CatalogEntry {
  /** 与 useData().page.relativePath 一致，带 .md 后缀 */
  path: string
  /** 章节标题（侧边栏 text） */
  title: string
  /** 干净 URL（无 .md，cleanUrls 模式下可直接跳转） */
  link: string
}

const byPath = new Map<string, CatalogEntry>()

function walk(items: any[]) {
  if (!Array.isArray(items)) return
  for (const it of items) {
    if (it.link) {
      const link: string = it.link
      const path = link.replace(/^\//, '') + '.md'
      if (!byPath.has(path)) {
        byPath.set(path, { path, title: it.text || link, link })
      }
    }
    if (Array.isArray(it.items)) walk(it.items)
  }
}

walk(sidebar as any)

export const catalog: CatalogEntry[] = Array.from(byPath.values())

/** path -> 标题 */
export const catalogTitle: Record<string, string> = Object.fromEntries(
  catalog.map((c) => [c.path, c.title])
)

/** path -> 干净链接 */
export const catalogLink: Record<string, string> = Object.fromEntries(
  catalog.map((c) => [c.path, c.link])
)
