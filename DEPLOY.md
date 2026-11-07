# 上线部署

这份文档记录**真实做过的事**和**还差什么**，不是通用教程。

---

## 现状（截至本轮）

| 项 | 状态 |
|---|---|
| 站点代码 | 完成，`inspect` 0 FAIL / 0 WARN，`lint` 0/0，冒烟全绿 |
| 干净产物 | `dist/`，40 个文件 4.05 MB（`python .work/scripts/build_dist.py` 生成） |
| 本地局域网 | `http://10.161.204.47:8811/`（WLAN，同一 Wi-Fi 下手机可直接看） |
| 公网临时预览 | `https://dpi-thermal-pvc-programming.trycloudflare.com`（**本机开着才活，机器睡了就断**） |
| 正式公网 | **未完成**，卡在域名与托管账号 |

---

## 一个必须先讲清楚的事实：大陆访问

这台机器在深圳（大陆网络）。我实测了各家静态托管的可达性：

| 托管 | 测试域名 | 结果 |
|---|---|---|
| Cloudflare Workers | `*.workers.dev` | **不通**（DNS 污染，21 秒超时） |
| Vercel | `vercel.app` | **不通**（21 秒超时） |
| Cloudflare Pages | `dash.pages.dev` | 通 |
| Netlify | `app.netlify.com` | 通（80ms） |
| Surge | `surge.sh` | 通（521ms） |
| Render | `onrender.com` | 通（330ms） |
| GitHub Pages | `github.io` | 通（252ms） |
| Gitee | `gitee.com` | 通（56ms） |
| 阿里云 OSS | `oss.aliyuncs.com` | 通（47ms） |
| 腾讯云 COS | `cos.ap-guangzhou.myqcloud.com` | 通（44ms） |

**结论一**：`*.workers.dev` 和 `*.vercel.app` 不能直接给大陆客户用。
**结论二**：Cloudflare 本身能连（`www.cloudflare.com` 247ms 通，`api.cloudflare.com` 也能调通——部署就是走它完成的）。**卡住的是 `workers.dev` 这个免费子域，不是 Cloudflare。** 绑上自己的域名就绕开了。

我已经把站部署到了 Cloudflare Workers 的临时账户：
`https://unitree-lab-site.sweet-sagittarius.workers.dev`

部署是成功的（39 个文件全部上传，Worker 和路由都建好了）。但上面那个地址在大陆打不开——所以我没法说它是"上线"。

---

## 三条正式路线，按推荐顺序

### A. 自有域名 + Cloudflare Workers（推荐）

**花钱**：域名 ¥30–80/年，托管 ¥0。不需要备案（服务器不在大陆）。
**大陆访问**：能开，速度一般但可接受（Cloudflare 香港/新加坡节点）。绑定自定义域名后不受 `workers.dev` 污染影响。

你要做的：
1. 买一个域名。阿里云 / 腾讯云 / Cloudflare Registrar / Namecheap 都行。
   建议 `.com`；`.cn` 要实名，流程长一点。
2. 把域名添加到 Cloudflare（免费套餐），按提示把 NS 记录改到 Cloudflare 分配的两个地址。
3. 告诉我域名，我做完剩下的。

我要做的：
```bash
npx wrangler login          # 浏览器里点一次授权，约 30 秒
# 在 wrangler.jsonc 里加 routes 绑定自定义域名后
python .work/scripts/build_dist.py
npx wrangler deploy
```

同时改这三处（绑域名后才成立）：
- `index.html` 的 `og:image` 从相对路径 `assets/img/og.jpg` 改成绝对 URL
- 加 `<link rel="canonical" href="https://你的域名/">`
- 如需统计，加一段访问统计脚本

---

### B. 国内云静态托管（阿里云 OSS / 腾讯云 COS）

**花钱**：对象存储几块钱/月 + 域名。**但自定义域名必须 ICP 备案**，备案要 3–20 个工作日，还要主体资质。
**大陆访问**：最快（国内 CDN）。

唯一的问题是备案周期。如果这是个要长期做的生意，早晚要备；如果只是想先把页面发出去给客户看，先用 A。

注意：用 OSS/COS 的**默认域名**访问 HTML 会被强制下载（`Content-Disposition: attachment`），不能当网站用。必须绑自定义域名。

---

### C. 自有服务器（香港 / 新加坡 VPS）

**花钱**：VPS ¥20–60/月 + 域名。不需要备案。
**大陆访问**：取决于线路，CN2 线路好，普通线路一般。

```bash
# 打包
python .work/scripts/build_dist.py
Compress-Archive -Path dist\* -DestinationPath site.zip

# 上传（有 root SSH 的前提下）
scp -r dist/* root@你的服务器:/var/www/unitree-lab/
```
服务器上配 Nginx 即可。`_headers` 是 Cloudflare 专有格式，Nginx 要另写：

```nginx
server {
    listen 443 ssl http2;
    server_name 你的域名;

    root /var/www/unitree-lab;
    index index.html;

    location /assets/ { expires 7d; add_header Cache-Control "public"; }
    location /assets/fonts/ { expires 30d; add_header Cache-Control "public, immutable"; }
    location / { try_files $uri $uri/ /404.html; }

    add_header X-Content-Type-Options nosniff;
    add_header Referrer-Policy strict-origin-when-cross-origin;

    gzip on;
    gzip_types text/css application/javascript image/svg+xml;
}
```

---

## 部署相关的文件

| 文件 | 作用 | 只在哪些平台生效 |
|---|---|---|
| `dist/` | 唯一该上传的目录（由脚本生成，已在 .gitignore） | 全部 |
| `wrangler.jsonc` | Cloudflare Workers 配置（静态资源目录 `./dist`、404 处理） | Cloudflare |
| `_headers` | 缓存策略 + 安全头 | Cloudflare Pages / Workers |
| `robots.txt` | 允许全站抓取 | 全部 |
| `404.html` | 404 页，与站点同一套视觉 | 全部 |

`dist/` 里没有的东西（故意的）：`.work/`、`.taste-skill/`、`.git/`、`README.md`、`REPORT.md`、`DEPLOY.md`、所有脚本。这些不进产物。

---

## 一改内容就要重新跑的两件事

```bash
# 1) 改了文案 → 必须重建字体子集，否则新加的字会悄悄回退成系统字体
python .work/scripts/fonts_v4.py
python .work/scripts/r3_glyphcheck.py     # 复核：三个字体对页面用字缺 0

# 2) 改了任何东西 → 重新验收 + 重新打包
node "C:\Users\11051\.dsh\skills\design-taste-frontend\scripts\inspect.mjs" index.html
node "C:\Users\11051\.dsh\skills\design-taste-frontend\scripts\lint.mjs" index.html
node .work/scripts/smoke.mjs
python .work/scripts/build_dist.py
```

第一条不是可选项。「交付实绩」的「绩」就是这么丢的：文案改了，字符表没跟上，字体里没有那个字，浏览器回退到系统字体——页面上看起来只是"这个字有点怪"，但根因在字体子集。
