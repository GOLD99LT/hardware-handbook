<script setup>
import DefaultTheme from 'vitepress/theme'
import Logo from './Logo.vue'
import SidebarProgress from '../learning/SidebarProgress.vue'
import ChapterLearning from '../learning/ChapterLearning.vue'
</script>

<template>
  <DefaultTheme.Layout>
    <!-- 导航栏标题前放 ~24px 品牌标识；其余插槽/功能完全沿用默认主题 -->
    <template #nav-bar-title-before>
      <Logo class="nav-brand" :width="32" :height="24" aria-hidden="true" />
    </template>

    <!-- 侧边栏顶部：整体学习进度（client-only，不影响 SSG/SEO） -->
    <template #sidebar-nav-before>
      <ClientOnly>
        <SidebarProgress />
      </ClientOnly>
    </template>

    <!-- 章末：已学/在学、收藏、我的笔记（首页不渲染） -->
    <template #doc-footer-before>
      <ClientOnly>
        <ChapterLearning />
      </ClientOnly>
    </template>
  </DefaultTheme.Layout>
</template>

<style>
.nav-brand {
  flex: none;
  margin-right: 2px;
}
</style>
