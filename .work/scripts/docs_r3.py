import io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")

# ---------------- README ----------------
r=open("README.md",encoding="utf-8").read()
r=r.replace("# 落地组 · 宇树 G1 落地交付官网","# 宇树机器人实验室 · 宇树 G1 落地交付官网",1)

# 本地预览段：补上线上地址
r=r.replace("""---

## 本地预览""","""**线上地址：<https://chenlockyer.github.io/studio/>**（GitHub Pages，推 `main` 即发布）

---

## 本地预览""",1)

# 目录树：补 wechat-qr 已有的说明不变，补 robots.txt / 404.html / DEPLOY.md
r=r.replace("assets/favicon.svg         站点图标",
"""assets/favicon.svg         站点图标
robots.txt                 允许全站抓取
404.html                   404 页（GitHub Pages 项目站在 /studio/ 子路径下，用绝对地址回首页）
DEPLOY.md                  三条正式托管路线与各自的前置条件
.nojekyll                  关掉 GitHub Pages 的 Jekyll 处理""",1)

# 页面结构表后面补「上线」一节
r=r.replace("""## 交互""","""## 上线（GitHub Pages）

线上仓库：`github.com/chenlockyer/studio`，Pages 从 `main` 分支根目录发布，站点在 `/studio/` 子路径下。

```bash
cd D:/code/unitree-site
git add -A && git commit -m "改动说明"
# 本地分支叫 master，远端叫 main，历史不相关 → 用 commit-tree 造一个以 origin/main 为父的快进提交
tree=$(git rev-parse "master^{tree}")
new=$(git commit-tree $tree -p origin/main -F <(echo "改动说明"))
git update-ref refs/heads/deploy-gh $new
git push origin deploy-gh:main
```

推完约 10–60 秒 GitHub Pages 自动重建，刷新 <https://chenlockyer.github.io/studio/> 即见新版。
**改文案后必须重建字体子集**（`python .work/scripts/fonts_v4.py`），否则新字会回退到系统字体——这个 bug 不报错，只能肉眼看出（「绩」字就是这么漏的）。

## 交互""",1)

open("README.md","w",encoding="utf-8").write(r)
print("README 已更新")

# ---------------- REPORT ----------------
p=open("REPORT.md",encoding="utf-8").read()
p=p.replace("# 建站报告 · 落地组官网（v3 重构）","# 建站报告 · 宇树机器人实验室官网（v3 重构）",1)

add = """
## 10 · 第三轮修改（改名 / 只留微信 / 上线）

### 10.1 名字：落地组 → 宇树机器人实验室

改名不是全局替换就完事——站名同时出现在 6 个地方：`<title>`、`og:title`、页头 `.wm`、页脚 `.foot-name`、微信弹层的 `.wx-k`、二维码 `alt`。
**改名会改字符集**，所以改完必须重建字体子集（见 8.1 的教训）。本轮重建后 3 个字体共 252.9 KB。

### 10.2 删掉表单，只留微信

原来是「填四个字段 → 一键复制成一段话 → 自己粘到微信」。实际使用里这一跳是多余的：客户最终一定是在微信里谈，而且场地照片、尺寸、点位数量都得发图。
改成：

- 联系区直接放二维码大图（`.contact-qr`），配一句「扫码加微信，直接发场地照片和尺寸」
- 页头「获取方案」、首屏「说清你的场地」、培训「预约开班」、问答侧栏四处按钮，点开同一个原生 `<dialog>` 弹层展示二维码
- **无 JS 时**这些按钮的 `href` 直接指向二维码 PNG，退化成「点开看图」，不会变成死链
- 手机上扫不了自己屏幕 → 窄屏下多一行「保存图片，微信『扫一扫 → 相册』识别」，带 `download` 属性

删掉表单后顺带清掉 CSS 18 条规则、JS 43 行，体积 -2.6 KB。

### 10.3 视频长宽比被改坏（本轮最严重的 bug）

现象：手机上「让 G1 自己带路讲解」等三个区块的视频，画面被横向裁掉约 72%，主体拉到变形，很丑。桌面端却「看着正常」。

根因链：

1. HTML 里写着 `<video width="1280" height="720">`。这两个属性是**表现性提示**，等价于 CSS `height: 720px`。
2. CSS 只写了 `width: 100%` 和 `aspect-ratio: 16 / 9`，**没写 `height: auto`**。
3. 因为高度已经被属性钉死，`aspect-ratio` 直接不生效。
4. 于是视频被塞进 `358 × 720`（比例 0.497）的框里，再 `object-fit: cover` → 横向裁掉 72%。

桌面端之所以看不出：桌面容器宽度恰好 ≈1280，被钉死的 720 高度正好等于 16:9，纯属巧合；一换到手机上就露馅。

修法：给 `.media-wide video` 与 `.chain-video > video` 各加一行 `height: auto`。修后实测渲染框 navi 358×201、group 358×201、chain 240×427，与源视频比例完全一致。

**教训**：`width`/`height` 属性与 `aspect-ratio` 同时存在时，属性会赢。要么把属性删掉，要么必须补 `height: auto`。

### 10.4 手机首屏不再是裁切

首屏用 16:9 素材铺满整屏（`object-fit: cover`）。桌面上只裁掉上下 11%，没问题；但 390×793 的竖框里，横向只剩 28% 的画面——糊、且看不出是什么。

改成：**手机上首屏是整块 16:9 视频带 + 下方文字**。视频一像素都不裁，文字落在实色底上，对比度反而更好。桌面端维持整屏视频不变。

### 10.5 上线

GitHub Pages，仓库 `chenlockyer/studio`，从 `main` 根目录发布，站点在 `/studio/` 子路径。

本地分支叫 `master`、远端叫 `main`，两边历史不相关（远端是旧的「预览版 v1」）。直接推会被拒，用 `commit-tree` 以 `origin/main` 为父造一个「树和 master 完全相同」的提交，再推就变成快进合并，远端历史不断。

为子路径部署补的：`<link rel="canonical">`、`og:url`、`og:image` 改绝对地址（`https://chenlockyer.github.io/studio/assets/img/og.jpg`）、`404.html` 里回首页的链接用绝对路径、加 `.nojekyll`。

线上实测：HTML / CSS / JS / 3 个 woff2 / 二维码 PNG / 4 段 mp4 / favicon 全部 200，首屏与各区块渲染与本地一致。
"""
p=p.replace("## 9 · 还差你补的", add.strip()+"\n\n## 9 · 还差你补的",1)
open("REPORT.md","w",encoding="utf-8").write(p)
print("REPORT 已更新（新增第 10 章，置于第 9 章之前）")
