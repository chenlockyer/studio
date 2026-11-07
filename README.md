# 落地组 · 宇树 G1 落地交付官网

纯静态单页：`index.html` + `assets/`，**没有构建步骤、没有依赖、没有外链 CDN**。
双击 `index.html` 就能看，放到任意静态服务器（Nginx / OSS / GitHub Pages）也一样。

---

## 本地预览

```bash
cd D:/code/unitree-site
python -m http.server 8811
# 打开 http://127.0.0.1:8811/
```

也可以直接双击 `index.html`。两种方式都测过：
- 字体在 `file://` 下能正常加载（已去掉会触发 CORS 报警的 `font` preload）
- 复制按钮在 `file://` 下浏览器禁用剪贴板 API，会自动展开一个可全选的文本框作为回退

---

## 目录

```
index.html                 单页正文（25.8 KB，无内联样式）
assets/css/site.css        全部样式（26 KB；颜色/字号/间距统一走 :root token）
assets/js/site.js          交互增强（5 KB；关掉脚本页面依然完整可用）
assets/fonts/              3 个按页面用字子集化的 woff2（共 257 KB；语料直接取自 index.html，改文案后需重建）
                             smiley-display  标题（得意黑，中文展示体）
                             noto-400/700    正文与数字（包含拉丁与数字字形）
assets/video/              4 段真实现场视频（共 2.27 MB，H.264 / 无音轨 / faststart）
assets/img/poster/         4 张视频封面（与视频首帧严格同帧，不会跳帧）
assets/img/ui/             4 张软件界面截图的 AVIF/WebP/JPG 响应式阶梯
assets/img/wechat-qr.png   微信二维码 720×720（从名片截图裁出，已去掉头像与昵称）
assets/img/og.jpg          社交分享图（1200×675）
assets/favicon.svg         站点图标
```

## 页面结构

| 锚点 | 区块 | 干什么 |
|---|---|---|
| `#top` | 首屏 | 整屏真实现场视频 + 业务定位 + 三个核心数字（7 台 / 3 个客户 / 24 米） |
| `#navi` | 场馆导览 | 展厅里 G1 自主带路的现场视频 + 四步上线流程 + 真机界面截图 |
| `#group` | 多机群控 | 多台 G1 同步执行的现场 + 真实手柄指令表 + 三条安全事实 |
| `#chain` | 动作定制 | 真机跳舞竖版视频 + 从人体数据到真机的四道验证 |
| `#deliver` | 交付流程 | 四步交付 + 交付清单；紧接白底「交付实绩」数字带 |
| `#course` | 师资培训 | 2 天 12 学时规格条 + 七项结业验收 |
| `#faq` | 常见问题 | 10 条真实问答（`<details>`，单开互斥） |
| `#contact` | 联系 | 微信扫码入口 + 四项表单，一键合成一段话复制到剪贴板 |

## 交互

| 动作 | 行为 |
|---|---|
| 点任意「获取方案 / 说清你的场地 / 预约开班」 | 弹微信二维码（原生 `<dialog>`；ESC 或点遮罩关闭） |
| 关闭 JS | 上面的按钮退化成直接打开 `wechat-qr.png`，页面其余部分完整可用 |
| 填完四项点「复制需求」 | 合成一段话写进剪贴板；`file://` 或无剪贴板权限时改为展开可全选的文本框 |
| 常见问题 | `<details>` 单开互斥 |
| 入场动画 | `IntersectionObserver`，`prefers-reduced-motion` 下自动关闭 |
| 视频 | 全部 `muted playsinline loop autoplay preload=metadata`，`prefers-reduced-motion` 下只显示封面 |

## 需要你补的占位

| 位置 | 现在 | 换成什么 |
|---|---|---|
| 页脚 | 没有电话 / 邮箱 / 备案号 | 补真实联系方式与备案号 |
| 微信二维码 | `assets/img/wechat-qr.png`，从 `C:/Users/11051/Pictures/个人信息/微信二维码.png` 裁出 | 换微信号后重跑 `.work/scripts/make_qr.py`（源图丢进同路径即可） |
| 品牌名「落地组」 | 临时 wordmark（`index.html` 内 6 处 + `<title>`/OG） | 定名后全局替换 |
| 客户名 | 「深圳某高校」 | 客户同意后换真名，否则保留匿名但具体的写法 |
| 交付范围 | 全站写「全球交付」 | 如果只做国内或只做珠三角，把 `.wm-sub` / FAQ 最后一条 / 页脚「现场」列改回去 |
| 案例数据 | 7 台 / 3 客户 / 3 套 / 24 米 | 有新交付时同步更新首屏与「交付实绩」两处 |

## 素材来源

视频全部来自你自己的实拍素材 `D:/my_media/video/unitree_g1`，没有一张是网上找的：

| 文件 | 来源 | 区间 |
|---|---|---|
| `tour-live.mp4` | `导览/导览投入使用.mp4` | 28.0s 起 6.1s |
| `group-sync.mp4`（首屏） | `群控/群控.mp4` | 29.5s 起 9.0s |
| `group-ops.mp4`（群控区块） | `群控/群控.mp4` | 44.0s 起 8.0s |
| `dance-live.mp4` | `江南.mp4` | 6.0s 起 5.0s |

界面截图来自 `D:/code/g1_navi_body`、`D:/code/g1_group_control` 两个产品的真实运行界面。
原始 PNG 已归档在 `.work/source-img/`。

**没有编造客户、证言与数据。** 页面上的每个数字都对应真实交付现场。
