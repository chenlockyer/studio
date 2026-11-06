/* ================================================================
   落地组 · site.js
   Everything here is enhancement: the page reads and works with it off.
   ================================================================ */
(() => {
  'use strict';
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  /* ---------- 1. entrances ---------- */
  const revealables = $$('.reveal');
  const reveal = (el) => el.classList.add('is-in');
  if ('IntersectionObserver' in window && !reduce.matches) {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) if (e.isIntersecting) { reveal(e.target); io.unobserve(e.target); }
    }, { rootMargin: '160px 0px 160px 0px', threshold: 0 });
    revealables.forEach((el, i) => {
      el.style.setProperty('--i', String(Math.min(i % 4, 3)));
      io.observe(el);
    });
    // a block that never entered the observer's range must still not stay invisible
    addEventListener('load', () => {
      setTimeout(() => { revealables.forEach(reveal); io.disconnect(); }, 2200);
    });
    // 兜底：某些环境（无头渲染、分享预览、节能模式下页面判为不可见）IO 永不回调，
    // 内容会整块留在 opacity:0。document 就绪后无论如何都要让它们出现。
    document.addEventListener('DOMContentLoaded', () => {
      setTimeout(() => { revealables.forEach(reveal); }, 3200);
    });
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) revealables.forEach(reveal);
    });
  } else {
    revealables.forEach(reveal);
  }

  /* ---------- 2. hero: the pinned poster (the strip advances, the sentence holds) ---------- */
  const hero = document.querySelector('.hero');
  const stripTrack = document.querySelector('.strip-track');
  const stripFrames = $$('.strip-frame');
  const stripCaption = document.getElementById('hero-caption');
  const CAPTIONS = ['学院楼 · 2 台 G1', '走向电梯口 · 3 站', '拉丁舞 · 动作定制', '指挥家 · 演出'];
  const heroVideo = document.querySelector('.hero-video');

  if (hero && stripTrack && stripFrames.length) {
    let current = -1;

    const geometry = () => {
      const cs = getComputedStyle(stripTrack);
      const gap = parseFloat(cs.rowGap) || parseFloat(cs.gap) || 0;
      const stripH = document.querySelector('.hero-strip').clientHeight;
      // one frame centred, leaving a quarter of the strip's height above and below
      const frameH = Math.round(stripH * 0.5);
      stripFrames.forEach((f) => f.style.setProperty('--frame-h', frameH + 'px'));
      return { gap, frameH, stripH };
    };

    const setFrame = (i) => {
      if (i === current) return;
      current = i;
      const { gap, frameH, stripH } = geometry();
      // the live frame is centred in the strip; the ones above and below are its neighbours
      const y = (stripH - frameH) / 2 - i * (frameH + gap);
      stripTrack.style.transform = `translate3d(0, ${y}px, 0)`;
      stripFrames.forEach((f, k) => f.classList.toggle('is-live', k === i));
      if (stripCaption) stripCaption.textContent = CAPTIONS[i] || '';
    };

    setFrame(0);

    // the strip's geometry depends on the viewport: re-place it on resize
    let lastW = window.innerWidth;
    addEventListener('resize', () => {
      if (window.innerWidth === lastW) return;
      lastW = window.innerWidth;
      current = -1;
      setFrame(Math.max(0, current));
    }, { passive: true });

    if (heroVideo && !reduce.matches && window.IntersectionObserver) {
      const io = new IntersectionObserver(([e]) => {
        if (e.isIntersecting) heroVideo.play?.().catch(() => {});
        else heroVideo.pause?.();
      }, { threshold: 0.2 });
      io.observe(hero);
    } else if (heroVideo) {
      heroVideo.play?.().catch(() => {});
    }

    const stripEl = document.querySelector('.hero-strip');
    let ticking = false;
    const onScroll = () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        const r = hero.getBoundingClientRect();
        const span = r.height - window.innerHeight;
        const p2 = span > 0 ? Math.min(1, Math.max(0, -r.top / span)) : 0;
        const i = Math.min(stripFrames.length - 1, Math.floor(p2 * stripFrames.length * 1.02));
        setFrame(i);

        // the strip drifts and shrinks a little as the sentence's scroll run advances:
        // the device is alive, not a still tile
        if (stripEl && !reduce.matches && window.innerWidth > 1100) {
          const drift = Math.sin(p2 * Math.PI) * 1.6;     // vw, eased in and out
          const scale = 1 - Math.sin(p2 * Math.PI) * 0.06;
          stripEl.style.transform = `translateX(calc(-50% + ${drift.toFixed(2)}vw)) scale(${scale.toFixed(3)})`;
          // the caption travels the other way, so the strip reads as passing through
          if (stripCaption) stripCaption.style.transform = `translateX(calc(-50% - ${drift.toFixed(2)}vw)) scale(${(1 + Math.sin(p2 * Math.PI) * 0.02).toFixed(3)})`;
        }
        ticking = false;
      });
    };
    addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- 3. delivery: pinned fragment, changing state ---------- */
  const steps = $$('.step');
  const frames = $$('.stage-frame');
  const stageLabel = document.getElementById('stage-label');
  const LABELS = [
    '勘察之后，先在后台把这条路排出来。',
    '建图：本体雷达边走边出图，不依赖外网。',
    '地图可编辑：走偏的墙线当场修掉。',
    '上线之后，场馆自己的人接着改。',
  ];
  const FRAME_FOR_STEP = [0, 1, 2, 2];
  if (steps.length && frames.length) {
    const pick = (i) => {
      const f = FRAME_FOR_STEP[i] ?? i;
      steps.forEach((s, k) => s.classList.toggle('is-live', k === i));
      frames.forEach((el, k) => el.classList.toggle('is-live', k === f));
      if (stageLabel) stageLabel.textContent = LABELS[i] || '';
    };
    pick(0);
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((entries) => {
        for (const e of entries) {
          if (!e.isIntersecting) continue;
          const i = steps.indexOf(e.target);
          if (i >= 0) pick(i);
        }
      }, { rootMargin: '-45% 0px -45% 0px', threshold: 0 });
      steps.forEach((s) => io.observe(s));
    } else {
      steps.forEach((s, i) => s.addEventListener('mouseenter', () => pick(i)));
    }
  }

  /* ---------- 4. the one live thing: venue adapter ---------- */
  const VENUES = [
    {
      name: '科技馆 · 展厅',
      machines: '2 台 G1',
      stops: '3–5 个',
      time: '约 8 分钟带讲',
      lead: '2–3 周',
      scope: '场地勘察 · 建图采点 · 讲解词定制 · 真机联调 · 2 人交接培训 · 3 个月维保',
      ask: '说明展厅面积、展品分区、每天客流高峰时段，我按你的动线排站。',
    },
    {
      name: '学校 · 实验室',
      machines: '1–2 台',
      stops: '3 个',
      time: '约 5 分钟带讲',
      lead: '2 周',
      scope: '实验室走线勘察 · 建图采点 · 讲解词定制 · 真机联调 · 2 人交接培训 · 3 个月维保',
      ask: '说明实验室在哪几层、要不要跨楼层、走廊有多宽，我按真实净空排路线。',
    },
    {
      name: '园区 · 前台',
      machines: '1 台',
      stops: '2–3 个',
      time: '约 4 分钟带讲',
      lead: '1–2 周',
      scope: '前台动线勘察 · 建图采点 · 迎宾与引导词 · 真机联调 · 2 人交接培训 · 3 个月维保',
      ask: '说明前台到会议室的距离、有没有门禁与地毯，这两项最容易让机器人停下来。',
    },
    {
      name: '商演 · 活动',
      machines: '按场次排',
      stops: '不定站点',
      time: '按节目单',
      lead: '3–4 周出片',
      scope: '动作需求拆解 · 编排与仿真验证 · 真机排练 · 现场值守 · 彩排一次',
      ask: '给我一段参考视频和节拍，我告诉你这个动作在 G1 上做不做得出来。',
    },
    {
      name: '我自己有本体',
      machines: '你出设备',
      stops: '按场地定',
      time: '按场地定',
      lead: '1–2 周',
      scope: '远端环境核查 · 部署与授权 · 方案配置 · 你的人接手培训 · 3 个月维保',
      ask: '说明你的 G1 型号与自由度配置、Jetson 版本，我判断要不要先做环境迁移。',
    },
  ];

  const chips = $$('.chip');
  const outVenue = document.getElementById('out-venue');
  const outMachines = document.getElementById('out-machines');
  const outStops = document.getElementById('out-stops');
  const outTime = document.getElementById('out-time');
  const outLead = document.getElementById('out-lead');
  const outScope = document.getElementById('out-scope');
  const outAskEl = document.querySelector('.out-ask');
  const venueSelect = document.querySelector('#ask-form select[name="venue"]');

  const renderVenue = (i) => {
    const v = VENUES[i];
    if (!v) return;
    chips.forEach((c, k) => {
      const on = k === i;
      c.classList.toggle('is-on', on);
      c.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    if (outVenue) outVenue.textContent = v.name;
    if (outMachines) outMachines.textContent = v.machines;
    if (outStops) outStops.textContent = v.stops;
    if (outTime) outTime.textContent = v.time;
    if (outLead) outLead.textContent = v.lead;
    if (outScope) outScope.textContent = '交付含：' + v.scope;
    if (outAskEl) outAskEl.textContent = v.ask;
    if (venueSelect) venueSelect.selectedIndex = i;
    if (outVenue && !reduce.matches) {
      outVenue.animate?.(
        [{ opacity: 0.35, transform: 'translateY(6px)' }, { opacity: 1, transform: 'none' }],
        { duration: 260, easing: 'cubic-bezier(0.22,1,0.36,1)' }
      );
    }
  };

  chips.forEach((c, i) => {
    c.addEventListener('click', () => renderVenue(i));
  });
  if (chips.length) renderVenue(0);

  /* ---------- 5. FAQ ---------- */
  const qs = $$('.faq-q');
  const answers = $$('.faq-a');
  const selectQ = (i) => {
    qs.forEach((q, k) => {
      const on = k === i;
      q.classList.toggle('is-on', on);
      q.setAttribute('aria-selected', on ? 'true' : 'false');
      q.setAttribute('tabindex', on ? '0' : '-1');
    });
    answers.forEach((a, k) => {
      const on = k === i;
      a.hidden = !on;
      a.classList.toggle('is-on', on);
    });
  };
  qs.forEach((q, i) => {
    q.addEventListener('click', () => selectQ(i));
    q.addEventListener('focus', () => selectQ(i));
    q.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
        e.preventDefault();
        const n = (i + 1) % qs.length;
        selectQ(n); qs[n].focus();
      } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
        e.preventDefault();
        const n = (i - 1 + qs.length) % qs.length;
        selectQ(n); qs[n].focus();
      }
    });
  });
  if (qs.length) selectQ(0);

  /* ---------- 5b. group-control viewer: four tabs, one pane ---------- */
  const gTabs = $$('.gc-tab');
  const gPanes = $$('.gc-pane');
  const selectG = (i) => {
    gTabs.forEach((t, k) => {
      const on = k === i;
      t.classList.toggle('is-on', on);
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.setAttribute('tabindex', on ? '0' : '-1');
    });
    gPanes.forEach((p, k) => {
      const on = k === i;
      p.hidden = !on;
      p.classList.toggle('is-on', on);
    });
  };
  gTabs.forEach((t, i) => {
    t.addEventListener('click', () => selectG(i));
    t.addEventListener('focus', () => selectG(i));
    t.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
        e.preventDefault();
        const n = (i + 1) % gTabs.length;
        selectG(n); gTabs[n].focus();
      } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
        e.preventDefault();
        const n = (i - 1 + gTabs.length) % gTabs.length;
        selectG(n); gTabs[n].focus();
      }
    });
  });
  if (gTabs.length) selectG(0);

  /* ---------- 6. the ask form: copy the brief, no fake submit ---------- */
  const form = document.getElementById('ask-form');
  const hint = document.getElementById('ask-hint');
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const who = (data.get('who') || '').toString().trim() || '（称呼待填）';
      const venue = (data.get('venue') || '').toString();
      const when = (data.get('when') || '').toString();
      const contact = (data.get('contact') || '').toString().trim() || '（联系方式待填）';
      const brief = [
        `称呼：${who}`,
        `场地：${venue}`,
        `时间：${when}`,
        `联系：${contact}`,
        '（从官网发的，想先要一份初步排法）',
      ].join('\n');
      try {
        await navigator.clipboard.writeText(brief);
        if (hint) {
          hint.textContent = '已复制：' + brief.replace(/\n/g, ' · ') + '。去微信粘贴给我，或直接扫码。';
          hint.classList.add('ask-done');
        }
      } catch {
        if (hint) {
          hint.textContent = '复制失败，手动复制这段发我：' + brief.replace(/\n/g, ' · ');
          hint.classList.add('ask-done');
        }
      }
    });
  }

  /* ---------- 7. the three scenes: each panel's card arrives as the panel enters ---------- */
  const panels = $$('.panel');
  if (panels.length && 'IntersectionObserver' in window && !reduce.matches) {
    const pio = new IntersectionObserver((entries) => {
      for (const e of entries) {
        const card = e.target.querySelector('.panel-card');
        if (!card) continue;
        if (e.isIntersecting) card.classList.add('is-in');
        else card.classList.remove('is-in');
      }
    }, { rootMargin: '-18% 0px -18% 0px', threshold: 0.15 });
    panels.forEach((p) => pio.observe(p));
  } else {
    $$('.panel-card').forEach((c) => c.classList.add('is-in'));
  }

  /* ---------- 7b. the three scenes: one full screen per scroll step ---------- */
  const sceneTrack = document.querySelector('.scene-track');
  const panelsList = $$('.panel');
  const dots = $$('.scene-dots .dot');

  if (sceneTrack && panelsList.length) {
    let scene = -1;

    const applyScene = (i) => {
      if (i === scene) return;
      scene = i;
      panelsList.forEach((p, k) => {
        const on = k === i;
        p.classList.toggle('is-active', on);
        // the panel that just left steps back; the one arriving slides in from below
        const delta = k - i;
        p.style.transform = delta === 0 ? 'translate3d(0,0,0)' : `translate3d(0, ${delta * 18}%, 0)`;
        p.style.opacity = on ? '1' : '0';
        p.style.pointerEvents = on ? 'auto' : 'none';
      });
      dots.forEach((d, k) => {
        const on = k === i;
        d.classList.toggle('is-on', on);
        d.setAttribute('aria-current', on ? 'true' : 'false');
      });
    };

    const pickScene = () => {
      const r = sceneTrack.getBoundingClientRect();
      const span = r.height - window.innerHeight;
      const p2 = span > 0 ? Math.min(1, Math.max(0, -r.top / span)) : 0;
      // one threshold per screen: the 300vh track maps to three whole screens
      const i = Math.min(panelsList.length - 1, Math.round(p2 * (panelsList.length - 1)));
      applyScene(i);
    };

    let st = false;
    addEventListener('scroll', () => {
      if (st) return;
      st = true;
      requestAnimationFrame(() => { pickScene(); st = false; });
    }, { passive: true });
    addEventListener('resize', pickScene, { passive: true });
    pickScene();

    // the dots jump straight to a screen (keyboard and thumb both work)
    dots.forEach((d, i) => {
      d.addEventListener('click', () => {
        const r = sceneTrack.getBoundingClientRect();
        const span = r.height - window.innerHeight;
        const y = window.scrollY + r.top + (span * i) / (panelsList.length - 1);
        window.scrollTo({ top: y, behavior: reduce.matches ? 'auto' : 'smooth' });
      });
    });
  }

  /* ---------- 8. the evidence numbers count up once ---------- */
  const counters = $$('[data-count]');
  if (counters.length && 'IntersectionObserver' in window && !reduce.matches) {
    const settle = (el) => { el.textContent = el.dataset.count; };
    const cio = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        const el = e.target;
        const target = Number(el.dataset.count);
        const dur = 900;
        const t0 = performance.now();
        const step = (now) => {
          const k = Math.min(1, (now - t0) / dur);
          const eased = 1 - Math.pow(1 - k, 3);
          el.textContent = String(Math.round(target * eased));
          if (k < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
        cio.unobserve(el);
      }
    }, { threshold: 0.4 });
    counters.forEach((c) => { c.textContent = '0'; cio.observe(c); });
    // 兜底：观察器没触发时（无头渲染、分享预览抓图、部分爬虫），数值不能停在 0
    addEventListener('load', () => {
      setTimeout(() => counters.forEach(settle), 2400);
    });
    // 还有一层：页面被判为不可见时 IO 不回调，同样要落到真实值
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) counters.forEach(settle);
    });
  } else {
    counters.forEach((c) => { c.textContent = c.dataset.count; });
  }

  /* ---------- 9. the marquee pauses when it leaves the screen (saves battery) ---------- */
  const marqueeTrack = document.querySelector('.marquee-track');
  if (marqueeTrack && 'IntersectionObserver' in window) {
    const mio = new IntersectionObserver(([e]) => {
      marqueeTrack.style.animationPlayState = e.isIntersecting ? 'running' : 'paused';
    }, { threshold: 0.05 });
    mio.observe(document.querySelector('.marquee'));
  }

  /* ---------- 10. control feedback ---------- */

  $$('.btn, .chip, .faq-q').forEach((el) => {
    el.addEventListener('pointerdown', () => el.classList.add('is-press'));
    el.addEventListener('pointerup', () => el.classList.remove('is-press'));
    el.addEventListener('pointercancel', () => el.classList.remove('is-press'));
  });
})();