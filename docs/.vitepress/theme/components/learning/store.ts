// 学习数据中心：reactive 单例 + localStorage 持久化。
// 键名带版本前缀 hh.v1.*，便于将来迁移；所有 localStorage 访问都做了 SSR 守卫。
import { reactive, watch } from 'vue'
import { catalog, catalogTitle, catalogLink } from './catalog'

export type ChapterStatus = 'done' | 'learning'

export interface LearningData {
  version: number
  /** relativePath -> 'done' | 'learning'；无键即未学 */
  progress: Record<string, ChapterStatus>
  /** relativePath -> 笔记文本 */
  notes: Record<string, string>
  /** relativePath -> true；无键即未收藏 */
  favorites: Record<string, boolean>
}

/** 唯一持久化键（版本前缀） */
export const STORAGE_KEY = 'hh.v1.learning'

const state = reactive<LearningData>({
  version: 1,
  progress: {},
  notes: {},
  favorites: {}
})

let booted = false

function load() {
  if (import.meta.env.SSR || booted) return
  booted = true
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return
    const parsed = JSON.parse(raw)
    if (parsed && parsed.version === 1) {
      state.progress = (parsed.progress && typeof parsed.progress === 'object') ? parsed.progress : {}
      state.notes = (parsed.notes && typeof parsed.notes === 'object') ? parsed.notes : {}
      state.favorites = (parsed.favorites && typeof parsed.favorites === 'object') ? parsed.favorites : {}
    }
  } catch (e) {
    console.warn('[hh.learning] 读取本地数据失败', e)
  }
}

function persist() {
  if (import.meta.env.SSR) return
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
  } catch (e) {
    console.warn('[hh.learning] 写入本地数据失败', e)
  }
}

// 客户端：首次调用即加载；之后深度监听自动落盘
if (!import.meta.env.SSR) {
  load()
  watch(state, () => persist(), { deep: true })
}

export interface Stats {
  total: number
  done: number
  learning: number
  favCount: number
  /** 已学 / 总章数，0-100 整数 */
  pct: number
}

export function useLearning() {
  load()

  function getStatus(path: string): ChapterStatus | undefined {
    return state.progress[path]
  }
  /** 传 null 表示取消标记（回到未学） */
  function setStatus(path: string, status: ChapterStatus | null) {
    if (status === null) delete state.progress[path]
    else state.progress[path] = status
  }

  function isFavorite(path: string): boolean {
    return !!state.favorites[path]
  }
  function toggleFavorite(path: string) {
    if (state.favorites[path]) delete state.favorites[path]
    else state.favorites[path] = true
  }

  function getNote(path: string): string {
    return state.notes[path] || ''
  }
  function setNote(path: string, text: string) {
    const t = (text || '').trim()
    if (t) state.notes[path] = text
    else delete state.notes[path]
  }

  function stats(): Stats {
    const total = catalog.length
    let done = 0
    let learning = 0
    for (const k of Object.keys(state.progress)) {
      if (state.progress[k] === 'done') done++
      else if (state.progress[k] === 'learning') learning++
    }
    return {
      total,
      done,
      learning,
      favCount: Object.keys(state.favorites).length,
      pct: total ? Math.round((done / total) * 100) : 0
    }
  }

  /** 导出为可下载的 JSON 字符串 */
  function exportJSON(): string {
    return JSON.stringify(
      {
        version: 1,
        app: 'hardware-handbook',
        exportedAt: new Date().toISOString(),
        progress: state.progress,
        notes: state.notes,
        favorites: state.favorites
      },
      null,
      2
    )
  }

  /** 导入并整体覆盖；返回校验结果 */
  function importJSON(text: string): { ok: boolean; message: string } {
    try {
      const parsed = JSON.parse(text)
      if (!parsed || typeof parsed !== 'object') {
        return { ok: false, message: '导入失败：不是合法的 JSON 对象' }
      }
      if (parsed.version !== 1) {
        return { ok: false, message: '导入失败：版本不兼容（需要 version=1）' }
      }
      state.progress = (parsed.progress && typeof parsed.progress === 'object') ? parsed.progress : {}
      state.notes = (parsed.notes && typeof parsed.notes === 'object') ? parsed.notes : {}
      state.favorites = (parsed.favorites && typeof parsed.favorites === 'object') ? parsed.favorites : {}
      return { ok: true, message: '导入成功，已覆盖当前数据' }
    } catch (e: any) {
      return { ok: false, message: '导入失败：JSON 解析错误（' + (e?.message || e) + '）' }
    }
  }

  function clearAll() {
    state.progress = {}
    state.notes = {}
    state.favorites = {}
  }

  return {
    state,
    catalog,
    catalogTitle,
    catalogLink,
    getStatus,
    setStatus,
    isFavorite,
    toggleFavorite,
    getNote,
    setNote,
    stats,
    exportJSON,
    importJSON,
    clearAll
  }
}
