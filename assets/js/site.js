/* ================================================================
   落地组 · site.js
   全部是增强：关掉脚本，页面仍然完整可读、可导航、可复制。
   ================================================================ */
(() => {
  'use strict';

  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const calm = () => reduce.matches;

  /* ---------------- 1 · 区块入场：各自错开 ---------------- */
  const PARTS = [
    '.sec-head .h', '.sec-head .lead',
    '.media-wide', '.chain-video', '.steps4 .step', '.facts3 .fact',
    '.cmd', '.tagrow',
    '.steps-d .dstep', '.handover', '.paper .fig',
    '.course-spec', '.goals-k', '.goals-list li', '.caution',
    '.faq-item', '.faq-aside',
    '.contact-say > *', '.ask',
  ];
  const targets = [];
  for (const sel of PARTS) {
    $$(sel).forEach((el, i) => {
      el.classList.add('rv');
      el.style.setProperty('--i', String(Math.min(i, 5)));
      targets.push(el);
    });
  }
  if ('IntersectionObserver' in window && !calm()) {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        e.target.classList.add('is-in');
        io.unobserve(e.target);
      }
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.04 });
    targets.forEach((el) => io.observe(el));
    addEventListener('load', () => {
      setTimeout(() => { targets.forEach((el) => el.classList.add('is-in')); io.disconnect(); }, 2600);
    });
  } else {
    targets.forEach((el) => el.classList.add('is-in'));
  }

  /* ---------------- 2 · 视频：进视口才播，离开就停（省流量省电） ---------------- */
  const loops = $$('video.loop');
  if (loops.length) {
    if (calm()) {
      loops.forEach((v) => v.pause?.());
    } else if ('IntersectionObserver' in window) {
      const vio = new IntersectionObserver((entries) => {
        for (const e of entries) {
          const v = e.target;
          if (e.isIntersecting) v.play?.().catch(() => {});
          else v.pause?.();
        }
      }, { threshold: 0.15 });
      loops.forEach((v) => vio.observe(v));
    } else {
      loops.forEach((v) => v.play?.().catch(() => {}));
    }
  }

  /* 首屏视频：安静模式或不支持自动播放时，退成 poster */
  const heroVideo = document.querySelector('.hero-video');
  if (heroVideo) {
    if (calm()) {
      heroVideo.pause?.();
      heroVideo.removeAttribute('autoplay');
    } else {
      heroVideo.play?.().catch(() => {});
    }
  }

  /* ---------------- 3 · 问答：同组只开一个 ---------------- */
  const faqItems = $$('.faq-item');
  faqItems.forEach((d) => {
    d.addEventListener('toggle', () => {
      if (!d.open) return;
      faqItems.forEach((o) => { if (o !== d) o.open = false; });
    });
  });

  /* ---------------- 4 · 表单：复制成一段话，不做假提交 ---------------- */
  const form = document.getElementById('ask-form');
  const hint = document.getElementById('ask-hint');
  const fallback = document.getElementById('ask-fallback');
  const briefBox = document.getElementById('ask-brief');
  if (form && hint) {
    const DEFAULT_HINT = hint.textContent.trim();

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const val = (k) => (data.get(k) || '').toString().trim();
      const brief = [
        `称呼：${val('who') || '（待填）'}`,
        `场地：${val('venue')}`,
        `时间：${val('when')}`,
        `联系：${val('contact') || '（待填）'}`,
        '（从官网发的，想先要一份初步落地方案）',
      ].join('\n');

      const showFallback = () => {
        if (!fallback || !briefBox) return;
        briefBox.value = brief;
        fallback.hidden = false;
        briefBox.focus();
        briefBox.select();
      };

      try {
        await navigator.clipboard.writeText(brief);
        hint.textContent = '已复制。直接粘贴到微信发给我们即可。';
        if (fallback) fallback.hidden = true;
      } catch {
        // file:// 打开或非 HTTPS 时剪贴板接口不可用：给一段可全选的手动复制文本
        hint.textContent = '这段需求已经生成，全选下面内容复制即可。';
        showFallback();
      }
    });

    form.addEventListener('reset', () => {
      hint.textContent = DEFAULT_HINT;
      if (fallback) fallback.hidden = true;
    });
  }

  /* ---------------- 5 · 控件按下反馈 ---------------- */
  $$('.btn, .faq-item summary').forEach((el) => {
    el.addEventListener('pointerdown', () => el.classList.add('is-press'));
    for (const ev of ['pointerup', 'pointercancel', 'pointerleave']) {
      el.addEventListener(ev, () => el.classList.remove('is-press'));
    }
  });
})();
