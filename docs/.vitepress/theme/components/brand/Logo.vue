<template>
  <svg
    class="brand-mark"
    :width="width"
    :height="height"
    viewBox="0 0 64 64"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-label="硬件工程师手册"
  >
    <!-- 运放三角形：左竖直边两个输入，右尖点输出 -->
    <path class="body" d="M16 12 L16 52 L52 32 Z"/>
    <!-- 同相 / 反相输入引线 -->
    <path d="M6 21 H16"/>
    <path d="M6 43 H16"/>
    <!-- 输出引线 + 正弦信号波 -->
    <path d="M52 32 H57"/>
    <path d="M57 32 q1.5 -4.4 3 0 t3 0"/>
    <!-- + / - 输入极性 -->
    <path d="M20.8 24 H24.6"/>
    <path d="M22.7 22.1 V25.9"/>
    <path d="M20.8 40 H24.6"/>
  </svg>
</template>

<script setup>
defineProps({
  width: { type: [Number, String], default: 48 },
  height: { type: [Number, String], default: 36 },
})
</script>

<style scoped>
/* 浅底：沉稳工程蓝；深底（VitePress html.dark）提亮 */
.brand-mark {
  color: #1a4f8b;
}
.brand-mark path {
  stroke: currentColor;
  stroke-width: 2.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.brand-mark .body {
  fill: currentColor;
  fill-opacity: 0.08;
}
.dark .brand-mark {
  color: #7aa8ff;
}
</style>
