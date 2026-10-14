// 手册 app 主题：catalog 与学习仓储均来自 content.config（已在其中装配/注册）。
import { createHwTheme } from '@hw/theme'
import { catalog, repository } from '../../../content.config'

export default createHwTheme({ catalog, repository })
