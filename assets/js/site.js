/* ================================================================
   落地组 · site.js
   这一层全部是增强：关掉脚本，页面仍然完整可读。
   ================================================================ */
(() => {
  'use strict';
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const calm = () => reduce.matches;

  /* ---------------- 1 · 分区入场：标题 → 正文 → 图，各自错开 ---------------- */
  // 一串稳定的选择器：区块里每个“部件”单独上来，而不是整块一起淡。
  // 顺序即阅读顺序，所以同一个区块里的 --i 天然形成 0,1,2 的错开。
  const PARTS = [
    '.sec-head .side', '.sec-head .sec-title', '.board', '.evidence .shot',
    '.axis-title', '.tile-head', '.tile-photo', '.tile-fig', '.tile-list',
    '.tile-film', '.tile-say', '.pad', '.cmd-all',
    '.stair-title', '.stair-lead', '.step', '.handover',
    '.pb-title', '.figs', '.pb-note',
    '.course-head .sec-title', '.course-lead', '.course-photo', '.route-tile',
    '.goals-head', '.goals-line li', '.course-cta',
    '.roll-title', '.roll-col', '.faq .roll-title', '.faq-cols p',
    '.contact-say', '.contact-pic', '.contact-title', '.contact-sub', '.ask',
  ];
  const targets = [];
  for (const sel of PARTS) {
    $$(sel).forEach((el, i) => {
      el.classList.add('is-stagger');
      el.style.setProperty('--i', String(Math.min(i, 4)));
      targets.push(el);
    });
  }
  const reveal = (el) => el.classList.add('is-in');
  if ('IntersectionObserver' in window && !calm()) {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        reveal(e.target);
        io.unobserve(e.target);
      }
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    targets.forEach((el) => io.observe(el));
    // 兜底：任何一直没进入观察范围的块，也不能永远看不见
    addEventListener('load', () => {
      setTimeout(() => { targets.forEach(reveal); io.disconnect(); }, 2600);
    });
  } else {
    targets.forEach(reveal);
  }

  /* ---------------- 2 · 首屏标题的蒙版上行（只在 HTML 里写好了行才动） ---------------- */
  const heroLines = $$('.mast-title h1 .mask > span');
  if (heroLines.length && !calm()) {
    heroLines.forEach((s, i) => {
      s.style.animationDelay = `${i * 90}ms`;
    });
  }

  /* ---------------- 3 · 导览：那一板四行，点开一行 ---------------- */
  const rows = $$('.board .row');
  if (rows.length) {
    const open = (i) => {
      rows.forEach((r, k) => {
        const on = k === i;
        r.classList.toggle('is-open', on);
        r.setAttribute('aria-expanded', on ? 'true' : 'false');
      });
    };
    rows.forEach((r, i) => {
      r.addEventListener('click', () => open(i));
      r.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(i); }
        else if (e.key === 'ArrowDown') { e.preventDefault(); open((i + 1) % rows.length); rows[(i + 1) % rows.length].focus(); }
        else if (e.key === 'ArrowUp') { e.preventDefault(); open((i - 1 + rows.length) % rows.length); rows[(i - 1 + rows.length) % rows.length].focus(); }
      });
    });
  }

  /* ---------------- 4 · 群控：唯一可以动手的东西 —— 真按键组合 ---------------- */
  // 这张表就是界面里那张命令表（按键序列、持续、活动空间），不是编的
  const COMMANDS = [
    { seq: 'R1+B', name: '舞蹈模式', trigger: '0.5 秒', dur: '3.0 秒', space: '原地' },
    { seq: 'R1+↑', name: '查尔斯顿舞 1', trigger: '0.5 秒', dur: '0.5 秒', space: '向前 1 米' },
    { seq: 'R1+←', name: '查尔斯顿舞 2', trigger: '0.5 秒', dur: '0.5 秒', space: '前 1 米，左 1 米' },
    { seq: 'R1+→', name: '查尔斯顿舞 3', trigger: '0.5 秒', dur: '0.5 秒', space: '向前 3 米' },
    { seq: 'R2+↑', name: '截拳道', trigger: '0.5 秒', dur: '0.5 秒', space: '3 米见方' },
    { seq: 'R2+←', name: '扭扭舞', trigger: '0.5 秒', dur: '0.5 秒', space: '3 米见方' },
    { seq: 'R1+Select', name: '功夫', trigger: '0.5 秒', dur: '0.5 秒', space: '向前 5 米，仅 U2' },
    { seq: 'R1+↓', name: '机械舞 3', trigger: '0.5 秒', dur: '0.5 秒', space: '3 米见方，仅 U2' },
    { seq: 'R2+↓', name: '格斗', trigger: '0.5 秒', dur: '0.5 秒', space: '向前 5 米，仅 U2' },
    { seq: 'L1+X', name: '机械舞 1', trigger: '0.5 秒', dur: '0.5 秒', space: '左 2 米，右 2 米，仅 U2' },
    { seq: 'L1+Y', name: '机械舞 4', trigger: '0.5 秒', dur: '0.5 秒', space: '前 6 米，右 3 米，仅 U2' },
  ];
  const padEl = document.getElementById('pad');
  if (padEl) {
    const keys = $$('.key', padEl);
    const seqEl = document.getElementById('pad-seq');
    const nameEl = document.getElementById('pad-name');
    const metaEl = document.getElementById('pad-meta');
    const hintEl = document.getElementById('pad-hint');
    const slots = ['R1', 'B'];

    const paint = () => {
      keys.forEach((k) => {
        const slot = Number(k.dataset.slot);
        const on = slots[slot] === k.dataset.val;
        k.classList.toggle('is-on', on);
        k.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
    };

    const show = () => {
      const seq = `${slots[0]}+${slots[1]}`;
      const hit = COMMANDS.find((c) => c.seq === seq);
      if (seqEl) seqEl.textContent = seq;
      if (hit) {
        if (nameEl) nameEl.textContent = hit.name;
        if (metaEl) metaEl.textContent = `触发 ${hit.trigger} · 持续 ${hit.dur} · ${hit.space}`;
        if (hintEl) hintEl.textContent = '这条命令在表里。点执行前，还要先勾选机器、再把它排进队列。';
        padEl.classList.remove('is-miss');
      } else {
        if (nameEl) nameEl.textContent = '这条组合不在表里';
        if (metaEl) metaEl.textContent = '换一个肩键或者换一个字母键';
        if (hintEl) hintEl.textContent = '凑不出来的组合，说明这条命令没有：命令是用真手柄按键一条条录进去的。';
        padEl.classList.add('is-miss');
      }
      if (!calm() && seqEl && seqEl.animate) {
        seqEl.animate(
          [{ opacity: 0.3, transform: 'translateY(5px)' }, { opacity: 1, transform: 'none' }],
          { duration: 220, easing: 'cubic-bezier(0.22,1,0.36,1)' }
        );
      }
    };

    keys.forEach((k) => {
      k.addEventListener('click', () => {
        slots[Number(k.dataset.slot)] = k.dataset.val;
        paint();
        show();
      });
    });
    paint();
    show();
  }

  /* ---------------- 5 · 会动的画面：舞蹈片段进视口才播，离开就停 ---------------- */
  const clip = document.querySelector('.tile-film video');
  if (clip) {
    if (calm()) {
      clip.removeAttribute('autoplay');
    } else if ('IntersectionObserver' in window) {
      const vio = new IntersectionObserver(([e]) => {
        if (e.isIntersecting) clip.play?.().catch(() => {});
        else clip.pause?.();
      }, { threshold: 0.25 });
      vio.observe(clip);
    } else {
      clip.play?.().catch(() => {});
    }
  }

  /* ---------------- 6 · 表格里的数字：滚到就数一遍（只数一次） ---------------- */
  const counters = $$('[data-count]');
  if (counters.length && 'IntersectionObserver' in window && !calm()) {
    const cio = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        const el = e.target;
        const target = Number(el.dataset.count);
        const t0 = performance.now();
        const dur = 720;
        const tick = (now) => {
          const k = Math.min(1, (now - t0) / dur);
          const eased = 1 - Math.pow(1 - k, 3);
          el.textContent = String(Math.round(target * eased));
          if (k < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
        cio.unobserve(el);
      }
    }, { threshold: 0.5 });
    counters.forEach((c) => { c.textContent = '0'; cio.observe(c); });
  }

  /* ---------------- 7 · 表单：复制成一段话，不做假提交 ---------------- */
  const form = document.getElementById('ask-form');
  const hint = document.getElementById('ask-hint');
  if (form) {
    const DEFAULT_HINT = hint ? hint.textContent : '';
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const val = (k) => (data.get(k) || '').toString().trim();
      const brief = [
        `称呼：${val('who') || '（待填）'}`,
        `场地：${val('venue')}`,
        `时间：${val('when')}`,
        `联系：${val('contact') || '（待填）'}`,
        '（从官网发的，想先要一份初步排法）',
      ].join('\n');
      try {
        await navigator.clipboard.writeText(brief);
        if (hint) hint.textContent = `已复制到剪贴板：${brief.replace(/\n/g, ' · ')}`;
      } catch {
        if (hint) hint.textContent = `复制没有成功，请手动复制这段：${brief.replace(/\n/g, ' · ')}`;
      }
    });
    form.addEventListener('reset', () => { if (hint) hint.textContent = DEFAULT_HINT; });
  }

  /* ---------------- 8 · 控件的按下反馈 ---------------- */
  $$('.btn, .key, .row, .quiet-link').forEach((el) => {
    el.addEventListener('pointerdown', () => el.classList.add('is-press'));
    el.addEventListener('pointerup', () => el.classList.remove('is-press'));
    el.addEventListener('pointercancel', () => el.classList.remove('is-press'));
    el.addEventListener('pointerleave', () => el.classList.remove('is-press'));
  });
})();
