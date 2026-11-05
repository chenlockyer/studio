# studio · 产品官网（内部预览版）

宇树 G1 / GO2 二次开发与落地交付工作室的官网。纯静态：`index.html` + `assets/`，无构建步骤。

预览地址：https://chenlockyer.github.io/studio/

> ⚠️ 这是**内部预览版**，`robots.txt` 与页面 meta 均为 `noindex`，不进入搜索引擎。
> 正式对外发布需要：独立域名 + 公司/个体主体 + ICP 备案 + 公安联网备案。

## 本地预览

```bash
cd work/studio-deploy
python -m http.server 8811
# http://127.0.0.1:8811/
```

## 目录

```
index.html              单页：首屏 → 三种现场 → 怎么交付 → 要几台（适配器）→ 证据 → 培训 → 问答 → 联系
assets/css/site.css     全部样式（颜色、字号、栅格、动效都是 token）
assets/js/site.js       动效与交互（首屏换帧、交付步骤切换、场地适配器、FAQ、表单复制）
assets/fonts/           拉丁 Epilogue + 中文 Noto Sans SC 子集（各约 65KB）
assets/img/             真机实拍帧 + 导览方案页截图
assets/video/           两段现场视频（巡场行走 12s、舞蹈 8s），H.264、无音轨
```

## 上线前还需要替换的占位

| 位置 | 现在 | 换成什么 |
|---|---|---|
| 联系区二维码 | 灰色方块「上线前替换」 | 真实微信二维码图片 |
| 群控界面（现场卡 3、案例 2） | 「截图待补」 | 群控软件真实截图 |
| 品牌名 | 临时 wordmark「落地组」 | 定名后全局替换（`index.html` 4 处） |
| 页脚 | 「本页为内部预览版」 | 备案号 + 主体名称 |

素材来自真实交付现场与真实界面截图，未编造客户、证言与数据。
