/* ================================================================
   宇树机器人实验室 · site.js
   全部是增强：关掉脚本，页面仍然完整可读、可导航。
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
    '.course-spec', '.goals', '.goals-k', '.goals-list li', '.caution',
    '.contact-say > *', '.contact-qr',
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

  /* ---------------- 3 · 微信二维码弹层 ---------------- */
  const wxDialog = document.getElementById('wx-dialog');
  if (wxDialog && typeof wxDialog.showModal === 'function') {
    // 没有弹层能力的环境下，这些 <a> 会退化成直接打开二维码图片 —— 不拦截
    $$('[data-wx]').forEach((a) => {
      a.addEventListener('click', (e) => {
        e.preventDefault();
        wxDialog.showModal();
        wxDialog.focus();          // 焦点落在弹层本身，关闭按钮的焦点环只在键盘 Tab 时出现
      });
    });
    wxDialog.addEventListener('click', (e) => {
      if (e.target === wxDialog) wxDialog.close();   // 点遮罩关闭
    });
    $$('[data-wx-close]').forEach((a) => {
      a.addEventListener('click', () => wxDialog.close());
    });
  }

  /* ---------------- 4 · 控件按下反馈 ---------------- */
  $$('.btn').forEach((el) => {
    el.addEventListener('pointerdown', () => el.classList.add('is-press'));
    for (const ev of ['pointerup', 'pointercancel', 'pointerleave']) {
      el.addEventListener(ev, () => el.classList.remove('is-press'));
    }
  });
})();
