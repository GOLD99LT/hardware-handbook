// @hw/learning —— P1 占位骨架。
// P2 起定义 LearningRepository 接口（getChapter/putChapter/export/import），
// 存储 key 按 appId：hb.v1.<appId>.learning；一次性迁移旧 hh.v1.learning（保留旧 key）。

export const PACKAGE_NAME = '@hw/learning' as const
export const VERSION = '0.1.0' as const

export type ChapterProgress = 'learning' | 'done'

export interface LearningExport {
  schemaVersion: 1
  appId: string
  contentRevision: string
  exportedAt: string
  progress: Record<string, ChapterProgress>
  favorites: Record<string, boolean>
  notes: Record<string, { text: string; updatedAt: string }>
}

export interface LearningRepository {
  getChapter(id: string): Promise<ChapterProgress | undefined>
  putChapter(id: string, progress: ChapterProgress): Promise<void>
  export(): Promise<LearningExport>
  import(json: string, mode: 'merge' | 'replace'): Promise<void>
}
