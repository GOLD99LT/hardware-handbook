import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import Layout from './components/brand/LayoutBrand.vue'
import Logo from './components/brand/Logo.vue'
import EChart from './components/EChart.vue'
import LearningPanel from './components/learning/HomePanel.vue'

import 'katex/dist/katex.min.css'
import './style.css'
import './components/learning/learning.css'

// ---------------------------------------------------------------------------
// 原理图点击放大：全局事件委托（监听 .md-figure img 的点击，弹固定遮罩）
// ---------------------------------------------------------------------------
let zoomInited = false
function setupFigureZoom() {
  if (zoomInited || typeof document === 'undefined') return
  zoomInited = true

  let overlay: HTMLDivElement | null = null
  function open(src: string, alt: string) {
    close()
    overlay = document.createElement('div')
    overlay.className = 'hh-zoom-overlay'
    overlay.innerHTML =
      '<img alt="">' +
      (alt ? '<div class="hh-zoom-cap"></div>' : '')
    const img = overlay.querySelector('img')!
    img.src = src
    if (alt) (overlay.querySelector('.hh-zoom-cap')!.textContent = alt)
    overlay.addEventListener('click', close)
    document.body.appendChild(overlay)
    document.body.style.overflow = 'hidden'
  }
  function close() {
    if (overlay) {
      overlay.remove()
      overlay = null
      document.body.style.overflow = ''
    }
  }
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') close()
  })
  document.addEventListener('click', (e) => {
    const img = (e.target as HTMLElement).closest('.md-figure img') as HTMLImageElement | null
    if (!img) return
    open(img.currentSrc || img.src, img.alt || '')
  })
}

export default {
  extends: DefaultTheme,
  Layout,
  enhanceApp({ app }) {
    app.component('EChart', EChart)
    app.component('Logo', Logo)
    app.component('LearningPanel', LearningPanel)
    setupFigureZoom()
  }
} satisfies Theme
