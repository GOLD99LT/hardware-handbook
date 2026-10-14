// 薄 config：通用规则全部来自 @hw/shared-config，站点数据来自 content.config。
// sidebar 为预构建生成物（gen:sidebar）；默认根 base，可用 VP_BASE 环境变量覆盖
// （如部署到子路径：VP_BASE='/<app>/' pnpm docs:build）。
import { defineHwConfig } from '@hw/shared-config'
import sidebar from './sidebar.generated.mjs'
import {
  APP_ID,
  TITLE,
  DESCRIPTION,
  FAVICON,
  PART_REGISTRY,
  NAV,
  SOCIAL_LINKS
} from '../../content.config'

export default defineHwConfig({
  appId: APP_ID,
  title: TITLE,
  description: DESCRIPTION,
  base: '/',
  nav: NAV,
  sidebar,
  partRegistry: PART_REGISTRY,
  socialLinks: SOCIAL_LINKS,
  favicon: FAVICON
})
