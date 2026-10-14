<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { useData } from 'vitepress'

const props = defineProps<{ option: Record<string, any> }>()

const el = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null
const { isDark } = useData()

function render() {
  if (!el.value) return
  if (chart) {
    chart.dispose()
    chart = null
  }
  try {
    chart = echarts.init(el.value, isDark.value ? 'dark' : undefined)
    chart.setOption(props.option)
  } catch (e) {
    // 图表渲染失败不应拖垮整页；错误上抛控制台便于排查
    console.error('[EChart] render failed', e)
  }
}

function resize() {
  chart?.resize()
}

onMounted(() => {
  render()
  window.addEventListener('resize', resize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resize)
  chart?.dispose()
  chart = null
})

// 深浅色切换后重绘
watch(isDark, () => render())
</script>

<template>
  <div ref="el" class="hh-chart"></div>
</template>

<style scoped>
.hh-chart {
  width: 100%;
  height: 360px;
  margin: 4px 0;
}
@media (max-width: 768px) {
  .hh-chart {
    height: 300px;
  }
}
</style>
