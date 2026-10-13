// hw-manifest CLI —— 由 SUMMARY.md + frontmatter + 磁盘扫描生成 content-manifest.json。
// 用法：node src/cli.ts [--src <docs目录>] [--out <输出JSON>] [--appId <id>]
// 默认：--src docs  --out .generated/content-manifest.json  --appId handbook

import * as fs from 'node:fs'
import * as path from 'node:path'
import { buildManifest, countSvg } from './index.ts'

function arg(name: string, fallback: string): string {
  const i = process.argv.indexOf(`--${name}`)
  return i >= 0 && i + 1 < process.argv.length ? process.argv[i + 1] : fallback
}

const src = arg('src', 'docs')
const out = arg('out', path.join('.generated', 'content-manifest.json'))
const appId = arg('appId', 'handbook')

const manifest = buildManifest(src, appId)
const imageTotal = manifest.docs.reduce((a, d) => a + d.images.length, 0)

fs.mkdirSync(path.dirname(out), { recursive: true })
fs.writeFileSync(out, JSON.stringify(manifest, null, 2) + '\n', 'utf8')

console.log(
  `manifest 已生成: ${manifest.docs.length} 章 / ${imageTotal} 处图片引用 / ` +
    `svg=${countSvg(src)} / revision=${manifest.revision} -> ${out}`,
)
