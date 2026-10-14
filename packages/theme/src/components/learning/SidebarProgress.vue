<script setup lang="ts">
// 侧边栏顶部学习进度条：整体百分比 + 已学/在学计数。
import { computed } from 'vue'
import { useLearning } from './store'

const learning = useLearning()
const s = computed(() => learning.stats())
</script>

<template>
  <div class="hh-learning-progress">
    <div class="hh-lp-head">
      <span class="hh-lp-title">学习进度</span>
      <span class="hh-lp-pct">{{ s.pct }}%</span>
    </div>
    <div class="hh-lp-bar"><div class="hh-lp-fill" :style="{ width: s.pct + '%' }"></div></div>
    <div class="hh-lp-count">已学 {{ s.done }} · 在学 {{ s.learning }} · 共 {{ s.total }} 章</div>
  </div>
</template>
