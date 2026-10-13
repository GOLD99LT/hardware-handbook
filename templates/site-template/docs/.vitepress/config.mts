import { defineConfig } from 'vitepress'

// 最小 VitePress 配置（P1：默认主题即可）。
// 未来真正的通用规则（五类容器/KaTeX/ECharts 等）由 @hw/shared-config 的
// defineHwConfig 提供，本模板仅验证「空内容也能 dev/build/preview」。
export default defineConfig({
  title: 'Site Template',
  description: '硬件学习生态 · 最小 VitePress 脚手架（P1）',
  themeConfig: {
    nav: [{ text: '示例', link: '/example/hello' }],
    sidebar: [
      {
        text: '示例章',
        items: [{ text: 'Hello · 示例章', link: '/example/hello' }],
      },
    ],
  },
})
