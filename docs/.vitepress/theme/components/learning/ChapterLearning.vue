<script setup lang="ts">
// 章末学习工具：已学/在学切换、收藏、我的笔记（按章自动保存到 localStorage）。
// 仅在内容页渲染（首页 index.md 不渲染）。
import { computed, ref, watch } from 'vue'
import { useData } from 'vitepress'
import { useLearning } from './store'

const { page } = useData()
const learning = useLearning()

const currentPath = computed(() => page.value.relativePath)
const isHome = computed(() => currentPath.value === 'index.md' || page.value.frontmatter?.layout === 'home')

const status = computed(() => learning.getStatus(currentPath.value))
const fav = computed(() => learning.isFavorite(currentPath.value))
const note = ref(learning.getNote(currentPath.value))
const savedHint = ref('')

// SPA 切章时刷新笔记内容
watch(currentPath, (p) => {
  note.value = learning.getNote(p)
  savedHint.value = ''
})

function setStatus(s: 'done' | 'learning') {
  // 再点同一状态 -> 取消（回到未学）
  learning.setStatus(currentPath.value, status.value === s ? null : s)
}
function toggleFav() {
  learning.toggleFavorite(currentPath.value)
}

let saveTimer: any = null
function onNoteInput() {
  learning.setNote(currentPath.value, note.value)
  savedHint.value = '已保存'
  clearTimeout(saveTimer)
  saveTimer = setTimeout(() => (savedHint.value = ''), 1200)
}
</script>

<template>
  <div v-if="!isHome" class="hh-learning-chapter">
    <div class="hh-learning-status">
      <button
        type="button"
        class="hh-ls-btn"
        :class="{ active: status === 'learning' }"
        @click="setStatus('learning')"
      >在学</button>
      <button
        type="button"
        class="hh-ls-btn"
        :class="{ active: status === 'done' }"
        @click="setStatus('done')"
      >已学</button>
      <button
        type="button"
        class="hh-ls-btn hh-ls-fav"
        :class="{ active: fav }"
        @click="toggleFav"
      >
      <svg class="hh-ls-star" viewBox="0 0 24 24" :fill="fav ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8L3.5 9.7l5.9-.9L12 3.5z"/></svg>
      {{ fav ? '已收藏' : '收藏本章' }}</button>
    </div>

    <div class="hh-learning-notes">
      <div class="hh-ln-head">
        <span class="hh-ln-title">我的笔记</span>
        <span class="hh-ln-hint">{{ savedHint || '自动保存到本地浏览器' }}</span>
      </div>
      <textarea
        v-model="note"
        rows="5"
        placeholder="按本章记录要点、坑、待办…（仅保存在你当前浏览器）"
        @input="onNoteInput"
      ></textarea>
    </div>
  </div>
</template>
