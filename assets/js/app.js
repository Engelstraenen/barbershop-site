/* KANTE – Wisch drüber. Keine Abhängigkeiten. */
(() => {
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fq = new URLSearchParams(location.search).get('farbe');
  if (fq) { const [b, a] = fq.split(','); const rgb = h => [0, 2, 4].map(i => parseInt(h.substr(i, 2), 16)).join(', '); const st = document.documentElement.style;
    if (b) { st.setProperty('--bg', '#' + b); st.setProperty('--bg-rgb', rgb(b)); } if (a) { st.setProperty('--or', '#' + a); st.setProperty('--or-rgb', rgb(a)); } }

  const hd = $('.hd'); const onHd = () => hd && hd.classList.toggle('solid', scrollY > 30 || !$('.hero')); addEventListener('scroll', onHd, { passive: true }); onHd();
  $('.burger')?.addEventListener('click', () => { const o = document.body.classList.toggle('menu-open'); $('.burger').setAttribute('aria-expanded', o); });
  $$('.nav a').forEach(a => a.addEventListener('click', () => document.body.classList.remove('menu-open')));
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .2 });
  $$('.rv, .kin').forEach(el => io.observe(el));
  const fmt = (v, d) => v.toLocaleString('de-DE', { minimumFractionDigits: d, maximumFractionDigits: d });
  const cio = new IntersectionObserver(es => es.forEach(e => { if (!e.isIntersecting) return; cio.unobserve(e.target); const el = e.target, to = +el.dataset.count, d = +(el.dataset.dec || 0), pre = el.dataset.pre || '', suf = el.dataset.suf || ''; if (reduce) { el.textContent = pre + fmt(to, d) + suf; return; } const t0 = performance.now(); const tick = t => { const k = clamp((t - t0) / 1600, 0, 1); el.textContent = pre + fmt(to * (1 - Math.pow(1 - k, 3)), d) + suf; if (k < 1) requestAnimationFrame(tick); }; requestAnimationFrame(tick); }), { threshold: .5 });
  $$('[data-count]').forEach(el => cio.observe(el));

  // ---------- Wisch drüber: Vorher/Nachher per Ziehen ----------
  $$('.swipe').forEach(sw => {
    let drag = false, touched = false;
    const set = x => sw.style.setProperty('--x', clamp(x, 0, 100) + '%');
    const at = e => { const r = sw.getBoundingClientRect(); return (e.clientX - r.left) / r.width * 100; };
    sw.addEventListener('pointerdown', e => { drag = true; touched = true; sw.setPointerCapture(e.pointerId); set(at(e)); });
    sw.addEventListener('pointermove', e => { if (drag) set(at(e)); else if (e.pointerType === 'mouse' && touched) set(at(e)); });
    sw.addEventListener('pointerup', () => drag = false);
    sw.addEventListener('keydown', e => { const v = parseFloat(getComputedStyle(sw).getPropertyValue('--x')) || 50; if (e.key === 'ArrowLeft') set(v - 5); if (e.key === 'ArrowRight') set(v + 5); });
    // Aktion ab der ersten Sekunde: Wischlinie fährt einmal von selbst
    if (!reduce && sw.dataset.auto !== undefined) { const t0 = performance.now(); const run = t => { if (touched) return; const k = (t - t0) / 2600; if (k > 1) { set(50); return; } set(50 + Math.sin(k * Math.PI * 2) * 38); requestAnimationFrame(run); }; setTimeout(() => requestAnimationFrame(run), 700); }
    else if (!reduce) { const o = new IntersectionObserver(es => es.forEach(en => { if (!en.isIntersecting) return; o.disconnect(); const t0 = performance.now(); const run = t => { if (touched) return; const k = (t - t0) / 2200; if (k > 1) { set(50); return; } set(50 - Math.sin(k * Math.PI * 2) * 34); requestAnimationFrame(run); }; requestAnimationFrame(run); }), { threshold: .5 }); o.observe(sw); }
  });

  // ---------- Barber wählen an der Spiegelwand ----------
  const pickBarber = k => { $$('.bcard').forEach(c => c.classList.toggle('on', c.dataset.b === k)); const b = $(`#booking .bb[data-b="${k}"]`); b && b.click(); };
  $$('.bcard').forEach(c => c.addEventListener('click', () => { pickBarber(c.dataset.b); }));

  // ---------- Film im Spiegel (Bildfolge per Scroll) ----------
  const fs = $('.filmsec');
  if (fs) {
    const stage = $('.stage', fs), cv = $('canvas', fs), ctx = cv.getContext('2d'), stills = $$('.still img', fs), steps = $$('.steps3 span', fs);
    let mob = innerWidth < 900; const N = +(stage.dataset.n || 0), frames = []; let p = 0, last = -1;
    const pat = () => stage.dataset[mob && innerHeight > 500 ? 'seqm' : 'seq'];
    const size = () => { const r = Math.min(devicePixelRatio || 1, 2), b = cv.getBoundingClientRect(); cv.width = Math.round(b.width * r); cv.height = Math.round(b.height * r); ctx.imageSmoothingQuality = 'high'; };
    const draw = force => { if (!frames.length) return; let i = clamp(Math.round(p * (N - 1)), 0, N - 1); while (i > 0 && !frames[i].complete) i--; if (i === last && !force) return; last = i; const f = frames[i]; if (!f.naturalWidth) return; const W = cv.width, H = cv.height, s = Math.max(W / f.naturalWidth, H / f.naturalHeight), w = f.naturalWidth * s, h = f.naturalHeight * s; ctx.drawImage(f, (W - w) / 2, (H - h) * .4, w, h); };
    const start = () => { for (let i = 0; i < N; i++) { const im = new Image(); im.decoding = 'async'; if (i === 0) im.onload = () => { stage.classList.add('seq'); size(); draw(true); }; im.src = pat().replace('###', String(i).padStart(3, '0')); frames.push(im); } };
    if (N && pat()) { if (document.readyState === 'complete') setTimeout(start, 200); else addEventListener('load', () => setTimeout(start, 200)); }
    addEventListener('resize', () => { mob = innerWidth < 900; size(); draw(true); });
    const upd = () => {
      const r = fs.getBoundingClientRect(), total = fs.offsetHeight - innerHeight; p = clamp(-r.top / total, 0, 1);
      if (!stage.classList.contains('seq') && stills.length) { const i = p < .34 ? 0 : p < .67 ? 1 : 2; stills.forEach((s, j) => s.style.opacity = j === Math.min(i, stills.length - 1) ? 1 : 0); }
      else draw();
      const st = p < .3 ? 0 : p < .75 ? 1 : 2; steps.forEach((s, j) => s.classList.toggle('on', j === st));
    };
    addEventListener('scroll', () => requestAnimationFrame(upd), { passive: true }); upd();
  }

  // ---------- Fade-Höhe ----------
  const cfg = $('.cfg');
  if (cfg) { const imgs = $$('.mirror img', cfg), name = $('.cfgname', cfg), txt = $('.cfgtxt', cfg);
    $$('.chip', cfg).forEach((c, i) => c.addEventListener('click', () => { $$('.chip', cfg).forEach(x => x.classList.toggle('on', x === c)); imgs.forEach((im, j) => im.classList.toggle('on', j === i)); name.textContent = c.dataset.name; txt.textContent = c.dataset.txt; })); }

  // ---------- Termin (Beispiel) ----------
  const bk = $('#booking');
  if (bk) {
    const st = { svc: null, bb: null, day: null, slot: null }; const days = $('.days', bk), slots = $('.slots', bk), sum = $('.sum p', bk), go = $('.sum .btn', bk);
    const wd = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'], now = new Date(); let h = '';
    for (let i = 0, n = 0; n < 7; i++) { const d = new Date(now); d.setDate(now.getDate() + i); if (d.getDay() === 0 || d.getDay() === 1) continue; h += `<button class="opt" data-d="${d.toISOString().slice(0, 10)}">${i === 0 ? 'Heute' : wd[d.getDay()]}<small>${d.getDate()}.${d.getMonth() + 1}.</small></button>`; n++; }
    days.innerHTML = h;
    const times = ['10:00', '10:30', '11:00', '11:30', '12:00', '13:00', '13:30', '14:00', '15:00', '16:00', '16:30', '17:30', '18:00', '19:00', '19:30'];
    const rs = () => { let x = 0; for (const c of (st.day || '') + (st.bb || '')) x = (x * 31 + c.charCodeAt(0)) >>> 0; slots.innerHTML = times.map((t, i) => `<button class="opt" ${(((x >> (i % 24)) & 3) === 0 || (x + i * 5) % 4 === 0) ? 'disabled' : ''} data-t="${t}">${t}</button>`).join(''); $$('button', slots).forEach(b => b.addEventListener('click', () => { $$('button', slots).forEach(y => y.classList.toggle('on', y === b)); st.slot = b.dataset.t; sync(); })); };
    const sync = () => { const n = st.bb ? $(`.bb[data-b="${st.bb}"]`, bk).dataset.name : 'egal wer'; sum.innerHTML = `<b>${st.svc || 'Leistung wählen'}</b> · ${n}${st.day ? ' · ' + new Date(st.day).toLocaleDateString('de-DE', { weekday: 'short', day: 'numeric', month: 'numeric' }) : ''}${st.slot ? ' · ' + st.slot : ''}`; const ok = st.svc && st.day && st.slot; go.toggleAttribute('disabled', !ok); go.style.opacity = ok ? 1 : .45; };
    const pick = (sel, key, attr, after) => $$(sel, bk).forEach(b => b.addEventListener('click', () => { $$(sel, bk).forEach(x => x.classList.toggle('on', x === b)); st[key] = b.dataset[attr]; after && after(); sync(); }));
    pick('[data-svc]', 'svc', 'svc'); pick('.bb', 'bb', 'b', () => { st.slot = null; rs(); $$('.bcard').forEach(c => c.classList.toggle('on', c.dataset.b === st.bb)); }); pick('.days .opt', 'day', 'd', () => { st.slot = null; rs(); });
    $('.again .btn', bk)?.addEventListener('click', () => { $('[data-svc="Skin Fade"]', bk)?.click(); $('.bb[data-b="milan"]', bk)?.click(); $('.days .opt', bk)?.click(); const f = $('.slots .opt:not([disabled])', bk); f && f.click(); });
    $('.gapcard .btn')?.addEventListener('click', () => { $('[data-svc="Haarschnitt"]', bk)?.click(); $('.days .opt', bk)?.click(); const f = [...$$('.slots .opt:not([disabled])', bk)].pop(); f && f.click(); bk.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' }); });
    rs(); sync();
    go.addEventListener('click', () => { if (go.hasAttribute('disabled')) return; $('#dlg-ok p').innerHTML = `${sum.innerHTML}.<br>Demo: Es wurde nichts gebucht. Im echten Betrieb kommt jetzt eine SMS, 24 h vorher eine Erinnerung.`; $('#dlg-ok').classList.add('on'); });
  }
  $$('.dlg').forEach(d => d.addEventListener('click', e => { if (e.target === d || e.target.closest('[data-close]')) d.classList.remove('on'); }));
  addEventListener('keydown', e => { if (e.key === 'Escape') $$('.dlg.on').forEach(d => d.classList.remove('on')); });

  const ap = $('.apply');
  if (ap) { const steps = $$('.step', ap), bar = $('.prog60 i', ap), tm = $('.timer', ap); let t0, iv; const show = i => { steps.forEach((s, j) => s.classList.toggle('on', j === i)); bar.style.width = (i / (steps.length - 1) * 100) + '%'; if (!t0 && i > 0) { t0 = Date.now(); iv = setInterval(() => tm.textContent = Math.max(0, 60 - Math.round((Date.now() - t0) / 1000)) + ' s', 500); } if (i === steps.length - 1) clearInterval(iv); };
    $$('[data-next]', ap).forEach(b => b.addEventListener('click', () => show(steps.indexOf(b.closest('.step')) + 1))); $('form', ap)?.addEventListener('submit', e => { e.preventDefault(); show(steps.length - 1); }); }

  const revs = $$('.rev'); if (revs.length) { let i = 0; revs[0].classList.add('on'); setInterval(() => { revs[i].classList.remove('on'); i = (i + 1) % revs.length; revs[i].classList.add('on'); }, 5000); }

  $$('[data-ics]').forEach(b => b.addEventListener('click', () => {
    const d = new Date(); d.setDate(d.getDate() + 7 * +b.dataset.ics); const z = n => String(n).padStart(2, '0'); const day = `${d.getFullYear()}${z(d.getMonth() + 1)}${z(d.getDate())}`;
    const ics = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Demo//DE', 'BEGIN:VEVENT', 'UID:' + Date.now() + '@demo', 'DTSTAMP:' + day + 'T090000', 'DTSTART;VALUE=DATE:' + day, 'SUMMARY:' + b.dataset.title, 'END:VEVENT', 'END:VCALENDAR'].join('\r\n');
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([ics], { type: 'text/calendar' })); a.download = 'erinnerung.ics'; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  }));
  $$('a[data-sub]').forEach(a => a.addEventListener('click', () => { try { sessionStorage.setItem('kt-back', JSON.stringify({ y: scrollY })); } catch (e) {} }));
  if (location.hash === '#zurueck') { try { const s = JSON.parse(sessionStorage.getItem('kt-back') || 'null'); if (s) { history.replaceState(null, '', location.pathname); requestAnimationFrame(() => scrollTo(0, s.y)); } } catch (e) {} }
})();
