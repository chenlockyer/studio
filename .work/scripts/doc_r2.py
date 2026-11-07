import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
p="README.md"; s=open(p,encoding="utf-8").read()

s=s.replace("assets/fonts/              3 个按页面用字子集化的 woff2（共 265 KB）",
            "assets/fonts/              3 个按页面用字子集化的 woff2（共 257 KB；语料直接取自 index.html，改文案后需重建）")
s=s.replace("assets/img/og.jpg          社交分享图（1200×675）",
            "assets/img/wechat-qr.png   微信二维码 720×720（从名片截图裁出，已去掉头像与昵称）\nassets/img/og.jpg          社交分享图（1200×675）")
s=s.replace("| `#contact` | 联系 | 四项表单，一键合成一段话复制到剪贴板 |",
            "| `#contact` | 联系 | 微信扫码入口 + 四项表单，一键合成一段话复制到剪贴板 |")

s=s.replace("""| 页脚 | 没有电话 / 邮箱 / 备案号 | 补真实联系方式与备案号 |""",
            """| 页脚 | 没有电话 / 邮箱 / 备案号 | 补真实联系方式与备案号 |
| 微信二维码 | `assets/img/wechat-qr.png`，从 `C:/Users/11051/Pictures/个人信息/微信二维码.png` 裁出 | 换微信号后重跑 `.work/scripts/make_qr.py`（源图丢进同路径即可） |""")

s=s.replace("""| 客户名 | 「深圳某高校」 | 客户同意后换真名，否则保留匿名但具体的写法 |""",
            """| 客户名 | 「深圳某高校」 | 客户同意后换真名，否则保留匿名但具体的写法 |
| 交付范围 | 全站写「全球交付」 | 如果只做国内或只做珠三角，把 `.wm-sub` / FAQ 最后一条 / 页脚「现场」列改回去 |""")

# 交互说明补一节
s=s.replace("""## 需要你补的占位""",
"""## 交互

| 动作 | 行为 |
|---|---|
| 点任意「获取方案 / 说清你的场地 / 预约开班」 | 弹微信二维码（原生 `<dialog>`；ESC 或点遮罩关闭） |
| 关闭 JS | 上面的按钮退化成直接打开 `wechat-qr.png`，页面其余部分完整可用 |
| 填完四项点「复制需求」 | 合成一段话写进剪贴板；`file://` 或无剪贴板权限时改为展开可全选的文本框 |
| 常见问题 | `<details>` 单开互斥 |
| 入场动画 | `IntersectionObserver`，`prefers-reduced-motion` 下自动关闭 |
| 视频 | 全部 `muted playsinline loop autoplay preload=metadata`，`prefers-reduced-motion` 下只显示封面 |

## 需要你补的占位""")
open(p,"w",encoding="utf-8").write(s)
print("README 已更新")
